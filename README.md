Simulador de combate y adaptación pokemon

Integrantes: Portillo Victoria, Ramírez Osorio María José, Ruiz Bruno y Villalba Solana.
Objetivo
El objetivo de este trabajo es desarrollar un juego interactivo que permita simular combates entre Pokémones con sus atributos modificados en distintos ambientes.

Descripción general del funcionamiento del sistema
El usuario elegirá 3 pokemones de un total de 12, de los cuales el tipo varía entre agua, tierra, fuego y eléctrico. Cada pokémon del equipo será de un nivel distinto, variando entre bajo, medio, alto (clasificados según sus valores de ataque, defensa, velocidad, ataque especial y defensa especial, a este último lo llamamos adaptabilidad). Al elegir cada pokémon del equipo, el usuario podrá mejorar el ataque, la defensa, la velocidad o la adaptabilidad del pokémon. Sin embargo, dependiendo de qué atributo elija mejorar, se le empeorará otro. La computadora hará lo mismo que el usuario de forma aleatoria. Una vez que tanto la computadora como el usuario tienen sus equipos con sus atributos modificados, se elegirá un ambiente aleatorio en dónde batallar. Este ambiente puede perjudicar al equipo si el tipo de ambiente no coincide con el tipo del pokémon. Una vez elegido el ambiente, el usuario deberá elegir el pokémon con el que quiera empezar la batalla (la computadora hará lo mismo de forma aleatoria). Puede suceder que por ronda, ocurra un evento aleatorio, el cual puede aumentar o disminuir la vida del pokémon en uso. De esta manera, el usuario (y la computadora) pueden elegir entre 3 acciones: atacar, defender o esquivar. La acción “atacar” provoca daño al contrincante, sin embargo, el daño generado puede variar según el contrincante decida “defender” o “esquivar”. La acción “defender” reduce el daño recibido por el ataque del contrincante; si el contrincante no decide atacar, entonces ninguno de los pokemones en batalla recibe daño por el otro. La acción “esquivar” consiste en dos posibilidades: por un lado, si el pokémon logra esquivar, entonces el ataque del contrincante no le producirá ningún daño (si el contrincante decide “atacar”); por el otro, si no logra esquivar y el contrincante decide atacar, entonces le producirá todo el daño del ataque. Esta elección de acciones seguirá hasta que todos los pokemones de uno de los equipos se muera. Es entonces que se consagra como ganador aquel equipo que tenga uno o más pokémons con vida (teniendo al otro equipo sin vida). Puede llegar a suceder que ambos equipos se mueran al mismo tiempo, provocando un empate. Es en ese caso que el usuario puede elegir entre terminar la partida en ese momento o revivir uno de sus pokémons y batallar de nuevo con la computadora. En el último caso, aquel pokémon que se muera primero será el perdedor. Además, al finalizar la partida, el usuario puede elegir ver un gráfico de su promedio de golpes efectivos o de la computadora.

