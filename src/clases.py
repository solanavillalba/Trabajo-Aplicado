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
    def __init__(self, nombre, tipo, vida, ataque, defensa, speed, adaptabilidad, ataque_crudo, defensa_crudo, speed_crudo):

        # informacion basica del pokemon, viene de la API via obtener_datos_api() y crear_pokemon()
        self.nombre = nombre 
        self.tipo = tipo           # 'agua', 'tierra', 'fuego' o 'electricidad' aca Ambiente.modifica_atributo() lo compara con el tipo del ambiente. 
                                    #si coinciden el pokemon no sufre penalizacion, que sino sus atributos bajan
              
        self.vida = vida     # este atributo se usan directamente en Ronda() para calcular como va yendo el combate, siempre vale 5 (lo fija rango_atributos())                
                                               # en Ronda() se resta cada vez que el pokemon recibe un golpe ( ej: si recibe ataque=2, vida = 5-2 = 3) si llega a 0 el pokemon muere y sale del equipo
      
        self.ataque = ataque                   # puede ser 1 (Bajo), 1.5 (Medio) o 2 (Alto)
                                               # en Ronda() es el daño que le hace al rival
                                               # ej: ataque=2  pokemon2.vida -= 2

        self.defensa = defensa                 # puede ser 0.75 (Bajo), 0.5 (Medio) o 0.25 (Alto)
                                               # en Ronda() multiplica el daño recibido cuando el pokemon defiende
                                               # ej: defensa=0.25,  recibe muy poco daño (pokemon1.vida -= ataque * 0.25)
                                               # ej: defensa=0.75, recibe casi todo el daño (pokemon1.vida -= ataque * 0.75)

        self.speed = speed                     # puede ser 0.25 (Bajo), 0.5 (Medio) o 0.75 (Alto)
                                               # en Ronda() es la probabilidad de esquivar un ataque
                                               # ej: speed=0.75 → 75% de chances de esquivar, speed=0.25 → 25% de chances

        self.adaptabilidad = adaptabilidad     # puede ser 0 (Bajo), 0.5 (Medio) o 1 (Alto)
                                               # Ambiente.modifica_atributo() lo usa para decidir cuanto penalizar al pokemon
                                               # adaptabilidad=1  no se penaliza nada en ambiente desfavorable
                                               # adaptabilidad=0.5  se penaliza a la mitad
                                               # adaptabilidad=0  se penaliza completo

        # guardamos los valores crudos de la API porque cambiar_atributo() los necesita, sino  que aca el problema es que una vez que rango_atributos() convirtio ataque=95 a ataque=1.5. ya no podemos recuperar el 95 si no lo guardamos y rango_atributos() necesita valores en escala 0-150, no 1/1.5/2
        self.ataque_crudo = ataque_crudo       
        self.defensa_crudo = defensa_crudo     
        self.speed_crudo = speed_crudo        

    def cambiar_atributo(self, atributo, nuevo_valor):
        '''
        Se llama una sola vez al inicio del juego, antes de que empiece la batalla.
        El jugador elige un atributo y le asigna un numero del 1 al 10.
        Ese numero se multiplica por 15 para pasarlo a escala 0-150 que entiende rango_atributos().
        rango_atributos() lo convierte al valor real que despues usa Ronda() en el combate.
        Parametros:
        atributo: str
        Nombre del atributo a modificar. Puede ser 'ataque', 'defensa' o 'speed'.
        nuevo_valor: int
        Numero del 1 al 10 elegido por el jugador.

        Return:
        No retorna nada.
        '''
        atributos_validos = ["ataque", "defensa", "speed"]
        if atributo not in atributos_validos:
            print(f"'{atributo}' no es modificable. Elegí entre: {atributos_validos}")
            return

        # 1) multiplicamos el valor del jugador (1-10) por 15 para pasarlo a escala 0-150,se necesita pq rango_atributos() fue diseñada para trabajar con valores de la API (0-150) (ej: jugador ingresa 3 () 3*15=45) aca rango_atributos() da  Bajo  (< 60)
        valor_convertido = nuevo_valor * 15

        if atributo == "ataque":
            # 2): llamamos a rango_atributos() con el valor convertido en ataque
            # los otros atributos van con sus valores crudos originales para que no cambien
            ataque_conv, defensa_conv, speed_conv, adaptabilidad_conv, vida_conv = rango_atributos(
                valor_convertido,    # este es el que el jugador quiere cambiar
                self.defensa_crudo,  # este no cambia, usamos el crudo original de la API
                self.speed_crudo,    # este no cambia, usamos el crudo original de la API
                self.adaptabilidad,
                self.vida
            )
            # 3): actualizamos el atributo con el valor que devolvio rango_atributos()
            # a partir de aca Ronda() va a usar este nuevo valor para calcular el daño
            self.ataque = ataque_conv
            print(f"{self.nombre}: ataque cambió a {self.ataque} y en Ronda() le va a sacar {self.ataque} puntos de vida al rival")

        elif atributo == "defensa":
            ataque_conv, defensa_conv, speed_conv, adaptabilidad_conv, vida_conv = rango_atributos(
                self.ataque_crudo,   # este no cambia, usamos el crudo original de la API
                valor_convertido,    # este es el que el jugador quiere cambiar
                self.speed_crudo,    # este no cambia, usamos el crudo original de la API
                self.adaptabilidad,
                self.vida
            )
            self.defensa = defensa_conv
            print(f"{self.nombre}: defensa cambió a {self.defensa} y en Ronda() el daño recibido se multiplica por {self.defensa}")

        elif atributo == "speed":
            ataque_conv, defensa_conv, speed_conv, adaptabilidad_conv, vida_conv = rango_atributos(
                self.ataque_crudo,   # este no cambia, usamos el crudo original de la API
                self.defensa_crudo,  # este no cambia, usamos el crudo original de la API
                valor_convertido,    # este es el que el jugador quiere cambiar
                self.adaptabilidad,
                self.vida
            )
            self.speed = speed_conv
            print(f"{self.nombre}: speed cambió a {self.speed} y en Ronda() tiene {self.speed*100}% de chances de esquivar")

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