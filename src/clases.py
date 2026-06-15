class Ambiente:
    '''
    Inicializa la clase de ambiente, la cual segun sus caracteristicas puede afectar al ataque, defensa y velocidad del pokemon o no.
    Tenes que ingresar, el nombre del ambiente (str), el tipo de ambiente (str), la fuerza que se va a modificar, la defensa que se va a modificar y la velocidad que se va a modificar (float negativo)."
    '''
    def __init__(self,nombre,tipo_ambiente, ataque, defensa, velocidad):
        self.nombre=nombre
        self.tipo_ambiente=tipo_ambiente
        self.ataque=ataque
        self.defensa=defensa
        self.velocidad=velocidad


    def modifica_atributo(self,pokemon, cpu=False):
        '''
        Modifica los atributos de los pokemones del equipo segun el ambiente en el que estén y el tipo que sea el pokemon. Si el tipo de ambiente y pokemon cooincide, se le suma los stats; sino, se le restan.
        Parámetros:
        pokemon: pokemon
        Objeto de tipo pokemon, el cual se va a utilizar para ver el tipo y modificar los atributos segun corresponda.

        Return:
        pokemon: devuelve objeto pokemon con sus atributos modificados segun el ambiente.
        '''

        if self.tipo_ambiente==pokemon.tipo:
            if cpu:
                print(f"El pokemon de la cpu, {pokemon.nombre}, se encuentra en su ambiente favorable: {self.nombre}")

            else:
                print(f"Tu {pokemon.nombre} se encuentra en su ambiente favorable: {self.nombre}")
            
        elif pokemon.adaptabilidad==1:
            if cpu:
                print(f"El pokemon de la cpu, {pokemon.nombre}, es adaptable, no se modifican sus atributos")

            else:
                print(f"Tu {pokemon.nombre} es adaptable, no se modifican sus atributos")
        elif pokemon.adaptabilidad==0.5:
            pokemon.ataque+= self.ataque/2
            pokemon.defensa+= self.defensa/2
            pokemon.velocidad+= self.velocidad/2
            if cpu:
                print(f"El pokemon de la cpu, {pokemon.nombre}, se encuentra en un ambiente desfavorable: {self.nombre}. Pero tiene adaptabilidad media asi que no se modifica tanto sus atributos.")
            else:
                print(f"Tu {pokemon.nombre} se encuentra en un ambiente desfavorable: {self.nombre}. Pero tiene adaptabilidad media asi que no se modifica tanto sus atributos.")
        else:
            pokemon.ataque+= self.ataque
            pokemon.defensa+= self.defensa
            pokemon.velocidad+= self.velocidad 
            if cpu:
                print(f"El pokemon de la cpu, {pokemon.nombre}, se encuentra en un ambiente desfavorable: {self.nombre}")
            else:
                print(f"Tu {pokemon.nombre} se encuentra en un ambiente desfavorable: {self.nombre}")
        
        return pokemon




class Evento_aleatorio:
    '''
    Inicializa la clase de evento aleatorio, la cual va a modificar la vida del pokemon si sucede.
    '''
    def __init__(self,nombre,vida):
        self.nombre=nombre
        self.vida=vida


    def evento(self,pokemon):
        '''
        Si ocurre un evento, modifica la vida del pokemon segun sea un evento afortunado (le otorga más vida) o desafortunado (le disminuye la vida).

        Parámetros:
        pokemon: pokemon
        objeto de tipo pokemon en el cual se le va a modificar su atributo de vida.

        Return: no devuelve ningún valor 
        '''
        pokemon.vida+=self.vida
        pokemon.vida=round(pokemon.vida,1)
        print(f"{pokemon.nombre} recibió un evento aleatorio: Ahora tiene {self.nombre} y su vida se modificó a {pokemon.vida}")


class Pokemon:
    '''
    Es el molde para crear cada pokemon del juego. 
    Guarda toda la informacion del pokemon y define como se comporta en la batalla.
    Cada pokemon que se crea a partir de este molde va a tener su propio nombre, tipo, vida, ataque, defensa, speed y adaptabilidad.
    Los atributos llegan ya convertidos a rangos desde crear_pokemon() que los paso por rango_atributos().
    '''
    def __init__(self, dicc):
            self.nombre = dicc['pokemon']
            self.vida = dicc['hp']
            self.ataque = dicc['ataque']                  
            self.defensa = dicc['defensa']
            self.special_attack= dicc['special_attack']
            self.adaptabilidad = dicc['adaptabilidad']
            self.velocidad = dicc['speed']
            self.tipo = dicc['tipo']

    def cambiar_atributo(self, atributo1, atributo2, num, print_cambios=True):
    
        setattr(self, atributo1, getattr(self, atributo1) + num)
        setattr(self, atributo2, getattr(self, atributo2) - num)

        if print_cambios:
            print(f"{self.nombre}: subiste '{atributo1}'")
            print(f"A cambio se reducio el atributo {atributo2}")
            print(f"ataque: {self.ataque} | defensa: {self.defensa} | velocidad: {self.velocidad} | adaptabilidad: {self.adaptabilidad}")

    def mostrar_atributos(self):
        print(f"Ataque: {self.ataque}")
        print(f"Defensa: {self.defensa}")
        print(f"Velocidad: {self.velocidad}")
        print(f"Adaptabilidad: {self.adaptabilidad}")