Principales funcionalidades y adjudicación de la parte del programa que realizó cada integrante
Portillo, Victoria: función partida(), función empate(), función rango_atributos().
Ramírez Osorio, María José: archivo data api.py, parte de clases.py (específicamente clase Pokemon),  analizar_datos.py (específicamente la parte de generar la función de gráfico torta mostrando las acciones usadas en el combate.
Ruiz, Bruno: archivo main.py, archivo app.py
Villalba, Solana: función ronda(), archivo pokemones.py (excepto la función rango_atributos), función promedio(), clase Evento_aleatorio y clase Ambiente.

Descripción de la fuente de datos
Como fuente de datos, utilizamos la API de Pokémon, denominada PokéAPI. La PokéAPI contiene información de todos los pokemons sobre sus distintas características. Nosotros reducimos nuestra fuente a las siguientes: “name” (nombre), “type” (tipo), “attack” (ataque), “defense” (defensa), “special_attack” (ataque especial), “special_defense” (adaptabilidad) y “speed” (velocidad).

Librerías utilizadas

Matplotlib: utilizada para la generación de gráficos de torta. Estos gráficos permiten visualizar la distribución porcentual de las acciones realizadas durante las partidas (ataques, defensas, esquives y ataques especiales), facilitando el análisis del desempeño del usuario y de la computadora.
Random: utilizada para generar valores aleatorios necesarios para la lógica del juego, incluyendo la selección de ambientes, la elección de Pokémon, la ocurrencia de eventos aleatorios durante las batallas, y todas las elecciones/acciones de la computadora.
Requests: permite obtener los datos de los Pokémon desde la PokéAPI. La información recibida en formato JSON se transforma en diccionarios que luego son utilizados para crear los Pokémon del juego. 
Pygame: Pygame es una biblioteca de Python diseñada para el desarrollo de videojuegos y aplicaciones multimedia. Proporciona herramientas para gestionar gráficos, sonido, animaciones, eventos de teclado y mouse, y control del tiempo dentro del juego.
io: el módulo io proporciona herramientas para trabajar con flujos de entrada y salida de datos (input/output). Permite leer y escribir información en archivos o manejar datos en memoria utilizando objetos similares a archivos.
os: el módulo os permite interactuar con el sistema operativo. Proporciona funciones para trabajar con directorios, archivos, rutas y variables del entorno.
sys: el módulo sys ofrece acceso a variables y funciones relacionadas con el intérprete de Python y la ejecución del programa.

Instrucciones para ejecutar el programa

Requisitos previos:

En primer lugar, es necesario contar con conexión a internet para poder utilizar la API.
Antes de ejecutar el programa, es necesario tener instalado Python 3.

Para verificar la instalación de Python:
Windows:
Abra CMD o PowerShell y ejecute:
python --version
macOS:
Abra Terminal y ejecute:
python3 --version
Si Python está instalado correctamente, se mostrará la versión correspondiente.
Instalación de las bibliotecas necesarias
El programa utiliza las siguientes bibliotecas externas:
pygame
matplotlib
requests
Instalación en Windows:
Abra CMD o PowerShell y ejecute:
pip install pygame/ matplotlib/ requests
Si el comando anterior no funciona, pruebe:
python -m pip install pygame/ matplotlib/ requests
Instalación en macOS:
Abra la aplicación Terminal y ejecute:
pip3 install pygame/ matplotlib/ requests
Si el comando anterior no funciona, utilice:
python3 -m pip install pygame/ matplotlib/ requests

Verificación de la instalación
Para comprobar que todas las bibliotecas se instalaron correctamente, abra Python e ingrese:
import pygame/matplotlib/requests
Si no aparece ningún mensaje de error, la instalación fue exitosa.

Ejecución del programa
Una vez instaladas las dependencias, ubíquese en la carpeta del proyecto y ejecute:
app.py (para ejecutar el juego con interfaz grafica)
main.py (para ejecutar el juego desde la consola)

Estructura del repositorio
El repositorio cuenta con las siguientes carpetas:
data: contiene la entrada de datos del programa (llamando a la PokéAPI).
docs: contiene la documentación y diseño del programa.
imágenes: contiene imágenes de fondo como representación de los ambientes del programa.
src: contiene toda la lógica detrás del programa. Esto incluye funciones, clases y la creación de gráficos.
main.py: el código principal del programa, aquello que une toda la lógica del programa y crea la experiencia del usuario.
app.py: genera el dashboard del programa.
requirements.txt: contiene las librerías necesarias para que corra el programa.

Explicación breve de las clases implementadas
Clase Pokemon: inicializa una clase de pokemon. Como atributos va a tener: vida, tipo, nivel de ataque, defensa, adaptabilidad, ataque especial y velocidad del pokémon. Como métodos, se van a poder modificar dos atributos según corresponda; y también se van a poder mostrar los atributos actuales del pokémon.
Clase Ambiente: inicializa una clase de ambiente. Como atributos tiene: nombre, tipo de ambiente, ataque, defensa y velocidad (los últimos tres indica cuánto de cada atributo le saca a los pokemones si este no es su ambiente ideal). Como métodos tiene modificar atributos, donde revisa la adaptabilidad del pokemon y, según cuánta tenga, le modifica más o menos los atributos (si es que el pokémon no está en su ambiente ideal).
Clase Evento_aleatorio: inicializa una clase de evento aleatorio. Como atributos tiene: nombre (del evento) y vida (a sumar o a quitar del pokemon). Como método tiene eventos donde se modifica la vida del pokémon según sea un evento afortunado (le otorga más vida) o desafortunado (le disminuye la vida).

Explicación breve de las funciones principales
ronda(): Simula una ronda de batalla entre dos pokemones. Le pregunta al usuario qué acción quiere realizar (ataque, defensa o esquive). Y teniendo en cuenta sus atributos y eventos aleatorios calcula el resultado de la pelea.
partida(): Mantiene a los pokemons batallando (llama a la función ronda()) hasta que uno muera. Cuando eso sucede, el usuario o la computadora pueden elegir alguno de los otros pokemones previamente seleccionados para seguir batallando, aquel que mantuvo su pokemon con vida lo va a seguir utilizando hasta que muera. Esto continuará hasta que uno de los dos equipos se quede sin pokemones con vida.
empate(): Si ocurre un empate (todos los pokemones de ambos equipos se encuentran sin vida), esta función se encarga de darle dos opciones al usuario. Si desea dejarlo como un empate, lo deja como un empate. Sino, da la opción de revivir a ambos equipos uno de los pokemones y volver a batallar.
convertir_diccio(): Recibe un diccionario con los values que son una lista de nombres (strings) de los pokemones. Después, devuelve otro diccionario con los Pokemones ya creados como objetos.
crear_pokemon(): Recibe el nombre de un pokemon, hace la consulta a la API, convierte los datos a rangos y devuelve un objeto Pokemon con los atributos correspondientes.
rango_atributos(): Convierte los valores de los datos del pokémon sacados de la API a rangos entre 0 y 2. Esto es con el objetivo de diferenciar pokemones de niveles bajos, medios y altos.
str_a_pokemones(): Recibe una lista con los nombres de los pokemones y los convierte en objetos.
Resultados y gráficos
Al final del programa, se le indicará al usuario si ganó o perdió la partida según las condiciones mencionadas anteriormente. Además, en caso de que el usuario haya derrotado como mínimo a uno de los pokemons del equipo contrario, entonces se le mostrará el promedio de la cantidad de golpes que le costó para matar a/los pokemon/s del contrincante y, también, cuál fue su mejor ronda según el pokemon del contrincante que le costó matar con la menor cantidad de golpes.
Además, genera dos gráficos de torta con las acciones realizadas en la partida y expresadas de una forma porcentual, permitiendo analizar las decisiones tomadas. 
Ejemplo del gráfico: 

Diagramas de diseño
https://github.com/solanavillalba/Trabajo-Aplicado/tree/main/docs/diagramas-de-flujo
Declaración de uso de IA
Si bien el uso de la IA no fue descartado, es necesario aclarar que su uso fue puramente de apoyo (cuando no sabíamos hacer alguna acción en específico, ej. “Hola chat, tengo este código … y quiero agregar un golpe especial pero no estoy segura de como hacerlo, tiene que tener una racha de 3 golpes efectivos. ayudame explicandome de a líneas”). El código en sí mismo y la lógica detrás fueron producciones nuestras.
La IA fue utilizada para dos tipos de acciones principales:
Uso de API
Se le solicito a la IA que genere un código para poder llamar a la API de Poké API y poder solicitar los datos que se necesitaban para el trabajo. Estos son: nombre de pokemon, ataque, defensa, speed, special attack, special defense, type, hp y sprite (imagen). A continuación se adjunta un ejemplo de prompt: 
“hola chat, necesito que me ayudes a comprender y generar una función para mi juego de pokemon. La idea es que use la librería requests para llamar a la pokeapi y que reciba como parámetro el nombre de un pokemon. Con esa informacion quiero obtener los datos necesarios para mi juego y devolverlos en un diccionario, en este caso hp, attack, defense, special attack, special defense, speed y el tipo del pokemon. Tambien me gustaria que me expliques mas o menos como se accede a esos datos dentro de la respuesta de la api para poder entenderlo mejor. Si el pokemon ingresado no existe o hay algun problema con la consulta, la función deberia tirar un ValueError. No necesito algo muy complicado, pero si que este bien explicado para poder adaptarlo despues al resto del proyecto”
q: “qué significa eso de status_code != 200? 
A: “El status_code es un código que devuelve el servidor para indicar si la solicitud fue exitosa o no. El código 200 significa que todo salió bien y que la información fue encontrada correctamente.
Por ejemplo:
200: consulta exitosa.
404: recurso no encontrado (por ejemplo, el Pokémon no existe).
500: error interno del servidor.
Por eso en el código aparece:
if respuesta.status_code != 200:
   	 raise ValueError(f"Error con {pokemon}")
La idea es verificar que la API respondió correctamente antes de intentar acceder a los datos.”
Creación de dashboard en archivo app.py con ejemplos de prompts.
Para desarrollar la interfaz gráfica del juego, se le pidió a la inteligencia artificial Claude que la produjera utilizando la librería Gamepy. Para que haga esto, primero, se le explicó a la IA el contexto y el objetivo del juego y bajo qué lógica desarrollamos el programa. Después, se les paso todos los archivos del programa (main, funciones, clases, pokemones, analizar_datos, imagenes) y que, utilizando las funciones ya creadas, y observando la lógica que observe en el programa, desarrolle un dashboard visual para poder jugar. A continuación se adjuntan ejemplos de prompts:
“Hola claude como estas, mira estoy haciendo un programa de batalla de pokemones. te dejo los archivos del programa. ahora tengo que hacer la interfaz grafica, para eso estoy usando gamepy. YO NO SE NADA DE GAMEPY, de python si. necesito que me ayudes a armar la interfaz grafica, te dejo los archivos. en el de app.py esta lo de la interfaz que ya pude armar un poquito”
“Q: ¿Cómo querés arrancar con la interfaz gráfica?
A: Ir pantalla por pantalla (primero selección de pokemones, después la batalla)
Q: ¿Tenés sprites/imágenes de los pokemones o usamos los de la PokeAPI?
A: Usemos los sprites de la PokeAPI (se descargan automático)”
Posteriormente, Claude nos preguntó como queríamos que lo hiciera y le dijimos que queríamos dividir el programa en varias pantallas, la de selección de equipo de pokemon, selección de pokemon a utilizar en la ronda, pantalla de batalla y pantalla de finalización.
Una vez que creó el programa, surgieron unos cuantos problemas, como por ejemplo el historial de acciones no se actualizaba o que la ronda quedaba congelada, por lo que también se le solicitó a Claude que solucionara eso.
“Claude, ya estuve laburando en la app.py, ya hice lo de la selección de personajes y lo de batalla. Ahi te paso el archivo. Ahora, necesito que me ayudes con dos cosas. 
Sabes que, primero, en el LOG de la batalla el texto de las acciones desaparece al instante, sale un instante y se va. Necesito que soluciones eso para que quede y despues vaya subiendo, y desapareciendo del cuadro, a medida que nuevo texto aparece.
Ademas, a la hora de elegir los personajes necesito hacer un cambio en la barra de las stats. Necesito que adaptes la barrita teniendo en cuenta que los maximos por stat son: 1. Ataque: 2,15 2. Defensa: 0,90 3. Adaptabilidad: 1 4. Velocidad: 0,90”

Eventualmente, la base del programa quedó totalmente funcional y de acuerdo a lo que se le solicitó. Al final, también se le pidió a la IA que arreglara algunos detalles visuales y cuestiones estéticas. 
“perfecto claude, posta quedo muy bien, ahora te puedo pedir otro favor. Viste que hay 4 tipos de ambientes, bosque, playa, volcan y tormenta de rayos. Tengo una imagen para cada ambiente, en las partidas podes generar un codigo para setear las imagenes de los ambientes? mira te las paso por las dudas, nose bien si podes ponerlas directamente o tengo que copiar la url de mi computadora, pero por lo menos podes ir viendo las dimensiones. Por las dudas, quiero que coloques la imagen donde van los pokemones, no a los costados sino en ese mismo panel, haciendo que los pokemones queden por encima de la imagen.”

Notas o explicaciones adicionales para correr correctamente el programa
En caso de tener problemas con la instalación de las librerías o de python en sí, adjunto el link de las páginas oficiales de cada librería, donde se puede consultar o ver mas información sobre su debida instalación.

requests: https://requests.readthedocs.io/en/latest/
pygame: https://www.pygame.org/news
matplotlib: https://matplotlib.org/ 
python: https://www.python.org/ 
