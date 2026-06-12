class Ambiente:
    '''
    Inicializa la clase de ambiente, la cual segun sus caracteristicas puede afectar al ataque, defensa y velocidad del pokemon o no.
    '''
    def __init__(self,nombre,tipo_ambiente):
        self.nombre=nombre
        self.tipo_ambiente=tipo_ambiente


    def modifica_atributo(self,pokemon):
        '''
        Modifica los atributos de los pokemones del equipo segun el ambiente en el que estén y el tipo que sea el pokemon. Si el tipo de ambiente y pokemon cooincide, se le suma los stats; sino, se le restan.
        Parámetros:
        pokemon: pokemon
        Objeto de tipo pokemon, el cual se va a utilizar para ver el tipo y modificar los atributos segun corresponda.

        Return: no devuelve ningún valor
        '''

        if self.tipo_ambiente=='agua' and pokemon.tipo!='agua':
            pokemon.ataque= pokemon.ataque-0.20
            pokemon.defensa= pokemon.defensa - 0.05
            pokemon.speed= pokemon.speed - 0.25
        else:
            pokemon.ataque= pokemon.ataque+0.20
            pokemon.defensa= pokemon.defensa + 0.05
            pokemon.speed= pokemon.speed + 0.25

        if self.tipo_ambiente=='tierra' and pokemon.tipo!='tierra':
            pokemon.ataque= pokemon.ataque-0.20
            pokemon.defensa= pokemon.defensa - 0.15
            pokemon.speed= pokemon.speed - 0.15
        else:
            pokemon.ataque= pokemon.ataque + 0.20
            pokemon.defensa= pokemon.defensa + 0.15
            pokemon.speed= pokemon.speed + 0.15
        
        if self.tipo_ambiente=='rayos' and pokemon.tipo!='electrico':
            pokemon.ataque= pokemon.ataque-0.15
            pokemon.defensa= pokemon.defensa - 0.2
            pokemon.speed= pokemon.speed - 0.05
        else:
            pokemon.ataque= pokemon.ataque+0.15
            pokemon.defensa= pokemon.defensa + 0.2
            pokemon.speed= pokemon.speed + 0.05
        
        if self.tipo_ambiente=='fuego' and pokemon.tipo!='fuego':
            pokemon.ataque= pokemon.ataque-0.5
            pokemon.defensa= pokemon.defensa - 0.15
            pokemon.speed= pokemon.speed - 0.1
        else:
            pokemon.ataque= pokemon.ataque + 0.5
            pokemon.defensa= pokemon.defensa + 0.15
            pokemon.speed= pokemon.speed + 0.1



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



  





