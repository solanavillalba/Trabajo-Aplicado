from src.clases import Pokemon
from data.api import poke_api

def rango_atributos(dicci):
    '''
    Convierte los valores de los datos del pokemon sacados de la API a rangos entre 0 y 2. Esto es con el objetivo de diferenciar pokemones de niveles bajos, medios y altos.
    Parámetros:
    diccio: dict
        Diccionario con los datos de la API del pokemon elegido. 
        Tiene la siguiente forma: {"pokemon":str,"hp":int,"ataque":int,"defensa":int,"special_attack":int,"adaptabilidad":int,"speed":int,"tipo":str}

    Retorna: dict
    Retorna el mismo diccionario con los valores modificados al rango de 0 y 2.
    '''
    diccio = dicci.copy()
    diccio["hp"]=5
    categoria=''
    rangos={}
    suma= diccio['ataque']+diccio['defensa']+diccio['special_attack']+diccio['adaptabilidad']+diccio['speed']
    
    if suma<300:
        categoria='Novatos'
        
    elif 300<=suma<=400:
        categoria='Medios'
        
    else:
        categoria='Altos'
    
    max_base=140

    if categoria=='Novatos':
        rangos={
            'ataque': (0.10,0.60),
            'special_attack':(0.05,0.30),
            'defensa':(0.05,0.22),
            'speed':(0.05,0.22),
            'adaptabilidad':(0.05,0.25)}
        
    elif categoria=='Medios':
        rangos={
            'ataque': (0.70,1.30),
            'special_attack':(0.35,0.60),
            'defensa':(0.25,0.48),
            'speed':(0.25,0.48),
            'adaptabilidad':(0.30,0.55)}
        
    else:
         rangos = {
            'ataque': (1.40, 2.00),
            'special_attack': (0.70, 1.00),
            'defensa': (0.50, 0.75),
            'speed': (0.50, 0.75),
            'adaptabilidad': (0.60, 0.85)
        }

    for atributo,(mini,maxi) in rangos.items():
        valor_base= diccio.get(atributo, 0)
        valor_escalado=mini+(valor_base/max_base)*(maxi-mini)
        valor_redondeado=round(valor_escalado,2)

        if valor_redondeado>maxi:
            diccio[atributo]=maxi
        elif valor_redondeado<mini:
            diccio[atributo]=mini
        else:
            diccio[atributo]=valor_redondeado

    return diccio

def crear_pokemon(pokemon):
    '''
    Recibe el nombre de un pokemon, hace la consulta a la API, convierte los datos a rangos y devuelve un objeto Pokemon con los atributos correspondientes.
    Parámetros:
    pokemon: str. El nombre del pokemon que se quiere consultar. Debe ser el nombre en ingles y en minuscula.

    Retorna:
    Pokemon: Un objeto Pokemon con los atributos correspondientes al pokemon consultado.
    '''
    try:
        datos_crudos=poke_api(pokemon)
    except:
        raise ValueError(f'Error con {pokemon}')
    else:
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
        try:
            pokemon=crear_pokemon(poke)
        except:
            raise ValueError(f"Error en la posición {lista.index(poke)+1} (Pokémon: {poke})")
                        
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
        try:
            pokemon= str_a_pokemones(valor)
        except ValueError as e:
            raise ValueError(f"Error con el diccionario de los pokemones, en la categoria {clave}. {e}") from None
    
        else:
            dicc[clave]=pokemon
    return dicc
