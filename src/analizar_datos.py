def promedio(lista):
    """
    Esta funcion analiza los datos de los golpes dados en las rondas.
    Parámetros:
    lista (list). Lista con de los golpes que dio la persona en toda la batalla. Ej. [[2,True],[4,False]...]
    Retorna:
    Promedio (int): con cuantos golpes mato al pokemon adversario en promedio
    Ronda con menor golpes (list): Una lista con la info del minimo de golpes que se dio en la mejor ronda, y el numero de ronda. Ej [2, 4]
    """

    if len(lista)==0:
        return 0, 0
    golpes_matar=[]
    acumulado=0
    poke_matados=0

    for listita in lista:
        if listita[1]:
            golpes_matar.append(listita[0]-acumulado)
            acumulado=listita[0]
            poke_matados+=1
    
    promedio=lista[-1][0]/poke_matados
    minimo=min(golpes_matar)
    posicion = golpes_matar.index(minimo)
    ronda_menos_golpes=[minimo, posicion+1]
    return promedio, ronda_menos_golpes