import random
def rango_atributos(ataque, defensa,speed,special_defense,vida):
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
        defensa=0.5
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
    pokemon2 (objeto): Luego de pasar por la ronda, con sus atributos actualizados.
    """
    accion1= input("¿Qué acción quieres realizar? (atacar, defender o esquivar) ").lower().strip()
    
    while accion1 not in ["atacar", "defender", "esquivar"]:
        print("Acción no válida. Por favor, elige entre atacar, defender o esquivar.")
        accion1= input("¿Qué acción quieres realizar? (atacar, defender o esquivar) ").lower().strip()

    accion2= random.choice(["atacar", "defender", "esquivar"])
    evento_si_no= random.choice([True, False])
    if evento_si_no:
        evento_quepasa= random.choice(eventos_random)
        poke_afectado= random.choice([pokemon1, pokemon2])
        evento_quepasa.evento(poke_afectado)
    
    if accion1=="atacar" and accion2=="atacar":
        pokemon1.vida-=pokemon2.ataque
        print(f"{pokemon2.nombre} atacó a {pokemon1.nombre} y su vida se modificó a {pokemon1.vida}")
        pokemon2.vida-=pokemon1.ataque
        print(f"{pokemon1.nombre} atacó a {pokemon2.nombre} y su vida se modificó a {pokemon2.vida}")

    elif (accion1=="esquivar" or accion1=="defender") and (accion2=="esquivar" or accion2=="defender"):
        print("Ningun pokemon ataco, no se modificó la vida de ninguno")

    elif accion1=="atacar" and accion2=="defender":
        pokemon2.vida-=pokemon1.ataque*pokemon2.defensa
        print(f"{pokemon1.nombre} atacó a {pokemon2.nombre} y su vida se modificó a {pokemon2.vida}")

    elif accion1=="atacar" and accion2=="esquivar":
        esquiva_sino = [True, False]
        pesos = [pokemon2.speed, 1-pokemon2.speed]
        seleccion = random.choices(esquiva_sino, weights=pesos, k=1)[0]
        if seleccion:
            print(f"{pokemon2.nombre} esquivó el ataque de {pokemon1.nombre} y su vida se mantuvo en {pokemon2.vida}")   
        else:
            pokemon2.vida-=pokemon1.ataque
            print(f"{pokemon1.nombre} atacó a {pokemon2.nombre} y su vida se modificó a {pokemon2.vida}")

    elif accion1=="defender" and accion2=="atacar":
        pokemon1.vida-=pokemon2.ataque*pokemon1.defensa
        print(f"{pokemon2.nombre} atacó a {pokemon1.nombre} y su vida se modificó a {pokemon1.vida}")

    elif accion1=="esquivar" and accion2=="atacar":
        esquiva_sino = [True, False]
        pesos = [pokemon1.speed, 1-pokemon1.speed]
        seleccion = random.choices(esquiva_sino, weights=pesos, k=1)[0]
        if seleccion:
            print(f"{pokemon1.nombre} esquivó el ataque de {pokemon2.nombre} y su vida se mantuvo en {pokemon1.vida}")   
        else:
            pokemon1.vida-=pokemon2.ataque
            print(f"{pokemon2.nombre} atacó a {pokemon1.nombre} y su vida se modificó a {pokemon1.vida}")

    if pokemon1.vida < 0:
        pokemon1.vida = 0
    if pokemon2.vida < 0:
        pokemon2.vida = 0

    return pokemon1, pokemon2
