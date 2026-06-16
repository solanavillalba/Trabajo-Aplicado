import pygame
import requests
import io
import random

# ─────────────────────────────────────────────
#  PALETA Y TIPOGRAFÍA
# ─────────────────────────────────────────────
COLOR_FONDO       = (15,  20,  40)    # azul noche profundo
COLOR_PANEL       = (25,  35,  60)    # panel oscuro
COLOR_BORDE       = (80, 120, 200)    # azul eléctrico
COLOR_BORDE_SEL   = (255, 210,  40)   # amarillo pikachu (seleccionado)
COLOR_TEXTO       = (220, 230, 255)   # blanco frío
COLOR_SUBTEXTO    = (130, 150, 200)   # gris azulado
COLOR_ATK         = (255,  90,  80)   # rojo ataque
COLOR_DEF         = (80,  180, 255)   # azul defensa
COLOR_SPD         = (100, 230, 100)   # verde velocidad
COLOR_ADP         = (200, 130, 255)   # violeta adaptabilidad
COLOR_BOTON       = (40,  60, 110)    # botón normal
COLOR_BOTON_HOV   = (60,  90, 160)    # botón hover
COLOR_BOTON_SEL   = (255, 210,  40)   # botón elegido
COLOR_TITULO_CAT  = {
    "Novatos": (100, 220, 130),
    "Medios":  (80,  180, 255),
    "Altos":   (255, 120,  80),
}

ANCHO, ALTO = 1100, 680

# ─────────────────────────────────────────────
#  HELPERS PYGAME
# ─────────────────────────────────────────────
def dibujar_texto(sup, texto, fuente, color, x, y, centrado=False):
    surf = fuente.render(texto, True, color)
    rect = surf.get_rect()
    if centrado:
        rect.centerx = x
        rect.y = y
    else:
        rect.x = x
        rect.y = y
    sup.blit(surf, rect)
    return rect

def dibujar_panel(sup, rect, color=COLOR_PANEL, radio=10, borde=None, grosor_borde=2):
    pygame.draw.rect(sup, color, rect, border_radius=radio)
    if borde:
        pygame.draw.rect(sup, borde, rect, grosor_borde, border_radius=radio)

def barra_stat(sup, x, y, ancho, valor, maximo, color, fuente_p, etiqueta):
    """Dibuja una mini barra de stat con etiqueta y valor."""
    dibujar_texto(sup, etiqueta, fuente_p, COLOR_SUBTEXTO, x, y)
    bg = pygame.Rect(x + 40, y + 2, ancho, 10)
    fill_w = int((valor / maximo) * ancho)
    pygame.draw.rect(sup, (50, 60, 90), bg, border_radius=5)
    if fill_w > 0:
        pygame.draw.rect(sup, color, (x + 40, y + 2, fill_w, 10), border_radius=5)
    val_txt = fuente_p.render(f"{valor:.2f}", True, COLOR_TEXTO)
    sup.blit(val_txt, (x + 40 + ancho + 4, y))

# ─────────────────────────────────────────────
#  DESCARGA DE SPRITES
# ─────────────────────────────────────────────
_cache_sprites = {}

def obtener_sprite(nombre_pokemon):
    """Descarga el sprite del pokemon de PokeAPI y lo devuelve como Surface de pygame.
    Usa un caché en memoria para no repetir descargas."""
    nombre = nombre_pokemon.lower()
    if nombre in _cache_sprites:
        return _cache_sprites[nombre]
    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{nombre}"
        datos = requests.get(url, timeout=5).json()
        img_url = datos["sprites"]["front_default"]
        if img_url is None:
            raise ValueError("Sin sprite")
        img_bytes = requests.get(img_url, timeout=5).content
        sprite = pygame.image.load(io.BytesIO(img_bytes)).convert_alpha()
        sprite = pygame.transform.scale(sprite, (96, 96))
        _cache_sprites[nombre] = sprite
        return sprite
    except Exception:
        # Si falla la descarga, devolvemos None (se mostrará un placeholder)
        _cache_sprites[nombre] = None
        return None

def placeholder_sprite(sup, cx, cy):
    """Dibuja un cuadrado punteado como placeholder si no hay sprite."""
    r = pygame.Rect(cx - 48, cy - 48, 96, 96)
    pygame.draw.rect(sup, (50, 60, 90), r, border_radius=8)
    pygame.draw.rect(sup, COLOR_BORDE, r, 2, border_radius=8)

