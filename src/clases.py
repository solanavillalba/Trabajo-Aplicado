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
        cpu: bool. Para ver si se imprime tu pokemon o el pokemon de la cpu. 

        Return:
        pokemon: devuelve objeto pokemon con sus atributos modificados segun el ambiente.
        '''

        if self.tipo_ambiente == pokemon.tipo:
            pass 
        elif pokemon.adaptabilidad <= 1:
            pass
        elif pokemon.adaptabilidad <= 0.5:
            pokemon.ataque= round(pokemon.ataque+(self.ataque/2),2)
            pokemon.defensa= round(pokemon.defensa+(self.defensa/2),2)
            pokemon.velocidad= round(pokemon.velocidad+(self.velocidad/2), 2)
        
        else:
            pokemon.ataque=  round(pokemon.ataque+self.ataque,2)
            pokemon.defensa= round(pokemon.defensa+self.defensa,2)
            pokemon.velocidad= round(pokemon.velocidad+self.velocidad,2)
        
        if pokemon.ataque<=0:
            pokemon.ataque=0.0
        if pokemon.defensa<=0:
            pokemon.defensa=0.0
        if pokemon.velocidad<=0:
            pokemon.velocidad=0.0

        if self.tipo_ambiente == pokemon.tipo:
            if cpu:
                print(f"\nEl pokemon de la cpu, {pokemon.nombre}, se encuentra en su ambiente favorable. Juega con ventaja.")
            else:
                print(f"\nTu pokemon {pokemon.nombre} está en su ambiente favorable.")
        elif pokemon.adaptabilidad == 1:
            if cpu:
                print(f"\nEl pokemon de la cpu, {pokemon.nombre}, se encuentra en un ambiente desfavorable. Pero se medio adaptó. Juega en condiciones normales.")
            else:    
                print(f"\nTu pokemon {pokemon.nombre} se adaptó perfectamente.")
        elif pokemon.adaptabilidad == 0.5:
            if cpu:
                print(f"\nEl pokemon de la cpu, {pokemon.nombre}, se encuentra en un ambiente desfavorable. Pero se medio adaptó. Juega en condiciones normales.")
            else:
                print(f"\nTu {pokemon.nombre} se encuentra en un ambiente desfavorable. Pero se medio adaptó. Juega en condiciones normales.")
        else:
            if cpu:
                print(f"\nEl pokemon {pokemon.nombre} de la cpu se encuentra en un ambiente desfavorable. Juega en desventaja.")
            else:
                print(f"\nTu pokemon {pokemon.nombre} tuvo cambios en sus atributos.")
            
        print(f"Sus atributos actualizados son:")

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
        if pokemon.vida<=0.0:
            pokemon.vida==0
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
        """
        Modifica dos valores de ciertos atributos. 
        Parametros:
        atributo1 (str): Atributo a mejorar
        atributo2 (str): Atributo afectado
        num (float): Cuanto se mejora y empeora cada atributo
        print_cambios (bool): Si se imprimen en consola los cambios

        Retorna: No retorna nada
        """
        
        
        setattr(self, atributo2, getattr(self, atributo2) - num)
        setattr(self, atributo1, getattr(self, atributo1) + num)
        
        if self.ataque<=0:
            self.ataque=0.0
        if self.defensa<=0:
            self.defensa=0.0
        if self.velocidad<=0:
            self.velocidad=0.0
        if self.adaptabilidad<=0:
            self.adaptabilidad=0.0

        if print_cambios:
            if getattr(self, atributo2) == 0:
                print(f"Subiste {atributo1} pero no se realizan cambios en {atributo2} porque ya es 0.")
            else:
                setattr(self, atributo2, getattr(self, atributo2) - num)
                print(f"Subiste {atributo1} y se redujo el atributo {atributo2} \n")

            print(f"Tu {self.nombre} tiene: \nAtaque: {self.ataque} | Defensa: {self.defensa} | Velocidad: {self.velocidad} | Adaptabilidad: {self.adaptabilidad}")

    def mostrar_atributos(self, nombre=False):
        '''
        Muesta los atributos del pokemon.
        Parámetros:
        nombre: bool
        Si la variable es True, imprime la información de los atributos con el nombre del pokemon. Si es False, imprime solo la info de los atributos (sin el nombre del pokemon).
        Retorna: no retorna nada
        '''
        if nombre:
            print(f"{self.nombre}: {self.tipo} | Ataque: {self.ataque} | Defensa: {self.defensa} | Velocidad: {self.velocidad} | Adaptabilidad: {self.adaptabilidad}")

        else:    
            print(f"Ataque: {self.ataque} | Defensa: {self.defensa} | Velocidad: {self.velocidad} | Adaptabilidad: {self.adaptabilidad}")

        