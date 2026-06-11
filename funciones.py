def rango_atributos(ataque,defensa,speed,special_defense,vida):
    '''
    Convierte los valores de los atributos del pokemon a rangos entre 0 y 2 para diferenciar atributos de nivel bajo, medio o alto.

    Parámetros:

    '''
    if ataque < 80:
        ataque=1
    elif 80<=ataque<=110:
        ataque=1.5
    else:
        ataque=2
    
    if defensa < 80:
        defensa=0.75
    elif 80<=defensa<=110:
        ataque=0.5
    else:
        defensa=0.25
    
    if speed< 80:
        speed=0.25
    elif 80<=speed<=110:
        speed=0.5
    else:
        speed=0.75
    
    if special_defense < 60:
        special_defense=0
    elif 60<=special_defense<=80:
        special_defense=0.5
    else:
        special_defense=1
        
    vida=5

    return ataque,defensa,speed,special_defense,vida