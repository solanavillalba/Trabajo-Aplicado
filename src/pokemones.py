import requests
from clases import Pokemon


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
    return diccio

def crear_pokemon(pokemon):
    '''
    Recibe el nombre de un pokemon, hace la consulta a la API, convierte los datos a rangos y devuelve un objeto Pokemon con los atributos correspondientes.
    Parámetros:
    pokemon: str. El nombre del pokemon que se quiere consultar. Debe ser el nombre en ingles y en minuscula.

    Retorna:
    Pokemon: Un objeto Pokemon con los atributos correspondientes al pokemon consultado.
    '''
    datos_crudos=poke_api(pokemon)
    datos_casteados=rango_atributos(datos_crudos)
    poke_creado=Pokemon(datos_casteados)

    return poke_creado


def str_a_pokemones(lista):
    '''
    Recibe una lista con los nombres de los pokemones y los convierte a objetos
    Parámetros:
    lista: list. Lista con los nombres de los pokemones elegidos por el usuario
    Return
    lista: list. Lista con objetos Pokemon con los atributos correspondientes a los pokemones elegidos por el usuario.
    '''
    
    lis=[]
    for poke in lista:
        pokemon=crear_pokemon(poke)
        lis.append(pokemon)
    return lis

def convertir_diccio(diccio):
    '''
    Recibe un diccionario con los values que son lista de pokemones
    Parámetros:
    diccio: dict. Diccionario con los datos de la API del pokemon elegido
    Return
    dicc: diccionario. diccionario con objetos Pokemon ordenados en las claves correspondientes.
    '''
    
    dicc={}
    for clave, valor in diccio.items():
        pokemon= str_a_pokemones(valor)
        dicc[clave]=pokemon
    return dicc

