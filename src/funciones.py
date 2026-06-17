import random
from src.pokemones import crear_pokemon

def ronda(pokemon1, pokemon2, eventos_random, dict_usu, dict_cpu, puntos_usuario=0, puntos_cpu=0):
    """Simula una ronda de batalla entre dos pokemones, teniendo en cuenta sus atributos y eventos aleatorios que pueden afectar el resultado.
    Parámetros:
    
    pokemon1 (objeto): Un objeto que representa al primer pokemon, con sus atributos.
    pokemon2 (objeto): Un objeto que representa al segundo pokemon, con sus atributos.
    eventos_random (list): Una lista de eventos aleatorios que pueden afectar el resultado de la batalla.
    puntos_usuario (int): Puntos acumulados por el usuario durante la ronda.
    puntos_cpu (int): Puntos acumulados por la CPU durante la ronda.
    dict_usu (dict): Diccionario de registro de las acciones del usuario.
    dict_cpu (dict): Diccionario de registro de las acciones de la CPU.
    
    Retorna:
    pokemon1 (objeto): Luego de pasar por la ronda, con sus atributos actualizados.
    pokemon2 (objeto): Luego de pasar por la ronda, con sus atributos actualizados.
    puntos_cpu (int): Puntos acumulados por la CPU durante la ronda.
    puntos_usuario (int): Puntos acumulados por el usuario durante la ronda.
    dict_usu (dict): Diccionario de registro de las acciones del usuario actualizado con la acción realizada en esta ronda.
    dict_cpu (dict): Diccionario de registro de las acciones de la CPU actualizado con la acción realizada en esta ronda.
    """
    if puntos_usuario>=3:
        if puntos_usuario >= 3:
            print("\n¡ATAQUE ESPECIAL DISPONIBLE! Tuviste una racha de 3 ataques exitosos. Desbloqueaste el ataque especial")
            accion1= input("\n¿Qué acción quieres realizar? (atacar, defender, esquivar o especial) ").lower().strip()
        
        while accion1 not in ["atacar", "defender", "esquivar", "especial"]:
            print("\nAcción no válida. Por favor, elige entre atacar, defender, esquivar o especial.")
            accion1= input("\n¿Qué acción quieres realizar? (atacar, defender, esquivar o especial) ").lower().strip()
    else:
        accion1= input("\n¿Qué acción quieres realizar? (atacar, defender o esquivar) ").lower().strip()
        
        while accion1 not in ["atacar", "defender", "esquivar"]:
            print("\nAcción no válida. Por favor, elige entre atacar, defender o esquivar.")
            accion1= input("\n¿Qué acción quieres realizar? (atacar, defender o esquivar) ").lower().strip()
    
    if accion1=="especial":
        puntos_usuario=0

    if accion1 not in dict_usu:
        dict_usu[accion1]=1
    else:
        dict_usu[accion1]+=1

    if puntos_cpu>=3:
        accion2= random.choice(["atacar", "defender", "esquivar", "especial"])
    else:
        accion2= random.choice(["atacar", "defender", "esquivar"])
    
    if accion2=="especial":
        puntos_cpu=0

    if accion2 not in dict_cpu:
        dict_cpu[accion2]=1
    else:
        dict_cpu[accion2]+=1

    if accion2!="especial" and accion1!="especial":    
        evento_si_no= random.choice([True, False])
        if evento_si_no:
            evento_quepasa= random.choice(eventos_random)
            poke_afectado= random.choice([pokemon1, pokemon2])
            evento_quepasa.evento(poke_afectado)
            if poke_afectado.vida==0:
                print(f"{poke_afectado.nombre} murió.")
                return pokemon1, pokemon2, puntos_usuario, puntos_cpu, dict_usu, dict_cpu

    
    if accion1=="especial" and accion2!="especial":
        pokemon2.vida-= (pokemon1.ataque*(pokemon1.special_attack+1))
        pokemon2.vida=round(pokemon2.vida, 1)
        if pokemon2.vida <= 0.0:
            pokemon2.vida = 0.0
            print(f"\nTu {pokemon1.nombre} usó su ataque especial en el {pokemon2.nombre} de la cpu y murió")
        else:
            print(f"\nTu {pokemon1.nombre} usó su ataque especial en el {pokemon2.nombre} de la cpu y su vida se bajó a {pokemon2.vida}")
            puntos_usuario+=1
    
    elif accion2=="especial" and accion1!="especial":
        pokemon1.vida-= (pokemon2.ataque*(pokemon2.special_attack+1))
        pokemon1.vida=round(pokemon1.vida, 1)
        if pokemon1.vida <= 0.0:
            pokemon1.vida = 0.0
            print(f"\nEl {pokemon2.nombre} de la cpu usó su ataque especial en tu {pokemon1.nombre} y murió")
        else:
            print(f"\nEl {pokemon2.nombre} de la cpu usó su ataque especial en tu {pokemon1.nombre} y su vida se bajó a {pokemon1.vida}")
            puntos_cpu+=1
    
    elif accion1=="especial" and accion2=="especial":
        pokemon1.vida-= (pokemon2.ataque*(pokemon2.special_attack+1))
        pokemon1.vida=round(pokemon1.vida, 1)
        pokemon2.vida-= (pokemon1.ataque*(pokemon1.special_attack+1))
        pokemon2.vida=round(pokemon2.vida, 1)
        if pokemon1.vida <= 0.0:
            pokemon1.vida = 0.0
            print(f"\nEl {pokemon2.nombre} de la cpu usó su ataque especial en tu {pokemon1.nombre} y murió")
        else:
            print(f"\nEl {pokemon2.nombre} de la cpu usó su ataque especial en tu {pokemon1.nombre} y su vida se bajó a {pokemon1.vida}")
            puntos_cpu+=1

        if pokemon2.vida <= 0.0:
            pokemon2.vida = 0.0
            print(f"\nTu {pokemon1.nombre} usó su ataque especial en el {pokemon2.nombre} de la cpu y murió")
        else:
            print(f"\nTu {pokemon1.nombre} usó su ataque especial en el {pokemon2.nombre} de la cpu y su vida se bajó a {pokemon2.vida}")
            puntos_usuario+=1

    elif accion1=="atacar" and accion2=="atacar":
        pokemon1.vida-=pokemon2.ataque
        pokemon1.vida=round(pokemon1.vida, 1)
        if pokemon1.vida <= 0.0:
            pokemon1.vida = 0.0
        print(f"\nEl {pokemon2.nombre} de la cpu atacó a tu {pokemon1.nombre} y su vida se bajó a {pokemon1.vida}")
        puntos_cpu+=1

        pokemon2.vida-=pokemon1.ataque
        pokemon2.vida=round(pokemon2.vida, 1)
        
        if pokemon2.vida <= 0.0:
            pokemon2.vida = 0.0
        print(f"Tu {pokemon1.nombre} atacó al {pokemon2.nombre} de la cpu y su vida se bajó a {pokemon2.vida}")
        puntos_usuario+=1

        if pokemon1.vida == 0.0 and pokemon2.vida == 0.0:
            print("\nAmbos pokemones murieron")
        elif pokemon1.vida == 0.0:
            print(f"\n{pokemon1.nombre} murió")
        elif pokemon2.vida == 0.0:
            print(f"\n{pokemon2.nombre} murió")

    elif (accion1=="esquivar" or accion1=="defender") and (accion2=="esquivar" or accion2=="defender"):
        print("\nNingún pokemon atacó, no se modificó la vida de ninguno")

    elif accion1=="atacar" and accion2=="defender":
        pokemon2.vida-=pokemon1.ataque*pokemon2.defensa
        pokemon2.vida=round(pokemon2.vida, 1)

        if pokemon2.vida <= 0.0:
            pokemon2.vida = 0.0
            print(f"\nTu {pokemon1.nombre} atacó al {pokemon2.nombre} de la cpu y murió")
        else:
            print(f"\nTu {pokemon1.nombre} atacó al {pokemon2.nombre} de la cpu y su vida se bajó a {pokemon2.vida}")
            puntos_usuario+=1

    elif accion1=="atacar" and accion2=="esquivar":
        esquiva_sino = [True, False]
        pesos = [pokemon2.velocidad, 1-pokemon2.velocidad]
        seleccion = random.choices(esquiva_sino, weights=pesos, k=1)[0]
        if seleccion:
            print(f"\nEl {pokemon2.nombre} de la cpu esquivó el ataque de tu {pokemon1.nombre} y su vida se mantuvo en {pokemon2.vida}")   
        else:
            pokemon2.vida-=pokemon1.ataque
            pokemon2.vida=round(pokemon2.vida, 1)
            if pokemon2.vida <= 0.0:
                pokemon2.vida = 0.0
                print(f"\nTu {pokemon1.nombre} atacó al {pokemon2.nombre} de la cpu y murió")
            else:
                print(f"\nTu {pokemon1.nombre} atacó al {pokemon2.nombre} de la cpu y su vida se bajó a {pokemon2.vida}")
                puntos_usuario+=1

    elif accion1=="defender" and accion2=="atacar":
        pokemon1.vida-=pokemon2.ataque*pokemon1.defensa
        pokemon1.vida=round(pokemon1.vida, 1)

        if pokemon1.vida <= 0.0:
            pokemon1.vida = 0.0
            print(f"\nEl {pokemon2.nombre} de la cpu atacó a tu {pokemon1.nombre} y murió")
        else:
            print(f"\nEl {pokemon2.nombre} de la cpu atacó a tu {pokemon1.nombre} y su vida se bajó a {pokemon1.vida}")
            puntos_cpu+=1

    elif accion1=="esquivar" and accion2=="atacar":
        esquiva_sino = [True, False]
        pesos = [pokemon1.velocidad, 1-pokemon1.velocidad]
        seleccion = random.choices(esquiva_sino, weights=pesos, k=1)[0]
        if seleccion:
            print(f"\nTu {pokemon1.nombre} esquivó el ataque del {pokemon2.nombre} de la cpu y su vida se mantuvo en {pokemon1.vida}")   
        else:
            pokemon1.vida-=pokemon2.ataque
            pokemon1.vida=round(pokemon1.vida, 1)
            if pokemon1.vida <= 0.0:
                pokemon1.vida = 0.0
                print(f"\nEl {pokemon2.nombre} de la cpu atacó a tu {pokemon1.nombre} y murió")
            else:    
                print(f"\nEl {pokemon2.nombre} de la cpu atacó a tu {pokemon1.nombre} y su vida se bajó a {pokemon1.vida}")
                puntos_cpu+=1

    return pokemon1, pokemon2, dict_usu, dict_cpu, puntos_usuario, puntos_cpu

