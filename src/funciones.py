import random
from pokemones import crear_pokemon

#falta agregar el special attack
def ronda(pokemon1, pokemon2, eventos_random, puntos_usuario=0, puntos_cpu=0):
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
        pesos = [pokemon2.velocidad, 1-pokemon2.velocidad]
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
        pesos = [pokemon1.velocidad, 1-pokemon1.velocidad]
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

    return pokemon1, pokemon2, puntos_usuario, puntos_cpu

def partida(equipo_usu,equipo_compu,lista_eventos,lista_ambientes):
    '''
    Mantiene a los pokemons batallando (llama a la función ronda() hasta que uno muera. Cuando eso sucede, 
    el usuario o la computadora pueden elegir alguno de los otros pokemones previamente seleccionados para 
    seguir batallando, aquel que mantuvo su pokemon con vida lo va a seguir utilizando hasta que muera. 
    Esto continuará hasta que uno de los dos equipos se quede sin pokemones con vida.

    Parámetros:
    equipo_usu: list
    Lista compuesta con los tres pokemones que el usuario va a utilizar en su equipo (los pokemones son objetos).

    equipo_compu: list
    Lista compuesta por los tres pokemones que la computadora va a utilzar en su equipo (los pokemones son objetos).

    lista_eventos: list
    Lista con eventos aleatorios que pueden suceder durante la partida.

    lista_ambientes: list
    Lista con los ambientes (objetos) donde transcurrirá la batalla. Estos ambientes pueden favorecer o perjudicar
    a los pokemones según sean del mismo tipo o no. 
    ambiente: Ambiente
    Objeto del tipo Ambiente el cual modificará los atributos de los pokemones según sean del mismo tipo 
    (favoreciéndolos) o no (perjudicándolos).

    Retorna: no retorna nada

    '''
    #Consigo solo los nombres de los objetos pokemones
    pokemones_usu=[None]
    for pokemon in equipo_usu:
        pokemones_usu.append(pokemon.nombre.lower())

     #Se elige el primer pokemon para empezar la batalla.
    poke_usu=input("Ingrese el nombre del pokemon con el que quiera empezar: ").lower().strip()

    #valido que esté bien ingresado el nombre
    while poke_usu not in pokemones_usu[1:]:
        print("El pokemon ingresado no se encuentra en su equipo. Inténtelo de nuevo.")
        poke_usu=input("Ingrese el nombre del pokemon con el que quiera empezar: ").lower().strip()
    
    pokemones_usu.remove(poke_usu) #saco de la lista el nombre del pokemon, asi no lo repite
    
    #convierto el str primer_poke_usu a objeto
    for pokemon in equipo_usu:
        if pokemon.nombre.lower()==poke_usu:
            poke_usu=pokemon
            break

    
    #Hago lo mismo con los de la compu
    pokemones_compu=[None]
    for pokemon in equipo_compu:
        pokemones_compu.append(pokemon.nombre.lower())

    poke_compu=random.choice(pokemones_compu[1:])
    pokemones_compu.remove(poke_compu)

    for pokemon in equipo_compu:
        if pokemon.nombre.lower()==poke_compu:
            poke_compu=pokemon
            break

    puntos_usu=0
    puntos_compu=0

    #Se elige aleatoriamente el ambiente en el que ocurrirá la batalla.
    ambiente=random.choice(lista_ambientes)
    print(f"Ambiente seleccionado al azar: {ambiente.nombre}")
    ambiente.modifica_atributo(poke_usu)
    ambiente.modifica_atributo(poke_compu, True)
    
    while True:
        post_usu,post_compu,puntos_usu,puntos_compu=ronda(poke_usu,poke_compu,lista_eventos,puntos_usu,puntos_compu)

        cond_salida_usu=post_usu.vida==0 and len(pokemones_usu)==1
        cond_salida_compu=post_compu.vida==0 and len(pokemones_compu)==1

        if cond_salida_usu ==True and cond_salida_compu==True:
            resultado=empate(equipo_usu,equipo_compu)
            if type(resultado)==str:
                print(resultado)
                break
            else:
                poke_usu=resultado[0]
                poke_compu=resultado[1]
                poke_usu.vida=5
                poke_compu.vida=5
                continue
        elif cond_salida_usu==True:
            print("La batalla ha finalizado. La computadora se consagra como ganadora.")
            break
        elif cond_salida_compu==True:
            print("La batalla ha finalizado. Te has consgrado como ganador. ¡Felicitaciones!")
            break


        if post_usu.vida!=0 and post_compu.vida!=0:
            poke_usu=post_usu
            poke_compu=post_compu
            continue
    
        elif post_usu.vida==0 and post_compu.vida!=0:
            poke_usu=input(f"Como {post_usu.nombre} murió, elija su siguiente pokemon para batallar de nuevo: ").lower().strip()
            while poke_usu not in pokemones_usu[1:]:
                print("El pokemon ingresado no se encuentra en su equipo. Inténtelo de nuevo.")
                poke_usu=input("Elija su siguiente pokemon para batallar de nuevo: ").lower().strip()
            
            pokemones_usu.remove(poke_usu) #saco de la lista el nombre del pokemon, asi no lo repite
            for pokemon in equipo_usu:
                if pokemon.nombre.lower()==poke_usu:
                    poke_usu=pokemon
                    break

        elif post_usu.vida!=0 and post_compu.vida==0:
            print(f"Como {post_compu.nombre} murió. Se elegirá el siguiente pokemon para batallar de nuevo")
            poke_compu=random.choice(pokemones_compu[1:])

            pokemones_compu.remove(poke_compu)
            for pokemon in equipo_compu:
                if pokemon.nombre.lower()==poke_compu:
                    poke_compu=pokemon
                    break
    
        else:
            print("Se elegirán los siguientes pokemones a batallar")
            poke_usu=input("Ingrese su siguiente pokemon para batallar de nuevo: ").lower().strip()
            while poke_usu not in pokemones_usu[1:]:
                print("El pokemon ingresado no se encuentra en su equipo. Inténtelo de nuevo.")
                poke_usu=input("Elija su siguiente pokemon para batallar de nuevo: ").lower().strip()
            
            pokemones_usu.remove(poke_usu) #saco de la lista el nombre del pokemon, asi no lo repite
            for pokemon in equipo_usu:
                if pokemon.nombre.lower()==poke_usu:
                    poke_usu=pokemon
                    break

            poke_compu=random.choice(pokemones_compu[1:])
            pokemones_compu.remove(poke_compu)

            for pokemon in equipo_compu:
                if pokemon.nombre.lower()==poke_compu:
                    poke_compu=pokemon
                    break

