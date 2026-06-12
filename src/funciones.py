import requests

def poke_api (pokemon):
    '''
    Recibe el nombre de un pokemon, hace la consulta a la API y devuelve un diccionario con los datos crudos del pokemon.
    Parametros:
    pokemon: str.El nombre del pokemon que se quiere consultar. Debe ser el nombre en ingles y en minuscula.
   
   Return:
    dict: un diccionario con los datos crudos del pokemon. Ejemplo:
    {"pokemon": "pikachu", "hp": 35, "ataque": 55, "defensa": 40, "special_attack": 50, "adaptabilidad": 50, "speed": 90, "tipo": "electric"} 
    '''
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}"
    respuesta = requests.get(url)

    if respuesta.status_code != 200:
        raise ValueError(f"Error con {pokemon}")

    datos = respuesta.json()
    stats = {stat["stat"]["name"]: stat["base_stat"]
        for stat in datos["stats"]}
    tipos_lista = [t["type"]["name"] for t in datos["types"]]
    
    fila = {
        "pokemon": pokemon,
        "hp": stats["hp"],
        "ataque": stats["attack"],
        "defensa": stats["defense"],
        "special_attack": stats["special-attack"],
        "adaptabilidad": stats["special-defense"],
        "speed": stats["speed"],
        "tipo": "/".join(tipos_lista)
    }

    return fila



import random
def rango_atributos(diccio):
    '''
    Convierte los valores de los datos del pokemon sacados de la API a rangos entre 0 y 2. Esto es con el objetivo de diferenciar pokemones de niveles bajos, medios y altos.
    Parámetros:
    diccio: dict
        Diccionario con los datos de la API del pokemon elegido. 
        Tiene la siguiente forma: {"pokemon":str,"hp":int,"ataque":int,"defensa":int,"special_attack":int,"adaptabilidad":int,"speed":int,"tipo":str}

    Retorna: dict
    Retorna el mismo diccionario con los valores modificados al rango de 0 y 2.
    '''
    diccio["hp"]=5

    if diccio['ataque'] < 80:
        diccio['ataque']=1
    elif 80<=diccio['ataque']<=110:
        diccio['ataque']=1.5
    else:
        diccio['ataque']=2
    

    if diccio['defensa'] < 80:
        diccio['defensa']=0.75
    elif 80<=diccio['defensa']<=110:
        diccio['defensa']=0.5
    else:
        diccio['defensa']=0.25


    if diccio["special_attack"] < 60:
        diccio["special_attack"]=0.25

    elif 60<=diccio["special_attack"]<=80:
        diccio["special_attack"]=0.5

    else:
        diccio["special_attack"]=1
    
    
    if diccio['speed']< 80:
        diccio['speed']=0.25
    elif 80<=diccio['speed']<=110:
        diccio['speed']=0.5
    else:
        diccio['speed']=0.75
    
    if diccio["adaptabilidad"] < 60:
        diccio["adaptabilidad"]=0
    elif 60<=diccio["adaptabilidad"]<=80:
        diccio["adaptabilidad"]=0.5
    else:
        diccio["adaptabilidad"]=1

    
        
    vida=5

    return diccio

