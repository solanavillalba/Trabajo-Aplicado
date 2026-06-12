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
            self.speed = dicc['speed']
            self.tipo = dicc['tipo']

def cambiar_atributo(self, atributo, numero_boost):
    
   if atributo == "ataque":
        self.ataque += numero_boost
        self.speed  -= numero_boost
    
    elif atributo == "defensa":
        self.defensa       += numero_boost
        self.adaptabilidad -= numero_boost
    
    elif atributo == "special_defense":
        self.adaptabilidad += numero_boost
        self.defensa       -= numero_boost

    elif atributo == "speed":
        self.speed += numero_boost
        self.ataque -= numero_boost

    else:
        print(f"'{atributo}' no es válido.")
        return

    print(f"{self.nombre}: subiste '{atributo}'")
    print(f"ataque: {self.ataque} | defensa: {self.defensa} | speed: {self.speed} | adaptabilidad: {self.adaptabilidad}")


    def mostrar_atributos(self):
        '''
        Muestra por pantalla todos los atributos del pokemon con su nivel descriptivo (Bajo, Medio o Alto).
        Util para que el jugador vea el estado de su pokemon antes y despues de modificarlo.
        Parametros:
        No recibe parametros.

        Return:
        No retorna nada.
        '''
        # diccionarios para traducir el valor numerico a palabras que entiende el jugador
        # ej: ataque=1.5 = "Medio", defensa=0.25 = "Alto", speed=0.75 = "Alto"
        niveles_adaptabilidad = {0: "Bajo", 0.5: "Medio", 1:    "Alto"}
        niveles_ataque        = {1: "Bajo", 1.5: "Medio", 2:    "Alto"}
        niveles_defensa       = {0.75: "Bajo", 0.5: "Medio", 0.25: "Alto"}
        niveles_speed         = {0.25: "Bajo", 0.5: "Medio", 0.75: "Alto"}

        print(f"{self.nombre} | Tipo: {self.tipo}")
        print(f"Vida:      {self.vida}   si llega a 0 el pokemon muere y sale del equipo")
        print(f"Ataque:    {self.ataque} ({niveles_ataque.get(self.ataque, '?')})   le saca {self.ataque} puntos de vida al rival en Ronda()")
        print(f"Defensa:   {self.defensa} ({niveles_defensa.get(self.defensa, '?')})   el daño recibido se multiplica por {self.defensa} en Ronda()")
        print(f"Velocidad: {self.speed} ({niveles_speed.get(self.speed, '?')})   {self.speed*100}% de chances de esquivar un ataque en Ronda()")
        print(f"Adaptab.:  {self.adaptabilidad} ({niveles_adaptabilidad.get(self.adaptabilidad, '?')})   cuanto lo afecta un ambiente desfavorable en Ambiente.modifica_atributo()")