# ─────────────────────────────────────────────
#  CLASE BOTÓN
# ─────────────────────────────────────────────
class Boton:
    def __init__(self, rect, texto, fuente, tag=None):
        self.rect   = pygame.Rect(rect)
        self.texto  = texto
        self.fuente = fuente
        self.tag    = tag          # dato asociado (nombre del pokemon, atributo, etc.)
        self.hover  = False
        self.activo = False        # está seleccionado

    def dibujar(self, sup):
        if self.activo:
            color_fondo  = COLOR_BOTON_SEL
            color_texto  = (20, 20, 20)
            color_borde  = COLOR_BOTON_SEL
        elif self.hover:
            color_fondo  = COLOR_BOTON_HOV
            color_texto  = COLOR_TEXTO
            color_borde  = COLOR_BORDE
        else:
            color_fondo  = COLOR_BOTON
            color_texto  = COLOR_TEXTO
            color_borde  = COLOR_BORDE

        dibujar_panel(sup, self.rect, color_fondo, radio=8, borde=color_borde)
        tx = self.rect.centerx
        ty = self.rect.centery - self.fuente.get_height() // 2
        dibujar_texto(sup, self.texto, self.fuente, color_texto, tx, ty, centrado=True)

    def actualizar_hover(self, pos):
        self.hover = self.rect.collidepoint(pos)

    def fue_clickeado(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            return self.rect.collidepoint(evento.pos)
        return False

# ─────────────────────────────────────────────
#  PANTALLA DE SELECCIÓN
# ─────────────────────────────────────────────

CATEGORIAS = ["Novatos", "Medios", "Altos"]

LISTA_POKEMONES = {
    "Novatos": ["dragonite", "tyranitar", "metagross", "arcanine"],
    "Medios":  ["vaporeon",  "jolteon",   "pikachu",   "eevee"],
    "Altos":   ["psyduck",   "charmander","charizard",  "rattata"],
}

ATRIBUTOS = ["ataque", "velocidad", "defensa", "adaptabilidad"]
PARES_ATRIBUTOS = {
    "ataque":        "velocidad",
    "velocidad":     "ataque",
    "defensa":       "adaptabilidad",
    "adaptabilidad": "defensa",
}
COLOR_ATRIBUTOS = {
    "ataque":        COLOR_ATK,
    "velocidad":     COLOR_SPD,
    "defensa":       COLOR_DEF,
    "adaptabilidad": COLOR_ADP,
}


def pantalla_seleccion(pantalla, pokemones_obj):
    """
    Muestra la pantalla de selección de pokemones.

    Parámetros:
        pantalla : pygame.Surface  — superficie principal
        pokemones_obj : dict       — {"Novatos": [Obj,...], "Medios": [...], "Altos": [...]}
                                     (objetos Pokemon ya creados con sus stats en rango)

    Retorna:
        list de objetos Pokemon con el atributo ya modificado,
        o None si el usuario cerró la ventana.
    """
    clock = pygame.time.Clock()

    # ── Fuentes ──
    fuente_titulo  = pygame.font.SysFont("Arial", 26, bold=True)
    fuente_cat     = pygame.font.SysFont("Arial", 20, bold=True)
    fuente_normal  = pygame.font.SysFont("Arial", 16)
    fuente_pequeña = pygame.font.SysFont("Arial", 13)
    fuente_boton   = pygame.font.SysFont("Arial", 15, bold=True)

    # ── Estado de la pantalla ──
    paso_actual   = 0          # 0,1,2 → qué categoría estamos eligiendo
    selecciones   = {}         # {"Novatos": obj_pokemon, ...}
    atrib_sel     = {}         # {"Novatos": "ataque", ...}
    sprites_cache = {}         # nombre → Surface o None

    # Precargamos sprites (en hilo principal para no complicar)
    def cargar_sprite_si_falta(nombre):
        if nombre not in sprites_cache:
            sprites_cache[nombre] = obtener_sprite(nombre)

    # ── Construir botones de pokemones para cada categoría ──
    #    Fila de 4 tarjetas centradas horizontalmente
    CARD_W, CARD_H = 200, 50
    CARD_GAP       = 15
    total_w        = 4 * CARD_W + 3 * CARD_GAP
    start_x        = (ANCHO - total_w) // 2

    botones_pokemones = {}   # cat → [Boton, ...]
    for cat in CATEGORIAS:
        bots = []
        for i, nombre in enumerate(LISTA_POKEMONES[cat]):
            rx = start_x + i * (CARD_W + CARD_GAP)
            ry = 220
            bots.append(Boton((rx, ry, CARD_W, CARD_H), nombre.capitalize(), fuente_boton, tag=nombre))
        botones_pokemones[cat] = bots

    # ── Botones de atributo ──
    ATR_W, ATR_H = 200, 44
    ATR_GAP      = 12
    total_atr_w  = 4 * ATR_W + 3 * ATR_GAP
    atr_start_x  = (ANCHO - total_atr_w) // 2

    botones_atributos = []
    for i, atr in enumerate(ATRIBUTOS):
        rx = atr_start_x + i * (ATR_W + ATR_GAP)
        botones_atributos.append(Boton((rx, 490, ATR_W, ATR_H), atr.capitalize(), fuente_boton, tag=atr))

    # ── Botón Confirmar ──
    btn_confirmar = Boton((ANCHO // 2 - 100, 570, 200, 46), "Confirmar →", fuente_boton)

    # ── Sprite actual ──
    sprite_actual   = None
    pokemon_hoverd  = None   # nombre sobre el que está el mouse

    # ──────────────────────────────────────────
    #  LOOP PRINCIPAL
    # ──────────────────────────────────────────
    corriendo = True
    while corriendo:
        cat = CATEGORIAS[paso_actual]
        poke_sel_actual  = selecciones.get(cat)     # objeto Pokemon o None
        atrib_sel_actual = atrib_sel.get(cat)        # str o None

        mouse_pos = pygame.mouse.get_pos()

        # ── Eventos ──────────────────────────
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return None

            # Clicks en tarjetas de pokemon
            for bot in botones_pokemones[cat]:
                bot.actualizar_hover(mouse_pos)
                if bot.fue_clickeado(evento):
                    # Deseleccionar todos y seleccionar este
                    for b in botones_pokemones[cat]:
                        b.activo = False
                    bot.activo = True
                    # Buscar el objeto Pokemon correspondiente
                    for obj in pokemones_obj[cat]:
                        if obj.nombre.lower() == bot.tag:
                            selecciones[cat] = obj
                            atrib_sel.pop(cat, None)  # resetear atributo si cambia pokemon
                            for ab in botones_atributos:
                                ab.activo = False
                            break
                    # Cargar sprite
                    cargar_sprite_si_falta(bot.tag)
                    sprite_actual = sprites_cache.get(bot.tag)

            # Clicks en atributos (solo si ya eligió pokemon)
            if poke_sel_actual is not None:
                for bot in botones_atributos:
                    bot.actualizar_hover(mouse_pos)
                    if bot.fue_clickeado(evento):
                        for b in botones_atributos:
                            b.activo = False
                        bot.activo = True
                        atrib_sel[cat] = bot.tag

            # Confirmar
            btn_confirmar.actualizar_hover(mouse_pos)
            puede_confirmar = (poke_sel_actual is not None and atrib_sel_actual is not None)
            if puede_confirmar and btn_confirmar.fue_clickeado(evento):
                if paso_actual < 2:
                    paso_actual += 1
                    # Limpiar botones para la nueva categoría
                    for b in botones_pokemones[CATEGORIAS[paso_actual]]:
                        b.activo = False
                    for b in botones_atributos:
                        b.activo = False
                    sprite_actual = None
                else:
                    # ── Aplicar cambios de atributo y devolver equipo ──
                    equipo_final = []
                    for c in CATEGORIAS:
                        poke = selecciones[c]
                        atr1 = atrib_sel[c]
                        atr2 = PARES_ATRIBUTOS[atr1]
                        poke.cambiar_atributo(atr1, atr2, 0.15, print_cambios=False)
                        equipo_final.append(poke)
                    return equipo_final

        # ── Actualizar hover sprite ──
        hoverd = None
        for bot in botones_pokemones[cat]:
            if bot.hover:
                hoverd = bot.tag
                if hoverd not in sprites_cache:
                    cargar_sprite_si_falta(hoverd)
        pokemon_hoverd = hoverd

        # ── DIBUJO ───────────────────────────
        pantalla.fill(COLOR_FONDO)

        # Título principal
        dibujar_texto(pantalla, "⚔  Armá tu equipo", fuente_titulo, COLOR_TEXTO, ANCHO // 2, 18, centrado=True)

        # Indicador de pasos
        for i, c in enumerate(CATEGORIAS):
            cx = 200 + i * 350
            completado = c in selecciones and c in atrib_sel
            actual     = i == paso_actual
            color_c    = COLOR_BORDE_SEL if actual else (COLOR_TITULO_CAT[c] if completado else COLOR_SUBTEXTO)
            marca      = "✓ " if completado and not actual else ""
            dibujar_texto(pantalla, f"{marca}{c}", fuente_cat, color_c, cx, 60, centrado=True)
            # línea indicadora
            if actual:
                pygame.draw.rect(pantalla, COLOR_BORDE_SEL, (cx - 40, 82, 80, 3), border_radius=2)

        # Panel central
        panel_rect = pygame.Rect(30, 100, ANCHO - 60, ALTO - 120)
        dibujar_panel(pantalla, panel_rect, COLOR_PANEL, radio=14, borde=COLOR_BORDE, grosor_borde=1)

        # ── Título de categoría ──
        color_cat = COLOR_TITULO_CAT[cat]
        dibujar_texto(pantalla, f"Categoría: {cat}", fuente_cat, color_cat, ANCHO // 2, 115, centrado=True)
        dibujar_texto(pantalla, "Elegí tu pokémon:", fuente_normal, COLOR_SUBTEXTO, ANCHO // 2, 140, centrado=True)

        # ── Tarjetas de pokemones ──
        for bot in botones_pokemones[cat]:
            bot.dibujar(pantalla)

        # ── Sprite + stats del pokemon seleccionado ──
        poke_mostrar = None
        if poke_sel_actual:
            poke_mostrar = poke_sel_actual
        elif pokemon_hoverd:
            for obj in pokemones_obj[cat]:
                if obj.nombre.lower() == pokemon_hoverd:
                    poke_mostrar = obj
                    break

        if poke_mostrar:
            # Panel de info — altura aumentada para que no se solapen los stats
            info_rect = pygame.Rect(ANCHO // 2 - 250, 275, 500, 165)
            dibujar_panel(pantalla, info_rect, (20, 30, 55), radio=10,
                          borde=COLOR_BORDE_SEL if poke_mostrar == poke_sel_actual else COLOR_BORDE)

            # Sprite
            spr = sprites_cache.get(poke_mostrar.nombre.lower())
            sprite_x = info_rect.x + 14
            sprite_cy = info_rect.centery
            if spr:
                pantalla.blit(spr, (sprite_x, sprite_cy - 48))
            else:
                placeholder_sprite(pantalla, sprite_x + 48, sprite_cy)

            # Nombre y tipo
            tx = sprite_x + 106
            dibujar_texto(pantalla, poke_mostrar.nombre.capitalize(), fuente_cat, COLOR_TEXTO, tx, info_rect.y + 10)
            dibujar_texto(pantalla, f"Tipo: {poke_mostrar.tipo}", fuente_pequeña, color_cat, tx, info_rect.y + 34)

            # Barras de stats — dos columnas con ancho reducido (110px) para que el valor no invada la columna vecina
            # Columna izquierda: ATK y DEF  |  Columna derecha: SPD y ADP
            # Separación vertical entre filas: 28px (antes 25) para evitar solapamiento
            max_val = 2.0
            BAR_W   = 110
            COL2_X  = tx + 185   # inicio de la segunda columna

            barra_stat(pantalla, tx,     info_rect.y + 62,  BAR_W, poke_mostrar.ataque,       max_val, COLOR_ATK, fuente_pequeña, "ATK")
            barra_stat(pantalla, tx,     info_rect.y + 92,  BAR_W, poke_mostrar.defensa,       max_val, COLOR_DEF, fuente_pequeña, "DEF")
            barra_stat(pantalla, COL2_X, info_rect.y + 62,  BAR_W, poke_mostrar.velocidad,     max_val, COLOR_SPD, fuente_pequeña, "SPD")
            barra_stat(pantalla, COL2_X, info_rect.y + 92,  BAR_W, poke_mostrar.adaptabilidad, max_val, COLOR_ADP, fuente_pequeña, "ADP")

            # Vida
            dibujar_texto(pantalla, f"HP: {poke_mostrar.vida}  |  Sp.Atk: {poke_mostrar.special_attack}",
                          fuente_pequeña, COLOR_SUBTEXTO, tx, info_rect.y + 128)

        else:
            # Placeholder "pasá el mouse"
            dibujar_texto(pantalla, "Pasá el mouse por un pokémon para ver sus stats",
                          fuente_normal, COLOR_SUBTEXTO, ANCHO // 2, 360, centrado=True)

        # ── Sección de atributo ──
        if poke_sel_actual is not None:
            atrib_y = 455
            dibujar_texto(pantalla, "Mejorá un atributo  (el par opuesto bajará un poco):",
                          fuente_normal, COLOR_SUBTEXTO, ANCHO // 2, atrib_y, centrado=True)
            for bot in botones_atributos:
                # Color especial por atributo
                if not bot.activo and not bot.hover:
                    bot_color = COLOR_ATRIBUTOS.get(bot.tag, COLOR_BOTON)
                    # Versión oscurecida del color
                    r, g, b = bot_color
                    bot_color_dark = (max(0, r - 100), max(0, g - 100), max(0, b - 100))
                    pygame.draw.rect(pantalla, bot_color_dark, bot.rect, border_radius=8)
                    pygame.draw.rect(pantalla, bot_color, bot.rect, 2, border_radius=8)
                    tx2 = bot.rect.centerx
                    ty2 = bot.rect.centery - fuente_boton.get_height() // 2
                    dibujar_texto(pantalla, bot.texto, fuente_boton, bot_color, tx2, ty2, centrado=True)
                else:
                    bot.dibujar(pantalla)

            # Mostrar el par afectado
            if atrib_sel_actual:
                par = PARES_ATRIBUTOS[atrib_sel_actual]
                msg = f"↑ {atrib_sel_actual.capitalize()} +0.15   |   ↓ {par.capitalize()} -0.15"
                dibujar_texto(pantalla, msg, fuente_pequeña, COLOR_SUBTEXTO, ANCHO // 2, 540, centrado=True)

        # ── Botón Confirmar ──
        puede_confirmar = (poke_sel_actual is not None and atrib_sel_actual is not None)
        if puede_confirmar:
            label = "Confirmar →" if paso_actual < 2 else "¡Iniciar batalla! →"
            btn_confirmar.texto = label
            btn_confirmar.dibujar(pantalla)
        else:
            # Versión deshabilitada
            dibujar_panel(pantalla, btn_confirmar.rect, (30, 40, 60), radio=8, borde=(50, 60, 90))
            dibujar_texto(pantalla, btn_confirmar.texto, fuente_boton, (60, 70, 100),
                          btn_confirmar.rect.centerx, btn_confirmar.rect.centery - fuente_boton.get_height() // 2,
                          centrado=True)

        pygame.display.flip()
        clock.tick(60)

    return None


# ─────────────────────────────────────────────
#  PANTALLA: ELEGIR POKEMON INICIAL
# ─────────────────────────────────────────────

def pantalla_elegir_inicial(pantalla, equipo_usu, ambiente):
    """
    Muestra el ambiente elegido y deja al jugador elegir con qué pokémon empezar.
    Retorna el objeto Pokemon elegido o None si se cierra la ventana.
    """
    clock = pygame.time.Clock()
    fuente_titulo  = pygame.font.SysFont("Arial", 26, bold=True)
    fuente_cat     = pygame.font.SysFont("Arial", 20, bold=True)
    fuente_normal  = pygame.font.SysFont("Arial", 16)
    fuente_pequeña = pygame.font.SysFont("Arial", 13)
    fuente_boton   = pygame.font.SysFont("Arial", 15, bold=True)

    COLOR_AMB = {
        "water":    (80,  180, 255),
        "ground":   (180, 140,  60),
        "electric": (255, 210,  40),
        "fire":     (255, 100,  40),
    }
    color_amb = COLOR_AMB.get(ambiente.tipo_ambiente, COLOR_SUBTEXTO)

    # Botones con los 3 pokemones del equipo
    CARD_W, CARD_H = 200, 54
    total_w = len(equipo_usu) * CARD_W + (len(equipo_usu) - 1) * 20
    sx = (ANCHO - total_w) // 2
    botones = []
    for i, pok in enumerate(equipo_usu):
        b = Boton((sx + i * (CARD_W + 20), 380, CARD_W, CARD_H),
                  pok.nombre.capitalize(), fuente_boton, tag=pok)
        botones.append(b)

    sprites_cache = {}
    for pok in equipo_usu:
        sprites_cache[pok.nombre.lower()] = obtener_sprite(pok.nombre)

    seleccion = None
    btn_ok = Boton((ANCHO // 2 - 110, 490, 220, 46), "¡A pelear! →", fuente_boton)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return None
            for b in botones:
                b.actualizar_hover(mouse_pos)
                if b.fue_clickeado(evento):
                    for bb in botones:
                        bb.activo = False
                    b.activo = True
                    seleccion = b.tag
            btn_ok.actualizar_hover(mouse_pos)
            if seleccion and btn_ok.fue_clickeado(evento):
                return seleccion

        pantalla.fill(COLOR_FONDO)

        # Título
        dibujar_texto(pantalla, "¡Comienza la batalla!", fuente_titulo, COLOR_TEXTO, ANCHO // 2, 30, centrado=True)

        # Panel de ambiente
        amb_rect = pygame.Rect(ANCHO // 2 - 280, 80, 560, 110)
        dibujar_panel(pantalla, amb_rect, COLOR_PANEL, radio=12, borde=color_amb)
        dibujar_texto(pantalla, f"Ambiente: {ambiente.nombre.capitalize()}", fuente_cat, color_amb,
                      ANCHO // 2, 95, centrado=True)
        dibujar_texto(pantalla, f"Tipo: {ambiente.tipo_ambiente}   |   "
                      f"ATK {ambiente.ataque:+.2f}  |  DEF {ambiente.defensa:+.2f}  |  SPD {ambiente.velocidad:+.2f}",
                      fuente_normal, COLOR_SUBTEXTO, ANCHO // 2, 128, centrado=True)

        # Estadísticas actualizadas del equipo
        dibujar_texto(pantalla, "Tu equipo adaptado al ambiente:", fuente_normal,
                      COLOR_SUBTEXTO, ANCHO // 2, 210, centrado=True)

        PANEL_W = 230
        total_panels = len(equipo_usu) * PANEL_W + (len(equipo_usu) - 1) * 20
        px0 = (ANCHO - total_panels) // 2
        for i, pok in enumerate(equipo_usu):
            pr = pygame.Rect(px0 + i * (PANEL_W + 20), 235, PANEL_W, 100)
            dibujar_panel(pantalla, pr, (20, 30, 55), radio=8, borde=COLOR_BORDE)
            spr = sprites_cache.get(pok.nombre.lower())
            if spr:
                spr_s = pygame.transform.scale(spr, (64, 64))
                pantalla.blit(spr_s, (pr.x + 6, pr.y + 18))
            dibujar_texto(pantalla, pok.nombre.capitalize(), fuente_cat, COLOR_TEXTO, pr.x + 76, pr.y + 8)
            barra_stat(pantalla, pr.x + 76, pr.y + 32, 80, pok.ataque,       2.0, COLOR_ATK, fuente_pequeña, "ATK")
            barra_stat(pantalla, pr.x + 76, pr.y + 52, 80, pok.defensa,      2.0, COLOR_DEF, fuente_pequeña, "DEF")
            barra_stat(pantalla, pr.x + 76, pr.y + 72, 80, pok.velocidad,    2.0, COLOR_SPD, fuente_pequeña, "SPD")

        dibujar_texto(pantalla, "Elegí tu primer pokémon:", fuente_cat, COLOR_TEXTO, ANCHO // 2, 345, centrado=True)
        for b in botones:
            b.dibujar(pantalla)

        if seleccion:
            btn_ok.dibujar(pantalla)

        pygame.display.flip()
        clock.tick(60)


# ─────────────────────────────────────────────
#  PANTALLA DE BATALLA
# ─────────────────────────────────────────────

ACCIONES_BASE     = ["atacar", "defender", "esquivar"]
ACCIONES_ESPECIAL = ["atacar", "defender", "esquivar", "especial"]

COLOR_ACCION = {
    "atacar":   (255,  90,  80),
    "defender": ( 80, 180, 255),
    "esquivar": (100, 230, 100),
    "especial": (255, 210,  40),
}

ETIQUETA_ACCION = {
    "atacar":   "⚔ Atacar",
    "defender": "🛡 Defender",
    "esquivar": "💨 Esquivar",
    "especial": "✨ Especial",
}

MAX_LOG = 7   # líneas visibles en el log de batalla


def _barra_vida(sup, x, y, ancho, vida_actual, vida_max, fuente_p, nombre, invertido=False):
    """Dibuja la barra de vida de un pokémon con nombre y valores."""
    ratio = max(0.0, vida_actual / vida_max)
    if ratio > 0.5:
        col = (80, 220, 80)
    elif ratio > 0.25:
        col = (255, 200, 40)
    else:
        col = (255, 60, 60)

    # Si está invertido (CPU) el nombre va a la derecha
    if invertido:
        txt = fuente_p.render(f"{nombre.capitalize()}  HP: {vida_actual:.1f}/{vida_max}", True, COLOR_TEXTO)
        sup.blit(txt, (x + ancho - txt.get_width(), y - 18))
    else:
        dibujar_texto(sup, f"{nombre.capitalize()}  HP: {vida_actual:.1f}/{vida_max}", fuente_p, COLOR_TEXTO, x, y - 18)

    bg = pygame.Rect(x, y, ancho, 14)
    pygame.draw.rect(sup, (50, 60, 90), bg, border_radius=7)
    fill_w = int(ratio * ancho)
    if fill_w > 0:
        pygame.draw.rect(sup, col, (x, y, fill_w, 14), border_radius=7)
    pygame.draw.rect(sup, COLOR_BORDE, bg, 1, border_radius=7)


def pantalla_batalla(pantalla, poke_usu, poke_compu, equipo_usu_restante,
                     eventos_random, puntos_usu, puntos_compu):
    """
    Corre UNA ronda completa de batalla (hasta que el jugador elige acción y se resuelve).
    También gestiona la espera cuando un pokémon cae y hay que elegir el siguiente.

    Retorna un dict con el estado actualizado:
    {
      "poke_usu": obj,
      "poke_compu": obj,
      "puntos_usu": int,
      "puntos_compu": int,
      "dict_usu": dict,
      "dict_cpu": dict,
      "log": [str, ...],           ← mensajes nuevos de esta ronda
      "usu_murio": bool,
      "compu_murio": bool,
      "cerrado": bool,             ← True si el jugador cerró la ventana
    }
    """
    import random

    clock = pygame.time.Clock()
    fuente_titulo  = pygame.font.SysFont("Arial", 24, bold=True)
    fuente_cat     = pygame.font.SysFont("Arial", 18, bold=True)
    fuente_normal  = pygame.font.SysFont("Arial", 15)
    fuente_pequeña = pygame.font.SysFont("Arial", 13)
    fuente_boton   = pygame.font.SysFont("Arial", 14, bold=True)
    fuente_log     = pygame.font.SysFont("Courier", 13)

    sprites_cache = {
        poke_usu.nombre.lower():    obtener_sprite(poke_usu.nombre),
        poke_compu.nombre.lower():  obtener_sprite(poke_compu.nombre),
    }

    # Botones de acción
    acciones = ACCIONES_ESPECIAL if puntos_usu >= 3 else ACCIONES_BASE
    BTN_W, BTN_H = 190, 48
    BTN_GAP = 14
    total_btns_w = len(acciones) * BTN_W + (len(acciones) - 1) * BTN_GAP
    bx0 = (ANCHO - total_btns_w) // 2
    botones_accion = []
    for i, acc in enumerate(acciones):
        b = Boton((bx0 + i * (BTN_W + BTN_GAP), 570, BTN_W, BTN_H),
                  ETIQUETA_ACCION[acc], fuente_boton, tag=acc)
        botones_accion.append(b)

    log_batalla = []    # mensajes de esta ronda
    accion_elegida = None
    resultado = None    # se completa cuando el jugador confirma acción

    while resultado is None:
        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return {"cerrado": True}

            for b in botones_accion:
                b.actualizar_hover(mouse_pos)
                if b.fue_clickeado(evento):
                    # Resolver la ronda con la acción elegida
                    accion_elegida = b.tag
                    log_batalla, nuevo_usu, nuevo_compu, ptu, ptc = \
                        _resolver_ronda(poke_usu, poke_compu, accion_elegida,
                                        eventos_random, puntos_usu, puntos_compu)
                    resultado = {
                        "poke_usu":    nuevo_usu,
                        "poke_compu":  nuevo_compu,
                        "puntos_usu":  ptu,
                        "puntos_compu": ptc,
                        "log":         log_batalla,
                        "usu_murio":   nuevo_usu.vida <= 0,
                        "compu_murio": nuevo_compu.vida <= 0,
                        "cerrado":     False,
                    }

        # ── DIBUJO ──
        pantalla.fill(COLOR_FONDO)

        # Título de la batalla
        dibujar_texto(pantalla, "⚔  Batalla Pokémon", fuente_titulo, COLOR_TEXTO,
                      ANCHO // 2, 14, centrado=True)

        # Área de combate
        area_rect = pygame.Rect(20, 45, ANCHO - 40, 380)
        dibujar_panel(pantalla, area_rect, (18, 26, 50), radio=12, borde=COLOR_BORDE, grosor_borde=1)

        # ── Sprite y vida del JUGADOR (izquierda) ──
        spr_usu = sprites_cache.get(poke_usu.nombre.lower())
        if spr_usu:
            spr_big = pygame.transform.scale(spr_usu, (128, 128))
            pantalla.blit(spr_big, (50, 130))
        else:
            placeholder_sprite(pantalla, 114, 194)

        _barra_vida(pantalla, 40, 90, 260, poke_usu.vida, 5, fuente_normal,
                    poke_usu.nombre, invertido=False)

        # Mini stats jugador
        barra_stat(pantalla, 40, 245, 80, poke_usu.ataque,      2.0, COLOR_ATK, fuente_pequeña, "ATK")
        barra_stat(pantalla, 40, 265, 80, poke_usu.defensa,     2.0, COLOR_DEF, fuente_pequeña, "DEF")
        barra_stat(pantalla, 40, 285, 80, poke_usu.velocidad,   2.0, COLOR_SPD, fuente_pequeña, "SPD")

        # Racha de puntos del jugador
        dibujar_texto(pantalla, f"Racha: {puntos_usu}/3", fuente_pequeña,
                      COLOR_BORDE_SEL if puntos_usu >= 3 else COLOR_SUBTEXTO, 40, 310)
        if puntos_usu >= 3:
            dibujar_texto(pantalla, "¡ESPECIAL DISPONIBLE!", fuente_pequeña, COLOR_BORDE_SEL, 40, 328)

        # ── Sprite y vida de la CPU (derecha) ──
        spr_cpu = sprites_cache.get(poke_compu.nombre.lower())
        if spr_cpu:
            spr_cpu_big = pygame.transform.scale(spr_cpu, (128, 128))
            spr_cpu_flip = pygame.transform.flip(spr_cpu_big, True, False)
            pantalla.blit(spr_cpu_flip, (ANCHO - 180, 130))
        else:
            placeholder_sprite(pantalla, ANCHO - 114, 194)

        _barra_vida(pantalla, ANCHO - 300, 90, 260, poke_compu.vida, 5, fuente_normal,
                    poke_compu.nombre, invertido=True)

        barra_stat(pantalla, ANCHO - 180, 245, 80, poke_compu.ataque,    2.0, COLOR_ATK, fuente_pequeña, "ATK")
        barra_stat(pantalla, ANCHO - 180, 265, 80, poke_compu.defensa,   2.0, COLOR_DEF, fuente_pequeña, "DEF")
        barra_stat(pantalla, ANCHO - 180, 285, 80, poke_compu.velocidad, 2.0, COLOR_SPD, fuente_pequeña, "SPD")
        dibujar_texto(pantalla, f"Racha CPU: {puntos_compu}/3", fuente_pequeña, COLOR_SUBTEXTO,
                      ANCHO - 180, 310)

        # ── VS central ──
        dibujar_texto(pantalla, "VS", fuente_titulo, COLOR_BORDE_SEL, ANCHO // 2, 185, centrado=True)

        # ── Log de combate ──
        log_rect = pygame.Rect(220, 430, ANCHO - 440, 130)
        dibujar_panel(pantalla, log_rect, (15, 22, 45), radio=8, borde=(50, 70, 120))
        dibujar_texto(pantalla, "Log de batalla", fuente_pequeña, COLOR_SUBTEXTO,
                      log_rect.x + 8, log_rect.y + 4)
        # Solo mostramos MAX_LOG líneas (las más recientes)
        lineas_vis = log_batalla[-MAX_LOG:] if len(log_batalla) > MAX_LOG else log_batalla
        for j, linea in enumerate(lineas_vis):
            col_log = COLOR_BORDE_SEL if "murió" in linea or "especial" in linea.lower() else COLOR_TEXTO
            dibujar_texto(pantalla, linea, fuente_log, col_log,
                          log_rect.x + 8, log_rect.y + 20 + j * 16)

        # ── Botones de acción (si aún no se eligió acción) ──
        if resultado is None:
            dibujar_texto(pantalla, "¿Qué hacés?", fuente_cat, COLOR_SUBTEXTO,
                          ANCHO // 2, 548, centrado=True)
            for b in botones_accion:
                # Colores por tipo de acción
                if not b.activo and not b.hover:
                    col_b = COLOR_ACCION.get(b.tag, COLOR_BOTON)
                    r, g, bl = col_b
                    dark = (max(0, r - 110), max(0, g - 110), max(0, bl - 110))
                    pygame.draw.rect(pantalla, dark, b.rect, border_radius=8)
                    pygame.draw.rect(pantalla, col_b, b.rect, 2, border_radius=8)
                    dibujar_texto(pantalla, b.texto, fuente_boton, col_b,
                                  b.rect.centerx, b.rect.centery - fuente_boton.get_height() // 2,
                                  centrado=True)
                else:
                    b.dibujar(pantalla)

        pygame.display.flip()
        clock.tick(60)

    # Mostrar resultado de la ronda brevemente antes de retornar
    _mostrar_resultado_ronda(pantalla, resultado, fuente_titulo, fuente_cat, fuente_normal, fuente_log)

    return resultado


def _resolver_ronda(poke_usu, poke_compu, accion_usu, eventos_random, puntos_usu, puntos_compu):
    """
    Implementa la misma lógica que funciones.ronda() pero sin input() ni print().
    Retorna (log:list, poke_usu, poke_compu, puntos_usu, puntos_compu).
    Trabaja sobre copias de vida (no modifica los objetos originales hasta devolver).
    """
    import random, copy

    log = []

    # La CPU elige su acción
    if puntos_compu >= 3:
        accion_cpu = random.choice(ACCIONES_ESPECIAL)
    else:
        accion_cpu = random.choice(ACCIONES_BASE)

    log.append(f"CPU eligió: {accion_cpu.upper()}")

    # Eventos aleatorios (solo si ninguno usa especial)
    if accion_usu != "especial" and accion_cpu != "especial":
        if random.choice([True, False]):
            ev = random.choice(eventos_random)
            afectado = random.choice([poke_usu, poke_compu])
            afectado.vida += ev.vida
            afectado.vida = round(max(0, afectado.vida), 1)
            quien = "Tu " + afectado.nombre if afectado is poke_usu else "CPU " + afectado.nombre
            signo = "+" if ev.vida > 0 else ""
            log.append(f"Evento: {quien} recibió {ev.nombre} (vida {signo}{ev.vida}) → HP:{afectado.vida}")
            if afectado.vida <= 0:
                return log, poke_usu, poke_compu, puntos_usu, puntos_compu

    # ── Resolver acciones ──
    if accion_usu == "especial" and accion_cpu != "especial":
        dano = round(poke_usu.ataque * (poke_usu.special_attack + 1), 1)
        poke_compu.vida = round(max(0, poke_compu.vida - dano), 1)
        puntos_usu = 0
        if poke_compu.vida <= 0:
            log.append(f"✨ Tu {poke_usu.nombre} usó ESPECIAL → ¡{poke_compu.nombre} murió!")
        else:
            log.append(f"✨ Tu {poke_usu.nombre} usó ESPECIAL → {poke_compu.nombre} HP:{poke_compu.vida}")
            puntos_usu += 1

    elif accion_cpu == "especial" and accion_usu != "especial":
        dano = round(poke_compu.ataque * (poke_compu.special_attack + 1), 1)
        poke_usu.vida = round(max(0, poke_usu.vida - dano), 1)
        puntos_compu = 0
        if poke_usu.vida <= 0:
            log.append(f"✨ CPU {poke_compu.nombre} usó ESPECIAL → ¡Tu {poke_usu.nombre} murió!")
        else:
            log.append(f"✨ CPU {poke_compu.nombre} usó ESPECIAL → tu {poke_usu.nombre} HP:{poke_usu.vida}")
            puntos_compu += 1

    elif accion_usu == "especial" and accion_cpu == "especial":
        d1 = round(poke_usu.ataque  * (poke_usu.special_attack  + 1), 1)
        d2 = round(poke_compu.ataque * (poke_compu.special_attack + 1), 1)
        poke_compu.vida = round(max(0, poke_compu.vida - d1), 1)
        poke_usu.vida   = round(max(0, poke_usu.vida   - d2), 1)
        puntos_usu = puntos_compu = 0
        log.append(f"✨ ¡Doble ESPECIAL! Tu {poke_usu.nombre} HP:{poke_usu.vida}  |  CPU {poke_compu.nombre} HP:{poke_compu.vida}")

    elif accion_usu == "atacar" and accion_cpu == "atacar":
        poke_usu.vida   = round(max(0, poke_usu.vida   - poke_compu.ataque), 1)
        poke_compu.vida = round(max(0, poke_compu.vida - poke_usu.ataque),   1)
        puntos_usu   += 1
        puntos_compu += 1
        log.append(f"⚔ Ambos atacan → Tu {poke_usu.nombre} HP:{poke_usu.vida}  |  CPU {poke_compu.nombre} HP:{poke_compu.vida}")

    elif accion_usu in ("esquivar", "defender") and accion_cpu in ("esquivar", "defender"):
        log.append("🛡 Ninguno atacó. Sin cambios en HP.")

    elif accion_usu == "atacar" and accion_cpu == "defender":
        dano = round(poke_usu.ataque * poke_compu.defensa, 1)
        poke_compu.vida = round(max(0, poke_compu.vida - dano), 1)
        if poke_compu.vida <= 0:
            log.append(f"⚔ Tu {poke_usu.nombre} atacó → ¡{poke_compu.nombre} murió!")
        else:
            puntos_usu += 1
            log.append(f"⚔ Tu {poke_usu.nombre} atacó (defensa CPU activa) → {poke_compu.nombre} HP:{poke_compu.vida}")

    elif accion_usu == "atacar" and accion_cpu == "esquivar":
        esquiva = random.choices([True, False],
                                 weights=[poke_compu.velocidad, max(0.01, 1 - poke_compu.velocidad)])[0]
        if esquiva:
            log.append(f"💨 CPU {poke_compu.nombre} esquivó el ataque de tu {poke_usu.nombre}.")
        else:
            poke_compu.vida = round(max(0, poke_compu.vida - poke_usu.ataque), 1)
            if poke_compu.vida <= 0:
                log.append(f"⚔ No esquivó → ¡{poke_compu.nombre} murió!")
            else:
                puntos_usu += 1
                log.append(f"⚔ No esquivó → {poke_compu.nombre} HP:{poke_compu.vida}")

    elif accion_usu == "defender" and accion_cpu == "atacar":
        dano = round(poke_compu.ataque * poke_usu.defensa, 1)
        poke_usu.vida = round(max(0, poke_usu.vida - dano), 1)
        if poke_usu.vida <= 0:
            log.append(f"🛡 Tu {poke_usu.nombre} se defendió pero murió.")
        else:
            puntos_compu += 1
            log.append(f"🛡 Tu {poke_usu.nombre} se defendió → HP:{poke_usu.vida}")

    elif accion_usu == "esquivar" and accion_cpu == "atacar":
        esquiva = random.choices([True, False],
                                 weights=[poke_usu.velocidad, max(0.01, 1 - poke_usu.velocidad)])[0]
        if esquiva:
            log.append(f"💨 Tu {poke_usu.nombre} esquivó el ataque de CPU {poke_compu.nombre}.")
        else:
            poke_usu.vida = round(max(0, poke_usu.vida - poke_compu.ataque), 1)
            if poke_usu.vida <= 0:
                log.append(f"⚔ No esquivaste → ¡Tu {poke_usu.nombre} murió!")
            else:
                puntos_compu += 1
                log.append(f"⚔ No esquivaste → tu {poke_usu.nombre} HP:{poke_usu.vida}")

    return log, poke_usu, poke_compu, puntos_usu, puntos_compu


def _mostrar_resultado_ronda(pantalla, resultado, fuente_titulo, fuente_cat, fuente_normal, fuente_log):
    """Muestra brevemente el resultado de la ronda (1.5 s) si alguien murió."""
    if not (resultado.get("usu_murio") or resultado.get("compu_murio")):
        return   # si nadie murió, no hace falta pausa extra

    clock = pygame.time.Clock()
    inicio = pygame.time.get_ticks()
    while pygame.time.get_ticks() - inicio < 1800:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return
            if ev.type == pygame.KEYDOWN or ev.type == pygame.MOUSEBUTTONDOWN:
                return   # saltar con cualquier tecla/clic

        pantalla.fill(COLOR_FONDO)
        if resultado.get("usu_murio") and resultado.get("compu_murio"):
            msg = "¡Los dos cayeron!"
            color = COLOR_BORDE
        elif resultado.get("usu_murio"):
            msg = f"💀 ¡Tu {resultado['poke_usu'].nombre.capitalize()} cayó!"
            color = (255, 80, 80)
        else:
            msg = f"💀 ¡{resultado['poke_compu'].nombre.capitalize()} de la CPU cayó!"
            color = COLOR_SPD

        dibujar_texto(pantalla, msg, fuente_titulo, color, ANCHO // 2, ALTO // 2 - 20, centrado=True)
        dibujar_texto(pantalla, "Clic o cualquier tecla para continuar...",
                      fuente_normal, COLOR_SUBTEXTO, ANCHO // 2, ALTO // 2 + 30, centrado=True)
        pygame.display.flip()
        clock.tick(60)


# ─────────────────────────────────────────────
#  PANTALLA: ELEGIR SIGUIENTE POKÉMON
# ─────────────────────────────────────────────

def pantalla_elegir_siguiente(pantalla, equipo_disponible):
    """
    Cuando el pokémon actual del jugador muere, permite elegir el siguiente.
    equipo_disponible: lista de objetos Pokemon que aún tienen vida (no incluye al que murió).
    Retorna el Pokemon elegido o None si se cierra la ventana.
    """
    clock = pygame.time.Clock()
    fuente_titulo  = pygame.font.SysFont("Arial", 24, bold=True)
    fuente_cat     = pygame.font.SysFont("Arial", 18, bold=True)
    fuente_normal  = pygame.font.SysFont("Arial", 15)
    fuente_pequeña = pygame.font.SysFont("Arial", 13)
    fuente_boton   = pygame.font.SysFont("Arial", 15, bold=True)

    sprites_cache = {}
    for pok in equipo_disponible:
        sprites_cache[pok.nombre.lower()] = obtener_sprite(pok.nombre)

    CARD_W, CARD_H = 220, 54
    total_w = len(equipo_disponible) * CARD_W + (len(equipo_disponible) - 1) * 20
    sx = (ANCHO - total_w) // 2
    botones = []
    for i, pok in enumerate(equipo_disponible):
        b = Boton((sx + i * (CARD_W + 20), 340, CARD_W, CARD_H),
                  pok.nombre.capitalize(), fuente_boton, tag=pok)
        botones.append(b)

    seleccion = None
    btn_ok = Boton((ANCHO // 2 - 110, 440, 220, 46), "¡A pelear! →", fuente_boton)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return None
            for b in botones:
                b.actualizar_hover(mouse_pos)
                if b.fue_clickeado(evento):
                    for bb in botones:
                        bb.activo = False
                    b.activo = True
                    seleccion = b.tag
            btn_ok.actualizar_hover(mouse_pos)
            if seleccion and btn_ok.fue_clickeado(evento):
                return seleccion

        pantalla.fill(COLOR_FONDO)
        dibujar_texto(pantalla, "💀 ¡Tu pokémon cayó! Elegí el siguiente", fuente_titulo,
                      (255, 90, 90), ANCHO // 2, 50, centrado=True)

        PANEL_W = 260
        total_p = len(equipo_disponible) * PANEL_W + (len(equipo_disponible) - 1) * 20
        px0 = (ANCHO - total_p) // 2
        for i, pok in enumerate(equipo_disponible):
            pr = pygame.Rect(px0 + i * (PANEL_W + 20), 130, PANEL_W, 160)
            dibujar_panel(pantalla, pr, (20, 30, 55), radio=10, borde=COLOR_BORDE)
            spr = sprites_cache.get(pok.nombre.lower())
            if spr:
                spr_s = pygame.transform.scale(spr, (80, 80))
                pantalla.blit(spr_s, (pr.x + 10, pr.y + 40))
            dibujar_texto(pantalla, pok.nombre.capitalize(), fuente_cat, COLOR_TEXTO, pr.x + 100, pr.y + 10)
            barra_stat(pantalla, pr.x + 100, pr.y + 40, 100, pok.ataque,       2.0, COLOR_ATK, fuente_pequeña, "ATK")
            barra_stat(pantalla, pr.x + 100, pr.y + 62, 100, pok.defensa,      2.0, COLOR_DEF, fuente_pequeña, "DEF")
            barra_stat(pantalla, pr.x + 100, pr.y + 84, 100, pok.velocidad,    2.0, COLOR_SPD, fuente_pequeña, "SPD")
            barra_stat(pantalla, pr.x + 100, pr.y + 106, 100, pok.adaptabilidad, 2.0, COLOR_ADP, fuente_pequeña, "ADP")
            dibujar_texto(pantalla, f"HP: {pok.vida:.1f}", fuente_normal, COLOR_SPD, pr.x + 100, pr.y + 132)

        dibujar_texto(pantalla, "Elegí tu próximo pokémon:", fuente_cat, COLOR_SUBTEXTO,
                      ANCHO // 2, 310, centrado=True)
        for b in botones:
            b.dibujar(pantalla)
        if seleccion:
            btn_ok.dibujar(pantalla)

        pygame.display.flip()
        clock.tick(60)


# ─────────────────────────────────────────────
#  PANTALLA FINAL (ganaste / perdiste / empate)
# ─────────────────────────────────────────────

def pantalla_final(pantalla, ganador, promedio=None, mejor_ronda=None):
    """
    Muestra la pantalla de fin de partida.
    ganador: "usuario" | "cpu" | "empate"
    Retorna True si el jugador quiere jugar de nuevo, False para salir.
    """
    clock = pygame.time.Clock()
    fuente_titulo  = pygame.font.SysFont("Arial", 40, bold=True)
    fuente_cat     = pygame.font.SysFont("Arial", 20, bold=True)
    fuente_normal  = pygame.font.SysFont("Arial", 16)
    fuente_boton   = pygame.font.SysFont("Arial", 16, bold=True)

    MSGS = {
        "usuario": ("🏆 ¡Ganaste!", (100, 230, 100)),
        "cpu":     ("💀 Perdiste...", (255, 80, 80)),
        "empate":  ("🤝 ¡Empate!", (255, 210, 40)),
    }
    msg, color_msg = MSGS.get(ganador, ("Fin de partida", COLOR_TEXTO))

    btn_nuevo = Boton((ANCHO // 2 - 230, ALTO - 130, 200, 50), "🔄 Jugar de nuevo", fuente_boton)
    btn_salir  = Boton((ANCHO // 2 + 30,  ALTO - 130, 200, 50), "🚪 Salir",           fuente_boton)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            btn_nuevo.actualizar_hover(mouse_pos)
            btn_salir.actualizar_hover(mouse_pos)
            if btn_nuevo.fue_clickeado(evento):
                return True
            if btn_salir.fue_clickeado(evento):
                return False

        pantalla.fill(COLOR_FONDO)

        # Panel central
        panel = pygame.Rect(ANCHO // 2 - 320, 80, 640, 440)
        dibujar_panel(pantalla, panel, COLOR_PANEL, radio=16, borde=color_msg, grosor_borde=3)

        dibujar_texto(pantalla, msg, fuente_titulo, color_msg, ANCHO // 2, 120, centrado=True)

        if promedio is not None:
            dibujar_texto(pantalla, f"Promedio de golpes por combate: {promedio:.1f}",
                          fuente_cat, COLOR_TEXTO, ANCHO // 2, 220, centrado=True)
        if mejor_ronda is not None:
            golpes, num = mejor_ronda
            dibujar_texto(pantalla, f"Mejor combate: {golpes} golpes (pokémon #{num})",
                          fuente_normal, COLOR_SUBTEXTO, ANCHO // 2, 265, centrado=True)

        dibujar_texto(pantalla, "¿Querés jugar de nuevo?", fuente_normal, COLOR_SUBTEXTO,
                      ANCHO // 2, 340, centrado=True)
        btn_nuevo.dibujar(pantalla)
        btn_salir.dibujar(pantalla)

        pygame.display.flip()
        clock.tick(60)


# ─────────────────────────────────────────────
#  PANTALLA: DESEMPATE
# ─────────────────────────────────────────────

def pantalla_desempate(pantalla, equipo_usu, equipo_compu):
    """
    Cuando hay empate permite al jugador elegir un pokémon para desempatar.
    Retorna (poke_usu, poke_compu) o ("empate_final", None) si se declara empate.
    """
    clock = pygame.time.Clock()
    fuente_titulo = pygame.font.SysFont("Arial", 24, bold=True)
    fuente_cat    = pygame.font.SysFont("Arial", 18, bold=True)
    fuente_normal = pygame.font.SysFont("Arial", 15)
    fuente_boton  = pygame.font.SysFont("Arial", 14, bold=True)
    fuente_pequeña = pygame.font.SysFont("Arial", 13)

    sprites_cache = {}
    for pok in equipo_usu + equipo_compu:
        sprites_cache[pok.nombre.lower()] = obtener_sprite(pok.nombre)

    CARD_W, CARD_H = 210, 50
    total_w = len(equipo_usu) * CARD_W + (len(equipo_usu) - 1) * 16
    sx = (ANCHO - total_w) // 2
    botones = []
    for i, pok in enumerate(equipo_usu):
        b = Boton((sx + i * (CARD_W + 16), 340, CARD_W, CARD_H),
                  pok.nombre.capitalize(), fuente_boton, tag=pok)
        botones.append(b)

    seleccion = None
    btn_ok     = Boton((ANCHO // 2 - 230, 440, 210, 46), "¡Desempatar! →",  fuente_boton)
    btn_empate = Boton((ANCHO // 2 + 20,  440, 210, 46), "🤝 Declarar empate", fuente_boton)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return ("empate_final", None)
            for b in botones:
                b.actualizar_hover(mouse_pos)
                if b.fue_clickeado(evento):
                    for bb in botones:
                        bb.activo = False
                    b.activo = True
                    seleccion = b.tag
            btn_ok.actualizar_hover(mouse_pos)
            btn_empate.actualizar_hover(mouse_pos)
            if seleccion and btn_ok.fue_clickeado(evento):
                seleccion.vida = 5
                poke_compu = random.choice(equipo_compu)
                poke_compu.vida = 5
                return (seleccion, poke_compu)
            if btn_empate.fue_clickeado(evento):
                return ("empate_final", None)

        pantalla.fill(COLOR_FONDO)
        dibujar_texto(pantalla, "🤝 ¡Empate! ¿Querés desempatar?", fuente_titulo,
                      COLOR_BORDE_SEL, ANCHO // 2, 50, centrado=True)
        dibujar_texto(pantalla, "Elegí un pokémon para revivir y seguir la batalla:",
                      fuente_normal, COLOR_SUBTEXTO, ANCHO // 2, 100, centrado=True)

        for i, pok in enumerate(equipo_usu):
            pr = pygame.Rect(sx + i * (CARD_W + 16), 155, CARD_W, 150)
            dibujar_panel(pantalla, pr, (20, 30, 55), radio=8, borde=COLOR_BORDE)
            spr = sprites_cache.get(pok.nombre.lower())
            if spr:
                pantalla.blit(pygame.transform.scale(spr, (64, 64)), (pr.x + 6, pr.y + 42))
            dibujar_texto(pantalla, pok.nombre.capitalize(), fuente_cat, COLOR_TEXTO, pr.x + 76, pr.y + 8)
            barra_stat(pantalla, pr.x + 76, pr.y + 38, 90, pok.ataque,    2.0, COLOR_ATK, fuente_pequeña, "ATK")
            barra_stat(pantalla, pr.x + 76, pr.y + 58, 90, pok.defensa,   2.0, COLOR_DEF, fuente_pequeña, "DEF")
            barra_stat(pantalla, pr.x + 76, pr.y + 78, 90, pok.velocidad, 2.0, COLOR_SPD, fuente_pequeña, "SPD")

        for b in botones:
            b.dibujar(pantalla)
        if seleccion:
            btn_ok.dibujar(pantalla)
        btn_empate.dibujar(pantalla)

        pygame.display.flip()
        clock.tick(60)


# ─────────────────────────────────────────────
#  ORQUESTADOR PRINCIPAL DE PARTIDA
# ─────────────────────────────────────────────

def run_partida(pantalla, equipo_usu, equipo_compu, lista_eventos, lista_ambientes):
    """
    Orquesta toda la partida desde que se tienen los equipos hasta la pantalla final.
    Reproduce exactamente la lógica de funciones.partida() pero con GUI.

    Retorna:
        "nuevo"  → el jugador quiere jugar de nuevo
        "salir"  → el jugador quiere salir
        None     → ventana cerrada
    """
    import random

    # 1. Elegir ambiente y aplicarlo
    ambiente = random.choice(lista_ambientes)
    for pok in equipo_usu:
        ambiente.modifica_atributo(pok, cpu=False)
    for pok in equipo_compu:
        ambiente.modifica_atributo(pok, cpu=True)

    # 2. Jugador elige su primer pokémon
    poke_usu = pantalla_elegir_inicial(pantalla, equipo_usu, ambiente)
    if poke_usu is None:
        return None

    # CPU elige al azar
    poke_compu = random.choice(equipo_compu)

    # Listas de los pokemones que aún pueden pelear (sin el que está activo)
    bench_usu   = [p for p in equipo_usu   if p is not poke_usu]
    bench_compu = [p for p in equipo_compu if p is not poke_compu]

    puntos_usu   = 0
    puntos_compu = 0
    dict_usu     = {}
    dict_compu   = {}
    info_rondas  = []

    # 3. Bucle principal de batalla
    while True:
        res = pantalla_batalla(
            pantalla, poke_usu, poke_compu, bench_usu,
            lista_eventos, puntos_usu, puntos_compu
        )
        if res.get("cerrado"):
            return None

        poke_usu     = res["poke_usu"]
        poke_compu   = res["poke_compu"]
        puntos_usu   = res["puntos_usu"]
        puntos_compu = res["puntos_compu"]

        # Acumular diccionarios de acciones (el log ya los tiene implícitamente)
        # (simplificado: contamos los mensajes del log para estadísticas)
        ataques = sum(1 for l in res["log"] if "⚔" in l or "✨" in l)
        info_rondas.append([ataques, not res["usu_murio"]])

        usu_sin_pokes   = res["usu_murio"]   and len(bench_usu)   == 0
        compu_sin_pokes = res["compu_murio"]  and len(bench_compu) == 0

        # ── Condición de fin de partida ──
        if usu_sin_pokes and compu_sin_pokes:
            # Empate: ofrecer desempate
            res_desempate = pantalla_desempate(pantalla, equipo_usu, equipo_compu)
            if res_desempate[0] == "empate_final":
                ganador = "empate"
                break
            else:
                poke_usu, poke_compu = res_desempate
                bench_usu   = [p for p in equipo_usu   if p is not poke_usu]
                bench_compu = [p for p in equipo_compu if p is not poke_compu]
                puntos_usu = puntos_compu = 0
                continue

        elif usu_sin_pokes:
            ganador = "cpu"
            break

        elif compu_sin_pokes:
            ganador = "usuario"
            break

        # ── Reemplazar pokemones caídos ──
        if res["usu_murio"] and bench_usu:
            nuevo = pantalla_elegir_siguiente(pantalla, bench_usu)
            if nuevo is None:
                return None
            bench_usu.remove(nuevo)
            poke_usu = nuevo
            puntos_usu = 0

        if res["compu_murio"] and bench_compu:
            poke_compu = random.choice(bench_compu)
            bench_compu.remove(poke_compu)
            puntos_compu = 0

    # 4. Calcular estadísticas
    from src.analizar_datos import promedio as calc_promedio
    try:
        prom, mejor = calc_promedio(info_rondas)
    except Exception:
        prom, mejor = 0, (0, 0)

    # 5. Pantalla final
    seguir = pantalla_final(pantalla, ganador, prom, mejor)
    return "nuevo" if seguir else "salir"


# ─────────────────────────────────────────────
#  FUNCIÓN DE ENTRADA PRINCIPAL
# ─────────────────────────────────────────────

def run_seleccion(pokemones_obj):
    """
    Inicializa pygame, corre la pantalla de selección y la cierra.
    Retorna la lista de 3 objetos Pokemon del equipo del jugador,
    o None si el usuario cerró la ventana.
    """
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Pokémon Battle")
    equipo = pantalla_seleccion(pantalla, pokemones_obj)
    return equipo, pantalla


# ─────────────────────────────────────────────
#  TEST STANDALONE (python app.py)
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))

    from src.pokemones  import convertir_diccio
    from src.clases     import Ambiente, Evento_aleatorio

    list_poke = {
        "Novatos": ["dragonite", "tyranitar", "metagross", "arcanine"],
        "Medios":  ["vaporeon",  "jolteon",   "pikachu",   "eevee"],
        "Altos":   ["psyduck",   "charmander","charizard",  "rattata"],
    }
    list_cpu = {
        "Novatos": ["dragonite", "tyranitar", "metagross", "arcanine"],
        "Medios":  ["vaporeon",  "jolteon",   "pikachu",   "eevee"],
        "Altos":   ["psyduck",   "charmander","charizard",  "rattata"],
    }

    print("Cargando pokemones...")
    pokemones_usu = convertir_diccio(list_poke)
    pokemones_cpu = convertir_diccio(list_cpu)

    # Ambientes y eventos (idénticos a main.py)
    lista_ambientes = [
        Ambiente("playa",           "water",    -0.20, -0.05, -0.25),
        Ambiente("bosque",          "ground",   -0.20, -0.15, -0.10),
        Ambiente("tormenta",        "electric", -0.15, -0.20, -0.30),
        Ambiente("volcán",          "fire",     -0.50, -0.15, -0.10),
    ]
    lista_eventos = [
        Evento_aleatorio("un kit médico", 1),
        Evento_aleatorio("un ibuprofeno", 0.5),
        Evento_aleatorio("una gripe",    -0.5),
        Evento_aleatorio("asma",         -1),
    ]

    while True:
        # Selección del equipo usuario
        equipo_usu, pantalla = run_seleccion(pokemones_usu)
        if equipo_usu is None:
            break

        # CPU elige automáticamente
        import random
        equipo_compu = []
        pares_cpu = {
            "ataque": "velocidad", "velocidad": "ataque",
            "defensa": "adaptabilidad", "adaptabilidad": "defensa",
        }
        for cat, lista in pokemones_cpu.items():
            pok = random.choice(lista)
            atr = random.choice(["ataque", "velocidad", "defensa", "adaptabilidad"])
            pok.cambiar_atributo(atr, pares_cpu[atr], 0.15, print_cambios=False)
            equipo_compu.append(pok)

        resultado = run_partida(pantalla, equipo_usu, equipo_compu, lista_eventos, lista_ambientes)

        if resultado == "nuevo":
            # Recargar pokemones frescos de la API para una partida nueva
            pokemones_usu = convertir_diccio(list_poke)
            pokemones_cpu = convertir_diccio(list_cpu)
            continue
        else:
            break

    pygame.quit()