def partida(equipo_usu,equipo_compu,lista_eventos,lista_ambientes):
    '''
    Mantiene a los pokemons batallando (llama a la función ronda()) hasta que uno muera. Cuando eso sucede, 
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
    pokemones_usu=[]
    for pokemon in equipo_usu:
        pokemones_usu.append(pokemon.nombre.lower())

    #Se elige aleatoriamente el ambiente en el que ocurrirá la batalla.
    ambiente=random.choice(lista_ambientes)
    print(f"Ambiente seleccionado: {ambiente.nombre}\n")
    
    print("Tus pokemones se están adaptando al ambiente...\n")
    for pok in equipo_usu: 
        ambiente.modifica_atributo(pok)
        pok.mostrar_atributos(False)
    
    print("\nLos pokemones de la cpu se están adaptando al ambiente...\n")
    for po in equipo_compu:
        ambiente.modifica_atributo(po, True)
        po.mostrar_atributos(False)
    
     #Se elige el primer pokemon para empezar la batalla.
    print("\nEmpieza la pelea.\n\nTu equipo está conformado por: ", pokemones_usu)
    poke_usu=input("Ingrese el nombre del pokemon con el que quiera empezar a pelear: ").lower().strip()

    #valido que esté bien ingresado el nombre
    while poke_usu not in pokemones_usu:
        print("El pokemon ingresado no se encuentra en su equipo. Inténtelo de nuevo.")
        poke_usu=input("Ingrese el nombre del pokemon con el que quiera empezar a pelear: ").lower().strip()
    
    pokemones_usu.remove(poke_usu) #saco de la lista el nombre del pokemon, asi no lo repite
    
    #convierto el str primer_poke_usu a objeto
    for pokemon in equipo_usu:
        if pokemon.nombre.lower()==poke_usu:
            poke_usu=pokemon
            break

    
    #Hago lo mismo con los de la compu
    pokemones_compu=[]
    for pokemon in equipo_compu:
        pokemones_compu.append(pokemon.nombre.lower())

    poke_compu=random.choice(pokemones_compu)
    pokemones_compu.remove(poke_compu)

    for pokemon in equipo_compu:
        if pokemon.nombre.lower()==poke_compu:
            poke_compu=pokemon
            print(f"\nLa cpu eligió a {poke_compu.nombre}")
            break

    puntos_usu=0
    puntos_compu=0

    dict_usu={}
    dict_compu={}
    info_rondas=[]
    print("\nTus pokemones pueden hacer 3 acciones:\nAtacar: El pokemon ataca al otro pokemon y le baja vida según su ataque. Si ambos pokemones atacan, se bajan vida mutuamente.\nDefender: El pokemon se defiende del ataque del otro pokemon, y le baja menos vida según su defensa. Si ambos pokemones se defienden, no se baja vida a ninguno.\nEsquivar: El pokemon intenta esquivar el ataque del otro pokemon. La probabilidad de esquivar es mayor cuanto mayor sea la velocidad del pokemon. Si ambos pokemones intentan esquivar, no se baja vida a ninguno.\n\n¡Comienza la pelea!\n¡Suerte!\n")
    
    while True:
        post_usu,post_compu,dict_usu,dict_compu,puntos_usu,puntos_compu=ronda(poke_usu,poke_compu,lista_eventos,dict_usu,dict_compu, puntos_usu,puntos_compu)

        cond_salida_usu=post_usu.vida==0 and len(pokemones_usu)==0
        cond_salida_compu=post_compu.vida==0 and len(pokemones_compu)==0
    
        if post_usu.vida==0 and post_compu.vida!=0:

            if 'atacar' in dict_usu:
                if "especial" in dict_usu:
                    sumar= dict_usu["atacar"] + dict_usu["especial"]
                    info_rondas.append([sumar, False])
                else:
                    info_rondas.append([dict_usu['atacar'], False])
            else:
                info_rondas.append([0, False])

        elif post_usu.vida!=0 and post_compu.vida==0:

            if 'atacar' in dict_usu:
                if "especial" in dict_usu:
                    sumar= dict_usu["atacar"] + dict_usu["especial"]
                    info_rondas.append([sumar, True])
                else:
                    info_rondas.append([dict_usu['atacar'], True])
            else:
                info_rondas.append([0, True])
    
        elif post_usu.vida==0 and post_compu.vida==0:
            if 'atacar' in dict_usu:
                if "especial" in dict_usu:
                    sumar= dict_usu["atacar"] + dict_usu["especial"]
                    info_rondas.append([sumar, True])
                else:
                    info_rondas.append([dict_usu['atacar'], True])
            else:
                info_rondas.append([0, True])
  

        if cond_salida_usu ==True and cond_salida_compu==True:
            resultado=empate(equipo_usu,equipo_compu)
            if type(resultado)==str:
                print(resultado)
                return dict_usu, dict_usu, info_rondas
            else:
                poke_usu=resultado[0]
                poke_compu=resultado[1]
                poke_usu.vida=5
                poke_compu.vida=5
                continue

        elif cond_salida_usu==True:
            print("La batalla ha finalizado. La computadora se consagra como ganadora.")
            resultado = "derrota"
            return dict_usu, dict_usu, info_rondas, resultado

        elif cond_salida_compu==True:
            print("La batalla ha finalizado. Te has consagrado como ganador. ¡Felicitaciones!")
            resultado = "victoria"

            return dict_usu, dict_usu, info_rondas, resultado
        
        if post_usu.vida!=0 and post_compu.vida!=0:
            poke_usu=post_usu
            poke_compu=post_compu
            continue
    
        elif post_usu.vida==0 and post_compu.vida!=0:
            puntos_usu=0
            puntos_compu=0
            print("Tu pokemon murió. Tu equipo está conformado por: ", pokemones_usu)
            poke_usu=input("Elija su siguiente pokemon para pelear de nuevo: ").lower().strip()
            while poke_usu not in pokemones_usu:
                print("El pokemon ingresado no se encuentra en su equipo. Inténtelo de nuevo.")
                poke_usu=input("Elija su siguiente pokemon para pelear de nuevo: ").lower().strip()
            
            pokemones_usu.remove(poke_usu) #saco de la lista el nombre del pokemon, asi no lo repite
            for pokemon in equipo_usu:
                if pokemon.nombre.lower()==poke_usu:
                    poke_usu=pokemon
                    print(f"La cpu eligió a {poke_compu.nombre}")
                    break

        elif post_usu.vida!=0 and post_compu.vida==0:
            puntos_usu=0
            puntos_compu=0
            print("Se elegirá el siguiente pokemon para pelear de nuevo...")
            poke_compu=random.choice(pokemones_compu)

            pokemones_compu.remove(poke_compu)
            for pokemon in equipo_compu:
                if pokemon.nombre.lower()==poke_compu:
                    poke_compu=pokemon
                    print(f"La cpu eligió a {poke_compu.nombre}")
                    break
    
        else:
            print("Se elegirán los siguientes pokemones a batallar")
            puntos_usu=0
            puntos_compu=0
            poke_usu=input("Tu equipo está conformado por: ", pokemones_usu, "\nIngrese su siguiente pokemon para batallar de nuevo: ").lower().strip()
            while poke_usu not in pokemones_usu:
                print("El pokemon ingresado no se encuentra en su equipo. Inténtelo de nuevo.")
                poke_usu=input("Elija su siguiente pokemon para batallar de nuevo: ").lower().strip()
            
            pokemones_usu.remove(poke_usu) #saco de la lista el nombre del pokemon, asi no lo repite
            for pokemon in equipo_usu:
                if pokemon.nombre.lower()==poke_usu:
                    poke_usu=pokemon
                    break

            poke_compu=random.choice(pokemones_compu)
            print(f"La cpu eligió a {poke_compu.nombre}")
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
    opcion=input("¡Ocurrió un empate! ¿Desea desempatar? (s/n): ").lower().strip()

    while opcion not in ['s','n']:
        print("Opción inválida")
        opcion=input("Intente de nuevo ").lower().strip

    if opcion=='n':
        return "El juego ha finalizado. Fue un empate."

    else:
        pokemons_usu=[]
        for pokemon in equipo_usu:
            pokemons_usu.append(pokemon.nombre.lower())
            
        #Se elige el primer pokemon para empezar la batalla.
        print(f"Recuerde que su lista de pokemones es: {pokemons_usu}")
        poke_usu=input("Ingrese el nombre del pokemon que quiere revivir: ").lower().strip()
        
        #valido que esté bien ingresado el nombre
        while poke_usu not in pokemons_usu:
            print("El pokemon ingresado no se encontraba en su equipo. Inténtelo de nuevo.")
            poke_usu=input("Ingrese el nombre del pokemon que quiere revivir: ").lower().strip()
        pokemons_usu.remove(poke_usu) #saco de la lista el nombre del pokemon, asi no lo repite
        
        #convierto el str primer_poke_usu a objeto
        for pokemon in equipo_usu:
            if pokemon.nombre.lower()==poke_usu:
                poke_usu=pokemon
                break
        #Hago lo mismo con los de la compu
        pokemons_compu=[]
        for pokemon in equipo_compu:
            pokemons_compu.append(pokemon.nombre.lower())
            
        poke_compu=random.choice(pokemons_compu)
        pokemons_compu.remove(poke_compu)
        
        for pokemon in equipo_compu:
            if pokemon.nombre.lower()==poke_compu:
                poke_compu=pokemon
                print(f"\nLa CPU eligio: {poke_compu}")
                break
        return [poke_usu,poke_compu]