def empate(equipo_usu,equipo_compu):
    '''
    Si ocurre un empate (todos los pokemones de ambos equipos se encuentran sin vida), esta función se encarga de darle dos opciones al usuario. Si desea dejarlo como un
    empate, lo deja como un empate. Sino, da la opción de revivir a ambos equipos uno de los pokemones y volver a batallar.

    Parámetros:
    equipo_usu: list
    Lista de objetos con el equipo de pokemones del usuario.

    equipo_compu: list
    Lista de objetos con el equipo de pokemones de la computadora.

    Retorna: str o dos objetos de tipo pokemon
    Si el usuario decide dejar el final de la partida como un empate, devuelve un mensaje sobre el empate. Si no, devuelve los pokemones que van a usar la computadora y el usuario para
    batallar de nuevo.

    '''
    opcion=input("¡Ocurrió un empate! ¿Desea terminar la partida? (s/n): ").lower().strip()

    while opcion not in ['s','n']:
        print("Opción inválida")
        opcion=input("Intente de nuevo").lower().strip

    if opcion=='s':
        return "El juego ha finalizado. Fue un empate."

    else:
        pokemons_usu=[None]
        for pokemon in equipo_usu:
            pokemons_usu.append(pokemon.nombre.lower())
            
        #Se elige el primer pokemon para empezar la batalla.
        poke_usu=input("Ingrese el nombre del pokemon que quiere revivir: ").lower().strip()
        
        #valido que esté bien ingresado el nombre
        while poke_usu not in pokemons_usu[1:]:
            print("El pokemon ingresado no se encontraba en su equipo. Inténtelo de nuevo.")
            poke_usu=input("Ingrese el nombre del pokemon que quiere revivir: ").lower().strip()
        pokemons_usu.remove(poke_usu) #saco de la lista el nombre del pokemon, asi no lo repite
        
        #convierto el str primer_poke_usu a objeto
        for pokemon in equipo_usu:
            if pokemon.nombre.lower()==poke_usu:
                poke_usu=pokemon
                break
        #Hago lo mismo con los de la compu
        pokemons_compu=[None]
        for pokemon in equipo_compu:
            pokemons_compu.append(pokemon.nombre.lower())
            
        poke_compu=random.choice(pokemons_compu[1:])
        pokemons_compu.remove(poke_compu)
        
        for pokemon in equipo_compu:
            if pokemon.nombre.lower()==poke_compu:
                poke_compu=pokemon
                break
        return [poke_usu,poke_compu]

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

def validar_rango(numero, mini, maxi):
    if (numero > maxi) or (numero < mini):
        raise ValueError("El numero no esta en el rango solicitado.")
    
def validar_int(numero):
    try: 
        numero = int(numero)
    except:
        raise ValueError("Debe ingresar un número.")
    
def validar_str(texto):
    try:
        str(texto)
    except:
        raise ValueError("Debe ingresar un texto.")

def validar_texto_en_lista(texto, lista):
    if texto not in lista:
        raise ValueError("Debe ingresar uno de los elementos de la lista.")
    