#falta agregar el special attack
def ronda(pokemon1, pokemon2, eventos_random, puntos_cpu=0, puntos_usuario=0):
    """Simula una ronda de batalla entre dos pokemones, teniendo en cuenta sus atributos y eventos aleatorios que pueden afectar el resultado.
    Parámetros:
    pokemon1 (objeto): Un objeto que representa al primer pokemon, con sus atributos.
    pokemon2 (objeto): Un objeto que representa al segundo pokemon, con sus atributos.
    eventos_random (list): Una lista de eventos aleatorios que pueden afectar el resultado de la batalla.
    Retorna:
    pokemon1 (objeto): Luego de pasar por la ronda, con sus atributos actualizados.
    pokemon2 (objeto): Luego de pasar por la ronda, con sus atributos actualizados.
    puntos_cpu (int): Puntos acumulados por la CPU durante la ronda.
    puntos_usuario (int): Puntos acumulados por el usuario durante la ronda.
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
        if pokemon1.vida < 0:
            pokemon1.vida = 0
        print(f"{pokemon2.nombre} atacó a {pokemon1.nombre} y su vida se bajó a {pokemon1.vida}")
        puntos_cpu+=1

        pokemon2.vida-=pokemon1.ataque
        if pokemon2.vida < 0:
            pokemon2.vida = 0
        print(f"{pokemon1.nombre} atacó a {pokemon2.nombre} y su vida se bajó a {pokemon2.vida}")
        puntos_usuario+=1

        if pokemon1.vida == 0 and pokemon2.vida == 0:
            print("Ambos pokemones murieron")
        elif pokemon1.vida == 0:
            print(f"{pokemon1.nombre} murió")
        elif pokemon2.vida == 0:
            print(f"{pokemon2.nombre} murió")

    elif (accion1=="esquivar" or accion1=="defender") and (accion2=="esquivar" or accion2=="defender"):
        print("Ningun pokemon ataco, no se modificó la vida de ninguno")

    elif accion1=="atacar" and accion2=="defender":
        pokemon2.vida-=pokemon1.ataque*pokemon2.defensa
        if pokemon2.vida < 0:
            pokemon2.vida = 0
            print(f"{pokemon1.nombre} atacó a {pokemon2.nombre} y murió")
        else:
            print(f"{pokemon1.nombre} atacó a {pokemon2.nombre} y su vida se bajó a {pokemon2.vida}")
            puntos_usuario+=1

    elif accion1=="atacar" and accion2=="esquivar":
        esquiva_sino = [True, False]
        pesos = [pokemon2.speed, 1-pokemon2.speed]
        seleccion = random.choices(esquiva_sino, weights=pesos, k=1)[0]
        if seleccion:
            print(f"{pokemon2.nombre} esquivó el ataque de {pokemon1.nombre} y su vida se mantuvo en {pokemon2.vida}")   
        else:
            pokemon2.vida-=pokemon1.ataque
            if pokemon2.vida < 0:
                pokemon2.vida = 0
                print(f"{pokemon1.nombre} atacó a {pokemon2.nombre} y murió")
            else:
                print(f"{pokemon1.nombre} atacó a {pokemon2.nombre} y su vida se bajó a {pokemon2.vida}")
                puntos_usuario+=1

    elif accion1=="defender" and accion2=="atacar":
        pokemon1.vida-=pokemon2.ataque*pokemon1.defensa
        if pokemon1.vida < 0:
            pokemon1.vida = 0
            print(f"{pokemon2.nombre} atacó a {pokemon1.nombre} y murió")
        else:
            print(f"{pokemon2.nombre} atacó a {pokemon1.nombre} y su vida se bajó a {pokemon1.vida}")
            puntos_cpu+=1

    elif accion1=="esquivar" and accion2=="atacar":
        esquiva_sino = [True, False]
        pesos = [pokemon1.speed, 1-pokemon1.speed]
        seleccion = random.choices(esquiva_sino, weights=pesos, k=1)[0]
        if seleccion:
            print(f"{pokemon1.nombre} esquivó el ataque de {pokemon2.nombre} y su vida se mantuvo en {pokemon1.vida}")   
        else:
            pokemon1.vida-=pokemon2.ataque
            if pokemon1.vida < 0:
                pokemon1.vida = 0
                print(f"{pokemon2.nombre} atacó a {pokemon1.nombre} y murió")
            else:    
                print(f"{pokemon2.nombre} atacó a {pokemon1.nombre} y su vida se bajó a {pokemon1.vida}")
                puntos_cpu+=1

    return pokemon1, pokemon2, puntos_cpu, puntos_usuario
