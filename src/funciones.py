import random

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

def Ronda(pokemon1, pokemon2, eventos_random):
    """Simula una ronda de batalla entre dos pokemones, teniendo en cuenta sus atributos y eventos aleatorios que pueden afectar el resultado.
    Parámetros:
    pokemon1 (objeto): Un objeto que representa al primer pokemon, con sus atributos.
    pokemon2 (objeto): Un objeto que representa al segundo pokemon, con sus atributos.
    eventos_random (list): Una lista de eventos aleatorios que pueden afectar el resultado de la batalla.
    Retorna:
    pokemon1 (objeto): Luego de pasar por la ronda, con sus atributos actualizados.
    pokemon2 (objeto): Luego de pasar por la ronda, con sus atributos actualizados..
    """
    accion1=input("¿Qué acción quieres realizar? (atacar, defender o esquivar) ")
    accion2= random.choice(["atacar", "defender", "esquivar"])
    evento_si_no= random.choice([True, False])
    if evento_si_no:
        evento_quepasa= random.choice(eventos_random)
        poke_afectado= random.choice([pokemon1, pokemon2])
        evento_quepasa.evento(poke_afectado)