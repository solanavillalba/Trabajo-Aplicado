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
    Esta función genera un gráfico de torta a partir del registro
    de acciones realizadas durante la batalla.
     
    Parámetro:
    diccionario (dict): registro de acciones
    titulo (str): título del gráfico
        Parámetro:
        diccionario (dict): registro de acciones
        titulo (str): título del gráfico
    """

    acciones = []

    for accion in diccionario.keys():
        acciones.append(accion)

    cantidades = []

    for cantidad in diccionario.values():
        cantidades.append(cantidad)

    colores = []

    for accion in acciones:

        if accion == "atacar":
            colores.append("red")

        elif accion == "defender":
             colores.append("blue")

        elif accion == "esquivar":
             colores.append("orange")

        elif accion == "especial":
             colores.append("purple")

    plt.figure()

    plt.pie(cantidades, labels=acciones, colors=colores, autopct="%1.0f%%")

    plt.title(titulo)
    plt.show()