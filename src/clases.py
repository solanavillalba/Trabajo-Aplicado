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


    def modifica_atributo(self,pokemon):
        '''
        Modifica los atributos de los pokemones del equipo segun el ambiente en el que estén y el tipo que sea el pokemon. Si el tipo de ambiente y pokemon cooincide, se le suma los stats; sino, se le restan.
        Parámetros:
        pokemon: pokemon
        Objeto de tipo pokemon, el cual se va a utilizar para ver el tipo y modificar los atributos segun corresponda.

        Return:
        pokemon: devuelve objeto pokemon con sus atributos modificados segun el ambiente.
        '''

        if self.tipo_ambiente==pokemon.tipo:
            print(f"{pokemon.nombre} se encuentra en su ambiente favorable: {self.nombre}")
        elif pokemon.adaptabilidad==1:
            print(f"{pokemon.nombre} es adaptable, no se modifican sus atributos")
        elif pokemon.adaptabilidad==0.5:
            pokemon.ataque+= self.ataque/2
            pokemon.defensa+= self.defensa/2
            pokemon.speed+= self.velocidad/2
            print(f"{pokemon.nombre} se encuentra en un ambiente desfavorable: {self.nombre}. Pero tiene adaptabilidad media asi que sus atributos.")
        else:
            pokemon.ataque+= self.ataque
            pokemon.defensa+= self.defensa
            pokemon.speed+= self.velocidad 
            print(f"{pokemon.nombre} se encuentra en un ambiente desfavorable: {self.nombre}")
        
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
        print(f"{pokemon.nombre} recibió un evento aleatorio: {self.nombre} y su vida se modificó a {pokemon.vida}")



  





