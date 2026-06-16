import random
import src.clases as c
import src.pokemones as p
import src.analizar_datos as a
import src.funciones as f


print("¡Bienvenido al juego de Pokemon!")
#----------------------------------------------------
# CREACION LISTA POKEMONES

list_poke = { #ESTA SERIA EL DICCIONARIO CREADO POR LA API
    "Novatos": ["dragonite","tyranitar","metagross","arcanine"],
    "Medios": ["vaporeon","jolteon","pikachu","eevee"],
    "Altos": ["psyduck","charmander","charizard","rattata"] }

pokemones= p.convertir_diccio(list_poke)
#----------------------------------------------------
#PARES ANALOGOS DE HABILIDADES
pares = {
    "ataque": "velocidad",
    "velocidad": "ataque",
    "defensa": "adaptabilidad",
    "adaptabilidad": "defensa"}

#----------------------------------------------------
#CREACION LISTA DE AMBIENTES
lista_ambientes = []
playa = c.Ambiente("playa", "water", float(-0.20), float(-0.05), float(-0.25))
lista_ambientes.append(playa)
bosque = c.Ambiente("bosque", "ground", float(-0.2), float(-0.15), float(-0.1))
lista_ambientes.append(bosque)
tormenta = c.Ambiente("tormenta de rayos", "electric", float(-0.15), float(-0.2), float(-0.3))
lista_ambientes.append(tormenta)
volcan = c.Ambiente("volcán", "fire", float(-0.5), float(-0.15), float(-0.1))
lista_ambientes.append(volcan)

#----------------------------------------------------
#CREACION LISTA EVENTOS ALEATORIOS
lista_eventos_aleatorios = []
aumentar_1vida = c.Evento_aleatorio("un kit médico", 1)
lista_eventos_aleatorios.append(aumentar_1vida)
aumentar_05vida = c.Evento_aleatorio("un ibuprofeno", 0.5)
lista_eventos_aleatorios.append(aumentar_05vida)
bajar_05vida = c.Evento_aleatorio("una gripe", -0.5)
lista_eventos_aleatorios.append(bajar_05vida)
bajar_1vida = c.Evento_aleatorio("asma", -1)
lista_eventos_aleatorios.append(bajar_1vida)

#----------------------------------------------------
#CREACION LISTA DE USUARIO Y CPU DE POKEMONES
print("Es hora de conformar tu equipo con tres pokemones personalizados")
pok_usuario = []
pok_cpu = []

#----------------------------------------------------
#ELECCION POKEMON USUARIO
for tipo, lista_pokemones in pokemones.items():
    print("\nElegí un pokemon de la categoría:", tipo, "\n")
    for pokemon in lista_pokemones:
        pokemon.mostrar_atributos(True) #sale de la clase pokemon 
    poke = input("\nSeleccione pokemon: ").lower().strip()
    
    while poke not in list_poke[tipo]:
            poke = input("Pokemon inválido. \nSeleccione Pokemon de la lista: ").lower().strip()
    print(f"¡Se ha seleccionado a {poke} de forma correcta!")

    pokemon_elegido = None
    for pokemon in lista_pokemones:
        if pokemon.nombre == poke:
            pokemon_elegido = pokemon
            break
            
# USUARIO SELECCIONAR ATRIBUTO A CAMBIAR
    lista_atributos = ["ataque","velocidad","defensa","adaptabilidad" ]
    
    print("\nIngrese el atributo a mejorar, recuerde que aumentar un atributo disminuye otro.")  
    atributo = input("Elegí entre Ataque, Adaptabilidad, Defensa o Velocidad: ").lower().strip()

    while atributo not in lista_atributos:
        atributo = input("Atributo inválido. \nSeleccione un atributo de la lista: ").lower().strip()
    
    atributo2 = pares[atributo]
    pokemon_elegido.cambiar_atributo(atributo, atributo2, 0.15)
    pok_usuario.append(pokemon_elegido) #VERIFICAR STRING UNA VEZ Q SE CREE BIEN EL OBJETO

list_cpu = { #ESTA SERIA EL DICCIONARIO CREADO POR LA API
    "Novatos": ["dragonite","tyranitar","metagross","arcanine"],
    "Medios": ["vaporeon","jolteon","pikachu","eevee"],
    "Altos": ["psyduck","charmander","charizard","rattata"] }

pokemones_cpu=p.convertir_diccio(list_cpu)

# ELECCION CPU
for categoria, lista_pokemones in pokemones_cpu.items():
    num_cpu = random.randint(0, (len(lista_pokemones) -1))
    pokemon_elegido_cpu = lista_pokemones[num_cpu]

# CPU SELECCIONAR ATRIBUTO A CAMBIAR   
    num_att = random.randint(0, (len(lista_atributos)-1))
    #funcion_cambio_atributo(poke_cpu, num_att)
    atributo_cpu = lista_atributos[num_att]
    atributo_cpu2 = pares[atributo_cpu]

    pokemon_elegido_cpu.cambiar_atributo(atributo_cpu, atributo_cpu2, 0.15, False)
    pok_cpu.append(pokemon_elegido_cpu)
    
print('\nLa cpu eligió a:')
for pokemon in pok_cpu:
    print(pokemon.nombre)

print("\nInicia la batalla")
print("Seleccionando arena de juego...\n")

dict_usuario, dict_cpu, info_partida = f.partida(pok_usuario, pok_cpu, lista_eventos_aleatorios, lista_ambientes)
promedio, mejor_ronda=a.promedio(info_partida)

print("\nAnalizando rendimientos de la batalla...")

print(f"En promedio matar al pokemon oponente te costo {promedio} golpes. Y tu mejor pelea es de {mejor_ronda[0]} golpes en el pokemon número {mejor_ronda[1]}")