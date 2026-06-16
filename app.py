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
            info_rect = pygame.Rect(ANCHO // 2 - 260, 275, 520, 160)
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
#  FUNCIÓN DE ENTRADA (para integrar desde main)
# ─────────────────────────────────────────────
def run_seleccion(pokemones_obj):
    """
    Inicializa pygame, corre la pantalla de selección y la cierra.
    Retorna la lista de 3 objetos Pokemon del equipo del jugador,
    o None si el usuario cerró la ventana.

    Uso desde main.py:
        from seleccion import run_seleccion
        equipo = run_seleccion(pokemones_obj)
    """
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Pokémon Battle — Seleccioná tu equipo")

    equipo = pantalla_seleccion(pantalla, pokemones_obj)

    # No llamamos pygame.quit() acá para que la siguiente pantalla
    # (batalla) siga usando el mismo contexto de pygame.
    return equipo


# ─────────────────────────────────────────────
#  TEST STANDALONE (python seleccion.py)
# ─────────────────────────────────────────────
if __name__ == "__main__":
    # Importamos las funciones reales del proyecto
    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))

    from src.pokemones import convertir_diccio

    list_poke = {
        "Novatos": ["dragonite", "tyranitar", "metagross", "arcanine"],
        "Medios":  ["vaporeon",  "jolteon",   "pikachu",   "eevee"],
        "Altos":   ["psyduck",   "charmander","charizard",  "rattata"],
    }

    print("Cargando pokemones desde la API...")
    pokemones_obj = convertir_diccio(list_poke)
    print("Listo. Abriendo pantalla de selección...")

    equipo = run_seleccion(pokemones_obj)

    if equipo:
        print("\nEquipo elegido:")
        for p in equipo:
            print(f"  {p.nombre}  |  ATK:{p.ataque}  DEF:{p.defensa}  SPD:{p.velocidad}  ADP:{p.adaptabilidad}")
    else:
        print("Ventana cerrada sin seleccionar.")

    pygame.quit()