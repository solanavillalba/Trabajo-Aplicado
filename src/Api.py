import requests

# traduccion de tipos de ingles a español, solo los 4 que usa el juego
# si el tipo del pokemon no esta en este diccionario, no va a funcionar bien con la clase Ambiente
TRADUCCION_TIPOS = {
    "fire":     "fuego",
    "water":    "agua",
    "ground":   "tierra",
    "electric": "electricidad"
}

# los 12 pokemones que vamos a usar en el juego, 3 por cada tipo
# estos nombres tienen que coincidir exactamente con los de la PokeAPI (en minuscula y sin espacios)
POKEMONES = [
    "vaporeon", "gyarados", "greninja",   # agua
    "blaziken", "arcanine", "charizard",  # fuego
    "garchomp", "donphan",  "flygon",     # tierra
    "pikachu",  "luxray",   "jolteon"     # electricidad
]

def obtener_datos_api():
    '''
    Llama a la PokeAPI y devuelve una lista de diccionarios con los datos crudos de cada pokemon.
    Esos datos crudos despues los usa crear_pokemon() para convertirlos a rangos y crear los objetos Pokemon.
    Parametros:
    No recibe parametros.

    Return:
    datos_pokemon: list
    Lista de diccionarios, uno por cada pokemon, con sus datos crudos sin convertir.
    '''
    datos_pokemon = []

    for nombre in POKEMONES:

        # armamos la url con el nombre del pokemon y le pedimos los datos a la PokeAPI
        url = f"https://pokeapi.co/api/v2/pokemon/{nombre}"
        respuesta = requests.get(url)

        # si la API no responde bien (ej: nombre mal escrito) saltamos ese pokemon y seguimos
        if respuesta.status_code != 200:
            print(f"Error al obtener datos de {nombre}, verificá que el nombre sea correcto")
            continue

        # convertimos la respuesta a un diccionario de python para poder acceder a los datos
        datos = respuesta.json()

        # sacamos el primer tipo del pokemon de la API y lo traducimos al español
        # usamos el primero [0] porque algunos pokemon tienen dos tipos (ej: charizard es fire/flying)
        # ese tipo despues lo usa Ambiente.modifica_atributo() para ver si el pokemon esta en su ambiente favorable
        tipo_ingles = datos["types"][0]["type"]["name"]
        tipo_español = TRADUCCION_TIPOS.get(tipo_ingles, tipo_ingles)

        # extraemos los stats que necesitamos del JSON
        # la API los manda como una lista, los convertimos a diccionario para accederlos por nombre
        stats = {stat["stat"]["name"]: stat["base_stat"] for stat in datos["stats"]}

        # armamos el diccionario con todos los datos del pokemon
        # estos valores son los CRUDOS de la API (ej: ataque=95), todavia no convertidos a rangos
        # crear_pokemon() los va a pasar por rango_atributos() para convertirlos a 1/1.5/2 etc.
        fila = {
            "nombre":          nombre,         # lo usa self.nombre en la clase Pokemon
            "tipo":            tipo_español,   # lo usa self.tipo en la clase Pokemon y Ambiente.modifica_atributo()
            "hp":              stats["hp"],              # lo convierte rango_atributos()  siempre queda en 5 (self.vida)
            "ataque":          stats["attack"],          # lo convierte rango_atributos()  1/1.5/2 (self.ataque) usado en Ronda()
            "defensa":         stats["defense"],         # lo convierte rango_atributos()  0.75/0.5/0.25 (self.defensa) usado en Ronda()
            "speed":           stats["speed"],           # lo convierte rango_atributos()  0.25/0.5/0.75 (self.speed) usado en Ronda()
            "special_defense": stats["special-defense"] # lo convierte rango_atributos()  0/0.5/1 (self.adaptabilidad) usado en Ambiente()
        }

        datos_pokemon.append(fila)
        print(f"{nombre} obtenido. del tipo: {tipo_español} , ataque: {stats['attack']} defensa : {stats['defense']}")

    return datos_pokemon


def crear_pokemon(datos_crudos):
    '''
    Recibe el diccionario con los datos crudos de un pokemon de la API,
    los convierte a rangos con rango_atributos() y devuelve un objeto Pokemon listo para jugar.
    Esta funcion conecta la API con la clase Pokemon.
    Parametros:
    datos_crudos: dict
    Diccionario con los datos crudos del pokemon, tal como lo devuelve obtener_datos_api().

    Return:
    Pokemon: objeto de la clase Pokemon con sus atributos ya convertidos a rangos.
    '''
    # rango_atributos() convierte los valores crudos de la API a los rangos que usa el juego
    # ej: ataque=95 (crudo) → ataque=1.5 (Medio) que es lo que usa Ronda() para calcular el daño
    ataque_conv, defensa_conv, speed_conv, adaptabilidad_conv, vida_conv = rango_atributos(
        datos_crudos["ataque"],          # valor crudo  se convierte a 1/1.5/2
        datos_crudos["defensa"],         # valor crudo  se convierte a 0.75/0.5/0.25
        datos_crudos["speed"],           # valor crudo  se convierte a 0.25/0.5/0.75
        datos_crudos["special_defense"], # valor crudo  se convierte a 0/0.5/1
        datos_crudos["hp"]               # valor crudo  siempre queda en 5
    )

    # creamos el objeto Pokemon con los valores ya convertidos a rangos
    # a partir de aca el pokemon esta listo para que el jugador le modifique un atributo y juegue
    return Pokemon(
        nombre        = datos_crudos["nombre"],
        tipo          = datos_crudos["tipo"],
        vida          = vida_conv,          # siempre 5
        ataque        = ataque_conv,        # 1, 1.5 o 2
        defensa       = defensa_conv,       # 0.75, 0.5 o 0.25
        speed         = speed_conv,         # 0.25, 0.5 o 0.75
        adaptabilidad = adaptabilidad_conv  # 0, 0.5 o 1
    )
