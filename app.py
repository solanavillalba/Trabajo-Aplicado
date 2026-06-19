import pygame
import requests
import io
import random
import os

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

# Paths de las imágenes de fondo según ambiente
# Las imágenes deben estar en la subcarpeta "imagenes/" junto a app.py
_DIR_APP = os.path.dirname(os.path.abspath(__file__))
IMAGENES_AMBIENTE = {
    "playa":             os.path.join(_DIR_APP, "imagenes", "imagen_pokemon_playa.png"),
    "bosque":            os.path.join(_DIR_APP, "imagenes", "imagen_pokemon_bosque.png"),
    "volcán":            os.path.join(_DIR_APP, "imagenes", "imagen_pokemon_volcan.png"),
    "tormenta": os.path.join(_DIR_APP, "imagenes", "imagen_pokemon_tormenta.png"),
}

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
    "Novatos": ["magikarp", "sandshrew", "tepig", "pikachu"],
    "Medios": ["wartortle", "marowak", "charmeleon", "luxio"],
    "Altos": ["milotic", "hippowdon", "arcanine", "jolteon"]}

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


def pantalla_introduccion(pantalla):
    """
    Pantalla de bienvenida / instrucciones del juego, mostrada antes de elegir
    el equipo. Sigue la misma estética que el resto de la app (panel oscuro,
    borde azul eléctrico, acentos amarillo "pikachu").

    Se avanza con clic o cualquier tecla. Si el contenido no entra en pantalla,
    se puede hacer scroll con la rueda del mouse o las flechas ↑ / ↓.

    Retorna True si se avanzó normalmente, o False si el usuario cerró la ventana.
    """
    import textwrap

    clock = pygame.time.Clock()

    fuente_titulo   = pygame.font.SysFont("Arial", 30, bold=True)
    fuente_subtitulo = pygame.font.SysFont("Arial", 16, italic=True)
    fuente_seccion  = pygame.font.SysFont("Arial", 18, bold=True)
    fuente_normal   = pygame.font.SysFont("Arial", 15)
    fuente_chica    = pygame.font.SysFont("Arial", 13)

    # ── Contenido estructurado en bloques ──
    # tipo: "seccion" (título de paso, en amarillo) | "texto" (párrafo normal)
    #       "vineta"  (línea con bullet, p. ej. una categoría o acción)
    CONTENIDO = [
        ("seccion", "1. Armá tu equipo"),
        ("texto",   "Seleccioná un Pokémon de cada categoría para formar tu equipo de 3:"),
        ("vineta",  "Novato"),
        ("vineta",  "Medio"),
        ("vineta",  "Alto"),

        ("seccion", "2. Personalizá tus atributos"),
        ("texto",   "Antes de la batalla podrás modificar algunos atributos de tus Pokémon "
                    "para adaptarlos a tu estrategia. Tené en cuenta que mejorar una "
                    "estadística implica reducir otra."),

        ("seccion", "3. El ambiente de combate"),
        ("texto",   "Se elegirá aleatoriamente uno de estos escenarios:"),
        ("vineta",  "Playa"),
        ("vineta",  "Bosque"),
        ("vineta",  "Tormenta de Rayos"),
        ("vineta",  "Volcán"),
        ("texto",   "Según su tipo, algunos Pokémon se verán beneficiados por el ambiente "
                    "y otros perjudicados. La adaptabilidad les permite resistir mejor los "
                    "efectos negativos."),

        ("seccion", "4. La batalla"),
        ("texto",   "Elegí cuál de tus Pokémon inicia el combate. La computadora hará lo "
                    "mismo con uno de los suyos. En cada turno podrás:"),
        ("vineta",  "Atacar — inflige daño al rival."),
        ("vineta",  "Defender — reduce el daño recibido."),
        ("vineta",  "Esquivar — intenta evitar el ataque por completo; la probabilidad "
                    "de éxito depende de la velocidad."),
        ("vineta",  "Ataque especial — tras 3 ataques exitosos consecutivos, desbloqueás "
                    "un golpe poderoso según tu ataque especial."),
        ("texto",   "Eventos aleatorios: durante la batalla pueden ocurrir sucesos "
                    "inesperados que suban o bajen la vida de algún Pokémon, cambiando "
                    "el rumbo del combate."),

        ("seccion", "5. Cuando un Pokémon cae"),
        ("texto",   "Si uno de tus Pokémon es derrotado, elegís otro integrante de tu "
                    "equipo para seguir luchando. La batalla termina cuando un equipo se "
                    "queda sin Pokémon disponibles."),

        ("seccion", "6. Empate"),
        ("texto",   "Si los últimos Pokémon de ambos equipos caen al mismo tiempo, podés "
                    "aceptar el empate o disputar un combate de desempate."),

        ("seccion", "7. Estadísticas finales"),
        ("texto",   "Al terminar la partida vas a ver estadísticas y gráficos sobre las "
                    "acciones realizadas durante el combate."),
    ]

    # ── Layout del panel ──
    PANEL_W = 760
    PANEL_X = (ANCHO - PANEL_W) // 2
    PANEL_Y = 96
    PANEL_H = ALTO - PANEL_Y - 60
    PAD_X   = 36
    WRAP_W  = PANEL_W - 2 * PAD_X

    # Anchos de envoltura de texto aproximados según fuente (caracteres por línea)
    def envolver(texto, fuente, ancho_px):
        """Envuelve un texto en líneas que entren en ancho_px, midiendo con la fuente real."""
        palabras = texto.split(" ")
        lineas, actual = [], ""
        for palabra in palabras:
            prueba = (actual + " " + palabra).strip()
            if fuente.size(prueba)[0] <= ancho_px:
                actual = prueba
            else:
                if actual:
                    lineas.append(actual)
                actual = palabra
        if actual:
            lineas.append(actual)
        return lineas

    # ── Pre-renderizamos todas las líneas con su estilo, una sola vez ──
    # cada item: (texto, fuente, color, indent_x, espacio_extra_arriba)
    lineas_render = []
    for tipo, contenido in CONTENIDO:
        if tipo == "seccion":
            lineas_render.append(("", None, None, 0, 10))   # espacio antes de cada sección
            lineas_render.append((contenido, fuente_seccion, COLOR_BORDE_SEL, 0, 0))
        elif tipo == "texto":
            for ln in envolver(contenido, fuente_normal, WRAP_W):
                lineas_render.append((ln, fuente_normal, COLOR_TEXTO, 0, 0))
        elif tipo == "vineta":
            sub_ancho = WRAP_W - 22
            partes = envolver(contenido, fuente_normal, sub_ancho)
            for j, ln in enumerate(partes):
                prefijo = "•  " if j == 0 else "    "
                lineas_render.append((prefijo + ln, fuente_normal, COLOR_SUBTEXTO, 14, 0))

    LINE_H = 24
    SECTION_GAP = 10

    # Calculamos la altura total del contenido para el scroll
    contenido_alto = 0
    for texto, fuente, color, indent, extra in lineas_render:
        contenido_alto += LINE_H + extra

    max_scroll = max(0, contenido_alto - (PANEL_H - 40))
    scroll_y = 0

    # ── "¡Buena suerte!" como cierre fijo debajo del panel con scroll ──
    avanzar = False

    while not avanzar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_PAGEUP, pygame.K_PAGEDOWN):
                    paso = 60 if evento.key in (pygame.K_PAGEUP, pygame.K_PAGEDOWN) else 28
                    if evento.key in (pygame.K_UP, pygame.K_PAGEUP):
                        scroll_y = max(0, scroll_y - paso)
                    else:
                        scroll_y = min(max_scroll, scroll_y + paso)
                else:
                    avanzar = True
            if evento.type == pygame.MOUSEBUTTONDOWN:
                avanzar = True
            if evento.type == pygame.MOUSEWHEEL:
                scroll_y = max(0, min(max_scroll, scroll_y - evento.y * 28))

        # ── DIBUJO ──
        pantalla.fill(COLOR_FONDO)

        dibujar_texto(pantalla, "Pokémon Battle", fuente_titulo, COLOR_TEXTO,
                      ANCHO // 2, 26, centrado=True)
        dibujar_texto(pantalla, "Guía rápida antes de empezar", fuente_subtitulo, COLOR_SUBTEXTO,
                      ANCHO // 2, 64, centrado=True)

        panel_rect = pygame.Rect(PANEL_X, PANEL_Y, PANEL_W, PANEL_H)
        dibujar_panel(pantalla, panel_rect, COLOR_PANEL, radio=16, borde=COLOR_BORDE, grosor_borde=2)

        # Intro narrativa, siempre visible arriba del texto con scroll
        intro_y = PANEL_Y + 18
        for ln in envolver(
            "Tu misión será formar un equipo de 3 Pokémon y derrotar al equipo rival "
            "antes de que todos tus Pokémon sean vencidos.",
            fuente_normal, WRAP_W
        ):
            dibujar_texto(pantalla, ln, fuente_normal, COLOR_TEXTO, PANEL_X + PAD_X, intro_y)
            intro_y += LINE_H

        # Área con scroll para el resto del contenido
        scroll_top = intro_y + 12
        scroll_rect = pygame.Rect(PANEL_X + 4, scroll_top, PANEL_W - 8, PANEL_Y + PANEL_H - scroll_top - 10)

        clip_prev = pantalla.get_clip()
        pantalla.set_clip(scroll_rect)
        y = scroll_rect.y - scroll_y
        for texto, fuente, color, indent, extra in lineas_render:
            y += extra
            if texto and fuente is not None:
                dibujar_texto(pantalla, texto, fuente, color, PANEL_X + PAD_X + indent, y)
            y += LINE_H
        pantalla.set_clip(clip_prev)

        # Línea divisoria sutil para indicar que hay scroll si corresponde
        if max_scroll > 0:
            pygame.draw.line(pantalla, COLOR_BORDE,
                             (PANEL_X + 10, scroll_rect.y - 4), (PANEL_X + PANEL_W - 10, scroll_rect.y - 4), 1)
            pygame.draw.line(pantalla, COLOR_BORDE,
                             (PANEL_X + 10, scroll_rect.bottom + 4), (PANEL_X + PANEL_W - 10, scroll_rect.bottom + 4), 1)

        # ── Indicación para avanzar ──
        pulso = 150 + int(80 * abs((pygame.time.get_ticks() % 1400) / 700 - 1))
        color_pulso = (pulso, pulso - 30 if pulso > 60 else 0, 40)
        msg = "Haz clic o pulsá cualquier tecla para continuar"
        dibujar_texto(pantalla, msg, fuente_chica, COLOR_BORDE_SEL,
                      ANCHO // 2, ALTO - 34, centrado=True)
        if max_scroll > 0:
            dibujar_texto(pantalla, "↑ ↓ / rueda del mouse para desplazarte", fuente_chica,
                          COLOR_SUBTEXTO, ANCHO // 2, PANEL_Y - 26, centrado=True)

        pygame.display.flip()
        clock.tick(60)

    return True


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
    paso_actual   = 0          # 0,1,2 : qué categoría estamos eligiendo
    selecciones   = {}         # {"Novatos": obj_pokemon, ...}
    atrib_sel     = {}         # {"Novatos": "ataque", ...}
    sprites_cache = {}         # nombre : Surface o None

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

    botones_pokemones = {}   # cat : [Boton, ...]
    for cat in CATEGORIAS:
        bots = []
        for i, nombre in enumerate(LISTA_POKEMONES[cat]):
            rx = start_x + i * (CARD_W + CARD_GAP)
            ry = 200
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
    btn_confirmar = Boton((ANCHO // 2 - 100, 570, 200, 46), "Confirmar", fuente_boton)

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
        dibujar_texto(pantalla, "Armá tu equipo", fuente_titulo, COLOR_TEXTO, ANCHO // 2, 18, centrado=True)

        # Indicador de pasos
        for i, c in enumerate(CATEGORIAS):
            cx = 200 + i * 350
            completado = c in selecciones and c in atrib_sel
            actual     = i == paso_actual
            color_c    = COLOR_BORDE_SEL if actual else (COLOR_TITULO_CAT[c] if completado else COLOR_SUBTEXTO)
            marca      = "✓ " if completado and not actual else ""
            dibujar_texto(pantalla, f"{c}", fuente_cat, color_c, cx, 60, centrado=True)
            # línea indicadora
            if actual:
                pygame.draw.rect(pantalla, COLOR_BORDE_SEL, (cx - 40, 82, 80, 3), border_radius=2)

        # Panel central
        panel_rect = pygame.Rect(30, 100, ANCHO - 60, ALTO - 120)
        dibujar_panel(pantalla, panel_rect, COLOR_PANEL, radio=14, borde=COLOR_BORDE, grosor_borde=1)

        # ── Título de categoría ──
        color_cat = COLOR_TITULO_CAT[cat]
        dibujar_texto(pantalla, f"Categoría: {cat}", fuente_cat, color_cat, ANCHO // 2, 135, centrado=True)
        dibujar_texto(pantalla, "Elegí tu pokémon:", fuente_normal, COLOR_SUBTEXTO, ANCHO // 2, 160, centrado=True)

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
            BAR_W   = 110
            COL2_X  = tx + 185   # inicio de la segunda columna

            barra_stat(pantalla, tx,     info_rect.y + 62,  BAR_W, poke_mostrar.ataque,       2.15, COLOR_ATK, fuente_pequeña, "ATK")
            barra_stat(pantalla, tx,     info_rect.y + 92,  BAR_W, poke_mostrar.defensa,       0.90, COLOR_DEF, fuente_pequeña, "DEF")
            barra_stat(pantalla, COL2_X, info_rect.y + 62,  BAR_W, poke_mostrar.velocidad,     0.90, COLOR_SPD, fuente_pequeña, "SPD")
            barra_stat(pantalla, COL2_X, info_rect.y + 92,  BAR_W, poke_mostrar.adaptabilidad, 1.00, COLOR_ADP, fuente_pequeña, "ADP")

            # Vida
            dibujar_texto(pantalla, f"Vida: {poke_mostrar.vida}  |  Sp.Atk: {poke_mostrar.special_attack}",
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
                msg = f" {atrib_sel_actual.capitalize()} +0.15   |    {par.capitalize()} -0.15"
                dibujar_texto(pantalla, msg, fuente_pequeña, COLOR_SUBTEXTO, ANCHO // 2, 540, centrado=True)

        # ── Botón Confirmar ──
        puede_confirmar = (poke_sel_actual is not None and atrib_sel_actual is not None)
        if puede_confirmar:
            label = "Confirmar" if paso_actual < 2 else "¡Iniciar batalla!"
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
    btn_ok = Boton((ANCHO // 2 - 110, 490, 220, 46), "¡A pelear!", fuente_boton)

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
            barra_stat(pantalla, pr.x + 76, pr.y + 32, 80, pok.ataque,       2.15, COLOR_ATK, fuente_pequeña, "ATK")
            barra_stat(pantalla, pr.x + 76, pr.y + 52, 80, pok.defensa,      0.90, COLOR_DEF, fuente_pequeña, "DEF")
            barra_stat(pantalla, pr.x + 76, pr.y + 72, 80, pok.velocidad,    0.90, COLOR_SPD, fuente_pequeña, "SPD")

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
    "atacar":   "Atacar",
    "defender": "Defender",
    "esquivar": "Esquivar",
    "especial": "Especial",
}

MAX_LOG = 7   # (legacy, ya no se usa — _dibujar_log calcula el espacio dinámicamente)


def _dibujar_log(sup, log_global, log_rect, fuente_log, fuente_pequeña):
    """
    Dibuja el panel del log de batalla mostrando TODO el historial acumulado.
    Las líneas más nuevas quedan abajo; cuando no entran todas, se recortan
    las más viejas (scroll automático hacia arriba), nunca las nuevas.
    """
    dibujar_panel(sup, log_rect, (15, 22, 45), radio=8, borde=(50, 70, 120))
    dibujar_texto(sup, "Log de batalla", fuente_pequeña, COLOR_SUBTEXTO,
                  log_rect.x + 8, log_rect.y + 4)

    LINE_H    = 16
    top_y     = log_rect.y + 22
    max_lines = max(1, (log_rect.height - 24) // LINE_H)

    lineas_vis = log_global[-max_lines:]   # las últimas N líneas (recorta las viejas)

    # Recortamos para que nada se dibuje fuera del panel
    clip_prev = sup.get_clip()
    sup.set_clip(log_rect.inflate(-4, -4))
    for j, (texto, color) in enumerate(lineas_vis):
        dibujar_texto(sup, texto, fuente_log, color, log_rect.x + 8, top_y + j * LINE_H)
    sup.set_clip(clip_prev)


def pantalla_batalla(pantalla, poke_usu, poke_compu, eventos_random,
                     puntos_usu, puntos_compu, log_global, dict_usu, dict_cpu, ambiente=None):
    """
    Muestra la pantalla de batalla y espera que el jugador elija una acción.
    Una vez elegida, resuelve la ronda, agrega los mensajes nuevos a log_global
    (que persiste durante TODA la partida) y muestra el resultado antes de salir.

    log_global : list de tuplas (texto:str, color:tuple). Se modifica in-place
                 y también se usa para pintar el log en cada frame.
    dict_usu, dict_cpu : dict que cuenta cuántas veces se eligió cada acción
                 (atacar/defender/esquivar/especial). Se modifican in-place,
                 igual que dict_usu/dict_cpu en funciones.ronda() del CLI original.
                 Se usan después para los gráficos de torta de analizar_datos.py.

    Retorna un dict:
    {
      "poke_usu", "poke_compu", "puntos_usu", "puntos_compu",
      "usu_murio", "compu_murio", "cerrado"
    }
    """
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

    # Cargar imagen de fondo del ambiente (una sola vez, escalada al área de batalla)
    _BG_W, _BG_H = ANCHO - 40, 380
    bg_imagen = None
    if ambiente is not None:
        ruta = IMAGENES_AMBIENTE.get(ambiente.nombre)
        print(f"[DEBUG] Ambiente: '{ambiente.nombre}':  ruta: {ruta}")
        print(f"[DEBUG] Archivo existe: {os.path.exists(ruta) if ruta else False}")
        if ruta and os.path.exists(ruta):
            try:
                raw = pygame.image.load(ruta).convert()
                bg_imagen = pygame.transform.scale(raw, (_BG_W, _BG_H))
                print("[DEBUG] Imagen cargada OK")
            except Exception as e:
                print(f"[DEBUG] Error cargando imagen: {e}")
                bg_imagen = None

    # Botones de acción
    acciones = ACCIONES_ESPECIAL if puntos_usu >= 3 else ACCIONES_BASE
    BTN_W, BTN_H = 190, 48
    BTN_GAP = 14
    total_btns_w = len(acciones) * BTN_W + (len(acciones) - 1) * BTN_GAP
    bx0 = (ANCHO - total_btns_w) // 2
    botones_accion = []
    for i, acc in enumerate(acciones):
        b = Boton((bx0 + i * (BTN_W + BTN_GAP), 600, BTN_W, BTN_H),
                  ETIQUETA_ACCION[acc], fuente_boton, tag=acc)
        botones_accion.append(b)

    log_rect = pygame.Rect(220, 430, ANCHO - 440, 130)

    def _barra_vida(sup, x, y, ancho, vida_actual, vida_max, fuente_p, nombre, invertido=False):
        """
        Dibuja la barra de vida de un pokémon.

        - Vida se muestra como porcentaje (vida_max = 100%).
        - Si vida_actual > vida_max, el excedente se representa en dorado
          superpuesto al final de la barra, al estilo de los juegos de lucha.
        """
        vida_base  = min(vida_actual, vida_max)   # la parte que cabe en la barra normal
        ratio_base = max(0.0, vida_base / vida_max)

        # Color de la barra base según cuánta vida queda
        if ratio_base > 0.5:
            col_base = (80, 220, 80)
        elif ratio_base > 0.25:
            col_base = (255, 200, 40)
        else:
            col_base = (255, 60, 60)

        # Texto: Vida como porcentaje (5 Vida = 100 %, 6 Vida = 120 %, etc.)
        pct = round(vida_actual / vida_max * 100)
        label_Vida = f"{nombre.capitalize()}  Vida: {pct}%"
        if invertido:
            txt = fuente_p.render(label_Vida, True, COLOR_TEXTO)
            sup.blit(txt, (x + ancho - txt.get_width(), y - 18))
        else:
            dibujar_texto(sup, label_Vida, fuente_p, COLOR_TEXTO, x, y - 18)

        # Fondo de la barra
        bg = pygame.Rect(x, y, ancho, 14)
        pygame.draw.rect(sup, (50, 60, 90), bg, border_radius=7)

        # Barra base (no supera el 100 %)
        fill_w = int(ratio_base * ancho)
        if fill_w > 0:
            pygame.draw.rect(sup, col_base, (x, y, fill_w, 14), border_radius=7)

        # Barra de excedente (Vida > vida_max) superpuesta al final, en dorado
        if vida_actual > vida_max:
            excedente   = vida_actual - vida_max
            overflow_w  = min(ancho, max(4, int(excedente / vida_max * ancho)))
            ox = x + ancho - overflow_w
            pygame.draw.rect(sup, (255, 185, 0), (ox, y, overflow_w, 14), border_radius=7)

        # Borde de la barra
        pygame.draw.rect(sup, COLOR_BORDE, bg, 1, border_radius=7)

    def _dibujar_escena(mostrar_botones):
        """Dibuja todo el frame de batalla. Se reusa en ambas fases (elegir / resultado)."""
        pantalla.fill(COLOR_FONDO)
        dibujar_texto(pantalla, "Batalla Pokémon", fuente_titulo, COLOR_TEXTO,
                      ANCHO // 2, 14, centrado=True)

        area_rect = pygame.Rect(20, 45, ANCHO - 40, 380)
        dibujar_panel(pantalla, area_rect, (18, 26, 50), radio=12, borde=COLOR_BORDE, grosor_borde=1)

        # Fondo de ambiente (debajo de sprites, barras y texto)
        if bg_imagen is not None:
            pantalla.blit(bg_imagen, (area_rect.x, area_rect.y))
            overlay = pygame.Surface((area_rect.w, area_rect.h), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 110))   # oscurece un poco para que se lea el texto
            pantalla.blit(overlay, (area_rect.x, area_rect.y))
            pygame.draw.rect(pantalla, COLOR_BORDE, area_rect, 1, border_radius=12)

        # Jugador (izquierda)
        spr_usu = sprites_cache.get(poke_usu.nombre.lower())
        if spr_usu:
            pantalla.blit(pygame.transform.scale(spr_usu, (128, 128)), (50, 130))
        else:
            placeholder_sprite(pantalla, 114, 194)

        _barra_vida(pantalla, 40, 90, 260, poke_usu.vida, 5, fuente_normal,
                    poke_usu.nombre, invertido=False)

        barra_stat(pantalla, 40, 245, 80, poke_usu.ataque,      2.15, COLOR_ATK, fuente_pequeña, "ATK")
        barra_stat(pantalla, 40, 265, 80, poke_usu.defensa,     0.90, COLOR_DEF, fuente_pequeña, "DEF")
        barra_stat(pantalla, 40, 285, 80, poke_usu.velocidad,   0.90, COLOR_SPD, fuente_pequeña, "SPD")

        dibujar_texto(pantalla, f"Racha: {puntos_usu}/3", fuente_pequeña,
                      COLOR_BORDE_SEL if puntos_usu >= 3 else COLOR_SUBTEXTO, 40, 310)
        if puntos_usu >= 3:
            dibujar_texto(pantalla, "¡ESPECIAL DISPONIBLE!", fuente_pequeña, COLOR_BORDE_SEL, 40, 328)

        # CPU (derecha)
        spr_cpu = sprites_cache.get(poke_compu.nombre.lower())
        if spr_cpu:
            spr_cpu_flip = pygame.transform.flip(pygame.transform.scale(spr_cpu, (128, 128)), True, False)
            pantalla.blit(spr_cpu_flip, (ANCHO - 180, 130))
        else:
            placeholder_sprite(pantalla, ANCHO - 114, 194)

        _barra_vida(pantalla, ANCHO - 300, 90, 260, poke_compu.vida, 5, fuente_normal,
                    poke_compu.nombre, invertido=True)

        barra_stat(pantalla, ANCHO - 180, 245, 80, poke_compu.ataque,    2.15, COLOR_ATK, fuente_pequeña, "ATK")
        barra_stat(pantalla, ANCHO - 180, 265, 80, poke_compu.defensa,   0.90, COLOR_DEF, fuente_pequeña, "DEF")
        barra_stat(pantalla, ANCHO - 180, 285, 80, poke_compu.velocidad, 0.90, COLOR_SPD, fuente_pequeña, "SPD")
        dibujar_texto(pantalla, f"Racha CPU: {puntos_compu}/3", fuente_pequeña, COLOR_SUBTEXTO,
                      ANCHO - 180, 310)

        dibujar_texto(pantalla, "VS", fuente_titulo, COLOR_BORDE_SEL, ANCHO // 2, 185, centrado=True)

        # Log persistente (siempre se dibuja, sea fase de elección o de resultado)
        _dibujar_log(pantalla, log_global, log_rect, fuente_log, fuente_pequeña)

        if mostrar_botones:
            dibujar_texto(pantalla, "¿Qué hacés?", fuente_cat, COLOR_SUBTEXTO,
                          ANCHO // 2, 568, centrado=True)
            for b in botones_accion:
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
        else:
            dibujar_texto(pantalla, "Clic o tecla para continuar...",
                          fuente_normal, COLOR_SUBTEXTO, ANCHO // 2, 568, centrado=True)

    # ── FASE 1: esperar que el jugador elija una acción ──
    accion_elegida = None
    while accion_elegida is None:
        mouse_pos = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return {"cerrado": True}
            for b in botones_accion:
                b.actualizar_hover(mouse_pos)
                if b.fue_clickeado(evento):
                    accion_elegida = b.tag

        _dibujar_escena(mostrar_botones=True)
        pygame.display.flip()
        clock.tick(60)

    # ── Resolver la ronda ──
    nuevas_lineas, poke_usu, poke_compu, puntos_usu, puntos_compu, accion_cpu = _resolver_ronda(
        poke_usu, poke_compu, accion_elegida, eventos_random, puntos_usu, puntos_compu
    )

    # Registrar las acciones elegidas en los diccionarios de conteo
    # (mismo patrón que dict_usu/dict_cpu en funciones.ronda del CLI)
    dict_usu[accion_elegida] = dict_usu.get(accion_elegida, 0) + 1
    dict_cpu[accion_cpu]     = dict_cpu.get(accion_cpu, 0) + 1

    for linea in nuevas_lineas:
        if "murió" in linea or "cayó" in linea or "ESPECIAL" in linea.upper():
            color = COLOR_BORDE_SEL
        elif linea.startswith("CPU eligió"):
            color = COLOR_SUBTEXTO
        elif "⚡" in linea:
            color = COLOR_ADP
        else:
            color = COLOR_TEXTO
        log_global.append((linea, color))

    usu_murio   = poke_usu.vida   <= 0
    compu_murio = poke_compu.vida <= 0

    # ── FASE 2: mostrar el resultado (log actualizado) hasta que el jugador avance ──
    clock2  = pygame.time.Clock()
    inicio  = pygame.time.get_ticks()
    espera_min_ms = 1100   # si nadie murió, avanza solo tras este tiempo (o con clic/tecla)
    while True:
        avanzar = False
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return {"cerrado": True}
            if evento.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                avanzar = True

        if avanzar:
            break
        if not (usu_murio or compu_murio) and pygame.time.get_ticks() - inicio >= espera_min_ms:
            break

        _dibujar_escena(mostrar_botones=False)
        pygame.display.flip()
        clock2.tick(60)

    return {
        "poke_usu":     poke_usu,
        "poke_compu":   poke_compu,
        "puntos_usu":   puntos_usu,
        "puntos_compu": puntos_compu,
        "usu_murio":    usu_murio,
        "compu_murio":  compu_murio,
        "cerrado":      False,
    }


def _resolver_ronda(poke_usu, poke_compu, accion_usu, eventos_random, puntos_usu, puntos_compu):
    """
    Implementa la misma lógica que funciones.ronda() pero sin input() ni print().
    Retorna (log:list, poke_usu, poke_compu, puntos_usu, puntos_compu, accion_cpu:str).
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
            log.append(f"Evento: {quien} recibió {ev.nombre} (vida {signo}{ev.vida}): Vida:{afectado.vida}")
            if afectado.vida <= 0:
                return log, poke_usu, poke_compu, puntos_usu, puntos_compu, accion_cpu

    # ── Resolver acciones ──
    if accion_usu == "especial" and accion_cpu != "especial":
        dano = round(poke_usu.ataque * (poke_usu.special_attack + 1), 1)
        poke_compu.vida = round(max(0, poke_compu.vida - dano), 1)
        puntos_usu = 0
        if poke_compu.vida <= 0:
            log.append(f"Tu {poke_usu.nombre} usó ESPECIAL: ¡{poke_compu.nombre} murió!")
        else:
            log.append(f"Tu {poke_usu.nombre} usó ESPECIAL: {poke_compu.nombre} Vida:{poke_compu.vida}")
            puntos_usu += 1

    elif accion_cpu == "especial" and accion_usu != "especial":
        dano = round(poke_compu.ataque * (poke_compu.special_attack + 1), 1)
        poke_usu.vida = round(max(0, poke_usu.vida - dano), 1)
        puntos_compu = 0
        if poke_usu.vida <= 0:
            log.append(f"CPU {poke_compu.nombre} usó ESPECIAL: ¡Tu {poke_usu.nombre} murió!")
        else:
            log.append(f"CPU {poke_compu.nombre} usó ESPECIAL: tu {poke_usu.nombre} Vida:{poke_usu.vida}")
            puntos_compu += 1

    elif accion_usu == "especial" and accion_cpu == "especial":
        d1 = round(poke_usu.ataque  * (poke_usu.special_attack  + 1), 1)
        d2 = round(poke_compu.ataque * (poke_compu.special_attack + 1), 1)
        poke_compu.vida = round(max(0, poke_compu.vida - d1), 1)
        poke_usu.vida   = round(max(0, poke_usu.vida   - d2), 1)
        puntos_usu = puntos_compu = 0
        log.append(f"¡Doble ESPECIAL! Tu {poke_usu.nombre} Vida:{poke_usu.vida}  |  CPU {poke_compu.nombre} Vida:{poke_compu.vida}")

    elif accion_usu == "atacar" and accion_cpu == "atacar":
        poke_usu.vida   = round(max(0, poke_usu.vida   - poke_compu.ataque), 1)
        poke_compu.vida = round(max(0, poke_compu.vida - poke_usu.ataque),   1)
        puntos_usu   += 1
        puntos_compu += 1
        log.append(f"Ambos atacan: Tu {poke_usu.nombre} Vida:{poke_usu.vida}  |  CPU {poke_compu.nombre} Vida:{poke_compu.vida}")

    elif accion_usu in ("esquivar", "defender") and accion_cpu in ("esquivar", "defender"):
        log.append("Ninguno atacó. Sin cambios en Vida.")

    elif accion_usu == "atacar" and accion_cpu == "defender":
        dano = round(poke_usu.ataque * poke_compu.defensa, 1)
        poke_compu.vida = round(max(0, poke_compu.vida - dano), 1)
        if poke_compu.vida <= 0:
            log.append(f"Tu {poke_usu.nombre} atacó: ¡{poke_compu.nombre} murió!")
        else:
            puntos_usu += 1
            log.append(f"Tu {poke_usu.nombre} atacó (defensa CPU activa) {poke_compu.nombre} Vida:{poke_compu.vida}")

    elif accion_usu == "atacar" and accion_cpu == "esquivar":
        esquiva = random.choices([True, False],
                                 weights=[poke_compu.velocidad, max(0.01, 1 - poke_compu.velocidad)])[0]
        if esquiva:
            log.append(f"CPU {poke_compu.nombre} esquivó el ataque de tu {poke_usu.nombre}.")
        else:
            poke_compu.vida = round(max(0, poke_compu.vida - poke_usu.ataque), 1)
            if poke_compu.vida <= 0:
                log.append(f"No esquivó ¡{poke_compu.nombre} murió!")
            else:
                puntos_usu += 1
                log.append(f"No esquivó {poke_compu.nombre} Vida:{poke_compu.vida}")

    elif accion_usu == "defender" and accion_cpu == "atacar":
        dano = round(poke_compu.ataque * poke_usu.defensa, 1)
        poke_usu.vida = round(max(0, poke_usu.vida - dano), 1)
        if poke_usu.vida <= 0:
            log.append(f"Tu {poke_usu.nombre} se defendió pero murió.")
        else:
            puntos_compu += 1
            log.append(f"Tu {poke_usu.nombre} se defendió: Vida:{poke_usu.vida}")

    elif accion_usu == "esquivar" and accion_cpu == "atacar":
        esquiva = random.choices([True, False],
                                 weights=[poke_usu.velocidad, max(0.01, 1 - poke_usu.velocidad)])[0]
        if esquiva:
            log.append(f"Tu {poke_usu.nombre} esquivó el ataque de CPU {poke_compu.nombre}.")
        else:
            poke_usu.vida = round(max(0, poke_usu.vida - poke_compu.ataque), 1)
            if poke_usu.vida <= 0:
                log.append(f"No esquivaste: ¡Tu {poke_usu.nombre} murió!")
            else:
                puntos_compu += 1
                log.append(f"No esquivaste: tu {poke_usu.nombre} Vida:{poke_usu.vida}")

    return log, poke_usu, poke_compu, puntos_usu, puntos_compu, accion_cpu


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
    btn_ok = Boton((ANCHO // 2 - 110, 440, 220, 46), "¡A pelear!", fuente_boton)

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
        dibujar_texto(pantalla, "¡Tu pokémon cayó! Elegí el siguiente", fuente_titulo,
                      (255, 90, 90), ANCHO // 2, 50, centrado=True)

        PANEL_W = 280
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
            barra_stat(pantalla, pr.x + 100, pr.y + 40, 100, pok.ataque,       2.15, COLOR_ATK, fuente_pequeña, "ATK")
            barra_stat(pantalla, pr.x + 100, pr.y + 62, 100, pok.defensa,      0.90, COLOR_DEF, fuente_pequeña, "DEF")
            barra_stat(pantalla, pr.x + 100, pr.y + 84, 100, pok.velocidad,    0.90, COLOR_SPD, fuente_pequeña, "SPD")
            barra_stat(pantalla, pr.x + 100, pr.y + 106, 100, pok.adaptabilidad, 1.00, COLOR_ADP, fuente_pequeña, "ADP")
            dibujar_texto(pantalla, f"Vida: {pok.vida:.1f}", fuente_normal, COLOR_SPD, pr.x + 100, pr.y + 132)

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

def pantalla_final(pantalla, ganador, promedio=None, mejor_ronda=None, dict_usu=None, dict_cpu=None):
    """
    Muestra la pantalla de fin de partida.
    ganador: "usuario" | "cpu" | "empate"
    dict_usu, dict_cpu : dict de conteo de acciones (atacar/defender/esquivar/especial)
                         de cada lado. Si se proveen, se muestran botones para abrir
                         los gráficos de torta (analizar_datos.grafico_torta), igual
                         que en la versión de consola.
    Retorna True si el jugador quiere jugar de nuevo, False para salir.
    """
    from src.analizar_datos import grafico_torta

    clock = pygame.time.Clock()
    fuente_titulo  = pygame.font.SysFont("Arial", 40, bold=True)
    fuente_cat     = pygame.font.SysFont("Arial", 20, bold=True)
    fuente_normal  = pygame.font.SysFont("Arial", 16)
    fuente_boton   = pygame.font.SysFont("Arial", 16, bold=True)
    fuente_chica   = pygame.font.SysFont("Arial", 14, bold=True)

    MSGS = {
        "usuario": ("¡Ganaste!", (100, 230, 100)),
        "cpu":     ("Perdiste...", (255, 80, 80)),
        "empate":  ("¡Empate!", (255, 210, 40)),
    }
    msg, color_msg = MSGS.get(ganador, ("Fin de partida", COLOR_TEXTO))

    btn_nuevo = Boton((ANCHO // 2 - 230, ALTO - 70, 200, 50), "Jugar de nuevo", fuente_boton)
    btn_salir  = Boton((ANCHO // 2 + 30,  ALTO - 70, 200, 50), "Salir",           fuente_boton)

    hay_graficos = bool(dict_usu) or bool(dict_cpu)
    btn_grafico_usu = Boton((ANCHO // 2 - 310, 360, 300, 44), "Ver gráfico: tus acciones", fuente_chica)
    btn_grafico_cpu = Boton((ANCHO // 2 +  10, 360, 300, 44), "Ver gráfico: acciones CPU", fuente_chica)

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

            if hay_graficos:
                btn_grafico_usu.actualizar_hover(mouse_pos)
                btn_grafico_cpu.actualizar_hover(mouse_pos)
                if dict_usu and btn_grafico_usu.fue_clickeado(evento):
                    # Igual que en el CLI: abre una ventana de matplotlib (bloqueante
                    # hasta que se cierre) con el porcentaje de acciones del usuario.
                    grafico_torta(dict_usu, "Porcentaje de acciones del Usuario")
                if dict_cpu and btn_grafico_cpu.fue_clickeado(evento):
                    grafico_torta(dict_cpu, "Porcentaje de acciones de la CPU")

        pantalla.fill(COLOR_FONDO)

        # Panel central
        panel = pygame.Rect(ANCHO // 2 - 320, 80, 640, 440)
        dibujar_panel(pantalla, panel, COLOR_PANEL, radio=16, borde=color_msg, grosor_borde=3)

        dibujar_texto(pantalla, msg, fuente_titulo, color_msg, ANCHO // 2, 120, centrado=True)

        if promedio is not None and mejor_ronda is not None and mejor_ronda[1] != 0:
            dibujar_texto(pantalla, f"Promedio de golpes por combate: {promedio:.1f}",
                          fuente_cat, COLOR_TEXTO, ANCHO // 2, 220, centrado=True)
            golpes, num = mejor_ronda
            dibujar_texto(pantalla, f"Mejor combate: {golpes} golpes (pokémon #{num})",
                          fuente_normal, COLOR_SUBTEXTO, ANCHO // 2, 265, centrado=True)
        else:
            dibujar_texto(pantalla, "No derrotaste a ningún pokémon en esta partida.",
                          fuente_normal, COLOR_SUBTEXTO, ANCHO // 2, 240, centrado=True)

        if hay_graficos:
            dibujar_texto(pantalla, "Análisis de acciones de la batalla:", fuente_normal,
                          COLOR_SUBTEXTO, ANCHO // 2, 320, centrado=True)
            if dict_usu:
                btn_grafico_usu.dibujar(pantalla)
            if dict_cpu:
                btn_grafico_cpu.dibujar(pantalla)

        dibujar_texto(pantalla, "¿Querés jugar de nuevo?", fuente_normal, COLOR_SUBTEXTO,
                      ANCHO // 2, ALTO - 130, centrado=True)
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

    CARD_W, CARD_H = 270, 50
    total_w = len(equipo_usu) * CARD_W + (len(equipo_usu) - 1) * 16
    sx = (ANCHO - total_w) // 2
    botones = []
    for i, pok in enumerate(equipo_usu):
        b = Boton((sx + i * (CARD_W + 16), 340, CARD_W, CARD_H),
                  pok.nombre.capitalize(), fuente_boton, tag=pok)
        botones.append(b)

    seleccion = None
    btn_ok     = Boton((ANCHO // 2 - 230, 440, 210, 46), "¡Desempatar!",  fuente_boton)
    btn_empate = Boton((ANCHO // 2 + 20,  440, 210, 46), "Declarar empate", fuente_boton)

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
        dibujar_texto(pantalla, "¡Empate! ¿Querés desempatar?", fuente_titulo,
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
            barra_stat(pantalla, pr.x + 76, pr.y + 38, 90, pok.ataque,    2.15, COLOR_ATK, fuente_pequeña, "ATK")
            barra_stat(pantalla, pr.x + 76, pr.y + 58, 90, pok.defensa,   0.90, COLOR_DEF, fuente_pequeña, "DEF")
            barra_stat(pantalla, pr.x + 76, pr.y + 78, 90, pok.velocidad, 0.90, COLOR_SPD, fuente_pequeña, "SPD")

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
        "nuevo"  : el jugador quiere jugar de nuevo
        "salir"  : el jugador quiere salir
        None     : ventana cerrada
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
    info_rondas  = []

    # Log persistente que se va llenando durante TODA la partida (no se reinicia entre rondas)
    log_global = []

    # Instrucciones iniciales en el log (caben 6 líneas)
    _A = COLOR_BORDE_SEL          # amarillo — encabezados
    _B = COLOR_TEXTO              # blanco   — descripciones
    _G = (100, 220, 130)          # verde    — inicio
    log_global += [
        (">> 3 acciones disponibles:",                              _A),
        ("  Atacar: reducir vida al rival segun tu ataque",         _B),
        ("  Defender: reduce el daño recibido segun tu defensa",   _B),
        ("  Esquivar: chance de esquivar totalmente o recibir el ataque según velocidad",      _B),
        ("  (Si ambos eligen lo mismo: sin ventaja para nadie)",   COLOR_SUBTEXTO),
        (">> iComienza la batalla! iBuena suerte!",                _G),
    ]

    # Diccionarios de conteo de acciones — igual que dict_usu/dict_cpu del CLI original,
    # se usan al final para los gráficos de torta (analizar_datos.grafico_torta)
    dict_usu = {}
    dict_cpu = {}

    # 3. Bucle principal de batalla
    while True:
        res = pantalla_batalla(
            pantalla, poke_usu, poke_compu,
            lista_eventos, puntos_usu, puntos_compu, log_global,
            dict_usu, dict_cpu, ambiente=ambiente
        )
        if res.get("cerrado"):
            return None

        poke_usu     = res["poke_usu"]
        poke_compu   = res["poke_compu"]
        puntos_usu   = res["puntos_usu"]
        puntos_compu = res["puntos_compu"]

        # Estadísticas por ronda — replica exactamente la lógica de funciones.partida():
        # solo se registra una entrada cuando algún pokémon muere en la ronda.
        # El booleano es True salvo que SOLO haya muerto el pokémon del usuario.
        if res["usu_murio"] or res["compu_murio"]:
            if "atacar" in dict_usu:
                golpes = dict_usu["atacar"] + dict_usu.get("especial", 0)
            else:
                golpes = 0
            gano_usu = not (res["usu_murio"] and not res["compu_murio"])
            info_rondas.append([golpes, gano_usu])

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
                # Una sola ronda: si un pokemon muere no hay reemplazos
                bench_usu   = []
                bench_compu = []
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
    seguir = pantalla_final(pantalla, ganador, prom, mejor, dict_usu, dict_cpu)
    return "nuevo" if seguir else "salir"


# ─────────────────────────────────────────────
#  PANTALLA DE ERROR FATAL
# ─────────────────────────────────────────────

def pantalla_error_fatal(pantalla, detalle=""):
    """
    Pantalla que se muestra cuando la carga de pokémones desde la API falla
    (nombre inválido, typo, pokémon inexistente, problema de red, etc).
    Se queda esperando hasta que el usuario cierre la ventana.
    """
    pygame.init()
    if pantalla is None:
        pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Pokémon Battle — Error")

    clock = pygame.time.Clock()
    fuente_titulo = pygame.font.SysFont("Arial", 28, bold=True)
    fuente_normal = pygame.font.SysFont("Arial", 16)
    fuente_chica  = pygame.font.SysFont("Arial", 13)
    fuente_boton  = pygame.font.SysFont("Arial", 15, bold=True)

    btn_cerrar = Boton((ANCHO // 2 - 110, 440, 220, 46), "Cerrar", fuente_boton)

    mensaje_principal = "No se pudo cargar la información de los pokémones."
    mensaje_secundario = (
        "Uno o más nombres configurados no son reconocidos por la base de datos "
        "de pokémones. Por favor, comunicate con el equipo de desarrollo para "
        "que revise la configuración del juego."
    )

    # Partimos el mensaje secundario en líneas que entren en el panel
    import textwrap
    lineas_msg = textwrap.wrap(mensaje_secundario, width=62)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            btn_cerrar.actualizar_hover(pygame.mouse.get_pos())
            if btn_cerrar.fue_clickeado(evento):
                pygame.quit()
                return

        pantalla.fill(COLOR_FONDO)

        panel = pygame.Rect(ANCHO // 2 - 320, 100, 640, 380)
        dibujar_panel(pantalla, panel, COLOR_PANEL, radio=16, borde=(255, 90, 80), grosor_borde=3)

        dibujar_texto(pantalla, "Error al iniciar el juego", fuente_titulo,
                      (255, 110, 100), ANCHO // 2, 130, centrado=True)
        dibujar_texto(pantalla, mensaje_principal, fuente_normal, COLOR_TEXTO,
                      ANCHO // 2, 195, centrado=True)

        y = 235
        for linea in lineas_msg:
            dibujar_texto(pantalla, linea, fuente_normal, COLOR_SUBTEXTO,
                          ANCHO // 2, y, centrado=True)
            y += 24

        if detalle:
            dibujar_texto(pantalla, f"Detalle técnico: {detalle}", fuente_chica,
                          (150, 100, 100), ANCHO // 2, y + 20, centrado=True)

        btn_cerrar.dibujar(pantalla)

        pygame.display.flip()
        clock.tick(60)


def cargar_pokemones_validado(diccio_nombres, pantalla=None):
    """
    Envuelve convertir_diccio() en un try/except para validar que todos los
    nombres de pokémon configurados existan en la PokeAPI antes de seguir.

    Parámetros:
        diccio_nombres : dict   — {"Novatos": [str, ...], ...} con nombres a consultar
        pantalla : Surface|None — si ya hay una ventana abierta, se reutiliza
                                   para mostrar el error; si no, se crea una nueva.

    Retorna:
        dict de objetos Pokemon (igual que convertir_diccio) si todo salió bien.
        Si falla, muestra pantalla_error_fatal() y termina el programa
        (sys.exit) — no retorna nada en ese caso.
    """
    import sys
    from src.pokemones import convertir_diccio

    try:
        return convertir_diccio(diccio_nombres)
    except Exception as e:
        # Cualquier nombre que la PokeAPI no reconozca (typo, pokémon inexistente,
        # error de red, etc.) cae acá. Mostramos un error claro y cerramos.
        pantalla_error_fatal(pantalla, detalle=str(e))
        sys.exit(1)


# ─────────────────────────────────────────────
#  FUNCIÓN DE ENTRADA PRINCIPAL
# ─────────────────────────────────────────────

def run_seleccion(pokemones_obj, mostrar_intro=True):
    """
    Inicializa pygame y muestra la pantalla de selección de equipo.
    Si mostrar_intro=True, antes muestra la pantalla de introducción/instrucciones
    (pensada para la primera partida; en revanchas conviene pasar False).

    Retorna (equipo, pantalla) o (None, pantalla) si el usuario cerró la ventana
    en cualquiera de las dos pantallas.
    """
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Pokémon Battle")

    if mostrar_intro:
        if not pantalla_introduccion(pantalla):
            return None, pantalla

    equipo = pantalla_seleccion(pantalla, pokemones_obj)
    return equipo, pantalla


# ─────────────────────────────────────────────
#  TEST STANDALONE (python app.py)
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))

    from src.clases import Ambiente, Evento_aleatorio

    list_poke = {
        "Novatos": ["magikarp", "sandshrew", "tepig", "pikachu"],
        "Medios": ["wartortle", "marowak", "charmeleon", "luxio"],
        "Altos": ["milotic", "hippowdon", "arcanine", "jolteon"]
    }
    list_cpu = {
        "Novatos": ["magikarp", "sandshrew", "tepig", "pikachu"],
    "Medios": ["wartortle", "marowak", "charmeleon", "luxio"],
    "Altos": ["milotic", "hippowdon", "arcanine", "jolteon"]
    }

    print("Cargando juego...")
    # Carga validada: si algún nombre no es un pokémon real para la API,
    # se muestra una pantalla de error profesional y el programa termina
    # en vez de explotar con un traceback.
    pokemones_usu = cargar_pokemones_validado(list_poke)
    pokemones_cpu = cargar_pokemones_validado(list_cpu)

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
            pokemones_usu = cargar_pokemones_validado(list_poke, pantalla)
            pokemones_cpu = cargar_pokemones_validado(list_cpu, pantalla)
            continue
        else:
            break

    pygame.quit()