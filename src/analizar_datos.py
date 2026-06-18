import matplotlib.pyplot as plt

def promedio(lista):
    """
    Esta funcion analiza los datos de los golpes dados en las rondas.
    Parámetros:
    lista (list). Lista con de los golpes que dio la persona en toda la batalla. Ej. [[2,True],[4,False]...]
    Retorna:
    Promedio (int): con cuantos golpes mato al pokemon adversario en promedio
    Ronda con menor golpes (list): Una lista con la info del minimo de golpes que se dio en la mejor ronda, y el numero de ronda. Ej [2, 4]
    """
    if len (lista)==0:
        return 0, [0, 0]

    golpes_netos_victorias = []
    acumulado_anterior = 0
    conteo_muertos_cpu = 0
    
    for registro in lista:
        murio_rival = registro[1]

        if murio_rival:
            acumulado_actual = registro[0]
            conteo_muertos_cpu += 1
            golpes_netos_victorias.append(acumulado_actual-acumulado_anterior)
            
            acumulado_anterior = acumulado_actual

    if not golpes_netos_victorias:
        return 0, [0, 0]

    total_golpes_efectivos = sum(golpes_netos_victorias)
    cantidad_victorias = conteo_muertos_cpu
    promedio_final = total_golpes_efectivos / cantidad_victorias
    minimo= min(golpes_netos_victorias)

    mejor_encuentro = [minimo, golpes_netos_victorias.index(minimo)+1 ]

    return round(promedio_final, 1), mejor_encuentro

def grafico_torta(diccionario, titulo):
    """
    Genera un gráfico de dona con tipografía moderna unificada y 
    un título en color blanco, haciendo juego con las etiquetas exteriores.
    """
    acciones = list(diccionario.keys())
    cantidades = list(diccionario.values())

    # 1. Colores de los Tipos Pokémon
    colores = []
    for accion in acciones:
        if accion == "atacar":
            colores.append("#FF421C")      # Fuego
        elif accion == "defender":
            colores.append("#2E94FA")    # Agua
        elif accion == "esquivar":
            colores.append("#FAC000")    # Eléctrico
        elif accion == "especial":
            colores.append("#A040A0")    # Psíquico

    desplazamiento = [0.03 for _ in acciones]

    # 2. Configurar fondo oscuro estilo interfaz
    color_fondo = "#1F2326" 
    fig, ax = plt.subplots(figsize=(7, 7), dpi=110, facecolor=color_fondo)
    ax.set_facecolor(color_fondo)
    
    # 3. Configuración de tipografía global
    config_fuente = {"family": "sans-serif", "weight": "black"}

    # 4. Dibujar la dona
    porciones, textos, porcentajes = ax.pie(
        cantidades, 
        labels=[accion.upper() for accion in acciones], 
        colors=colores, 
        explode=desplazamiento,
        autopct="%1.0f%%", 
        startangle=140,                         
        pctdistance=0.75,                        
        wedgeprops={"linewidth": 3, "edgecolor": color_fondo},  
        textprops={"fontsize": 12, **config_fuente}          
    )

    # 5. Círculo central (Dona) con texto interno estilizado
    circulo_central = plt.Circle((0,0), 0.52, fc=color_fondo, ec=color_fondo)
    fig.gca().add_artist(circulo_central)
    
    ax.text(0, 0, "STATS", color="#7F8C8D", fontsize=14, 
            va='center', ha='center', weight="black", family="sans-serif")

    # 6. Estilizar los textos de las categorías exteriores (Blanco puro)
    for texto in textos:
        texto.set_color("#FFFFFF")               
        texto.set_fontsize(13)

    # Estilizar los porcentajes internos (Texto oscuro para máximo contraste)
    for porcentaje in porcentajes:
        porcentaje.set_color("#1F2326")         
        porcentaje.set_fontsize(12)

    # 7. --- CORRECCIÓN AQUÍ: Título con el color blanco del label (#FFFFFF) ---
    ax.set_title(
        titulo.upper(), 
        fontsize=18, 
        pad=30, 
        color="#FFFFFF",  # Mismo color blanco que las etiquetas externas
        fontdict={"family": "sans-serif", "weight": "black"}
    )
    
    plt.tight_layout()
    plt.show()