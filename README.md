# **ST0263 Tópicos Especiales en Telemática**

# **Estudiantes**: Daniel Melguizo Roldan, dmelguizor@eafit.edu.co Holmer Ortega Gomez, hortegag@eafit.edu.co

# **Profesor**: Juan Carlos Montoya Mendoza, jcmontoy@eafit.edu.co

*******

**Tabla de Contenido**
1. [Introducción](#introduccion)
2. [Requisitos completados y no completados](#requisitos)
3. [Diseño y arquitectura](#arquitectura)
4. [Ambiente de desarrollo](#ambiente)
5. [Ejecución](#ejecucion)
6. [Referencias](#referencias)

*******

<div id="introduccion" />
  
### **Proyecto 1**
El proyecto consiste en diseñar un sistema de archivos distribuido, que permita compartir y descargar de manera concurrente cualquier tipo de archivo que se encuentre almacenado en un conjunto de nodos gestionados por un servidor principal. El servidor principal lo conoceremos con NameNode, y el conjunto de nodos sobre el cual se almacenaran los distintos archivos subidos en el sistema se conoceran como DataNodes. Ademas, la red de DataNodes se comportara a su vez como una red P2P.

*******

<div id="requisitos" />

### ***Requisitos completados***
* El sistema debe permitir al usuario subir un archivo.
* El sistema debe permitir al usuario descargar un archivo.
* El almacenamiento de archivos en el sistema se debe realizar por bloques.
* El sistema debe tener un registro de los distintos archivos subidos en el sistema.
* El cliente debe utilizar sus propios recursos para particionar el archivo que desea subir.
* Los DataNodes deben garantizar una replicacion de los bloques que reciben.
* El sistema debe permitir al usuario obtener una lista de los archivos disponibles en el sistema.
* El sistema debe implementar MOM como middleware para la transferencia de archivos.
* El sistema debe implementar gRPC como middleware para ejecutar las distintas funciones del sistema.

### ***Requisitos no completados***
* El NameNode Leader debe tener un NameNode Follower a manera de respaldo.

*******

<div id="arquitectura" />

### ***Arquitectura***

![Arquitectura](./imgs/Arquitectura.png)

*******

<div id="ambiente" />
  
### ***3. Descripción del ambiente de desarrollo y técnico***
Este reto fue desarrollado en Python, la carpeta Bootsp inicialmente fue pensada para el desarrollo del servidor de arranque en JavaScript al final se presentaron algunos problemas en el manejo de sockets dentro del lenguaje, que por alguna razón bloqueaban el servidor así que fue adaptado de igual manera a Python para un correcto funcionamiento.

Para el desarrollo de este reto use las siguientes librerías, todas las que son necesarias instalar vienen para ser instaladas dentro del archivo texto requirements.txt:

* **threading , re , socket , random , json , configparser , os**
* **grpc version >= 1.62.0**
* **grpcio-tools version >= 1.62.0**
* **requests version >= 2.31.0**
* **pika version >= 1.3.2**

La red P2P fue pensada como un árbol binario, en la que cada nodo o peer puede tener inicialmente máximo tres conexiones, un padre y dos hijos, en este caso, el nodo padre será el peer al cual nos conectamos en primera instancia los nodos hijos serán peers que vayan llegando a la red. En primera instancia se puede llegar a pensar que si se cae el nodo raíz se cae toda la red, pero esto no es cierto, ya que el primer nodo, es decir el servidor de arranque no está limitado a dos hijos, también tiene como límite tres conexiones las cuales se van agregando de manera aleatoria, se explica un poco mejor en la imagen.

![red](./imgs/red.jpg)

Esto es una representación gráfica de cómo se puede ir organizando la red, cada que un nodo llega, consulta el servidor de arranque por los nodos disponibles en la red y se conecta de manera aleatoria a uno de ellos, en este caso la red seria centralizada, ya que hay que preguntarle a un servidor antes de ingresar a la red, la solución planteada a este problema es tener más de un servidor de arranque en la que cada uno comparte el mismo archivo de peers disponibles, pero esto no se logró a implementar dentro del reto, por lo tanto, considero no se cumplió esa meta; aun así, si desaparece el servidor de arranque, a pesar de que nadie puede ingresar en la red, los que forman parte de ella pueden operar sin problemas.

Un problema planteado con esta solución es el tema de que sucede cuando un nodo abandona la red, ¿los nodos hijos de ese peer que abandona la red se caen y ya no forman parte de la red? la respuesta es no, aunque en este caso el sistema no contempla que el nodo que abandona se caiga por algún factor externo, si el nodo que abandona la red, lo hace mediante la interfaz que es ofrecida por el sistema, reestructura la red para que uno de sus hijos tome su posición y se conecte a los nodos que él estaba conectado a manera de puente.

Esta estructura de árbol facilita la búsqueda de archivos dentro de la red, podemos enviar una petición a todos los nodos que un peer conozca y además, decir que esa solicitud no se la devuelva al peer que se la está realizando, esto para evitar que hayan peticiones redundantes dentro de la red y haya mucho tráfico, en cierto modo se realiza un flooding dentro de la red para buscar el archivo, no se estableció un TTL para las peticiones.

Hablando un poco de la implementación, como se mostró en la imagen correspondiente a la arquitectura, se usaron distintos middlewares para la transferencia de datos entre peers, por un lado, tenemos gRPC que considero es una buena opción para hacer llamados a funciones en un ordenador remoto. Como en un principio se tenía desarrollado el servidor de arranque en JavaScript fue una buena opción para romper las limitaciones entre los lenguajes. Se utiliza sockets para la comunicación entre el cliente/servidor y enviar mensajes como peticiones de archivo y por último se tiene MOM pensado para la transferencia del archivo, aunque no se logró que enviara el archivo y se descargara en el peer origen, se tiene una simulación que envía un mensaje del peer que posee el archivo al peer origen, en este caso considero que es buena opción usar MOM, ya que el peer puede enviar el archivo totalmente, y si por algún casual el peer consumidor pierde conexión, pueda recibir el archivo una vez vuelva a estar en línea.

Se definieron los siguientes puertos para el uso de cada uno de los middlewares:
* **8000** utilizado para la transferencia por sockets.
* **8001** utilizado para la transferencia por gRPC.
* **5672** utilizado para la transferencia por MOM.

*******

<div id="ejecucion" />
  
#### ***4. Descripción de como configurar y como ejecutar el proyecto***

Para ejecutar el código es necesario crear mínimo dos instancias en AWS, para un efecto práctico y que se pueda ver digamos de manera entretenida el reto, es recomendable usar cuatro instancias en AWS. Para un buen funcionamiento seguir por favor las siguientes instrucciones:

Crear dos (la cantidad deseada) instancias de EC2 con OS Ubuntu 20.04, recomendable usar el mismo grupo de seguridad para las instancias creadas para no configurar cada una manualmente. Una vez la instancia este creada, ir a los grupos de seguridad y editar las reglas de entrada, vamos a habilitar los siguientes puertos, cada uno de tipo TCP y permitiendo origen desde 0.0.0.0/0:
  * 8000
  * 8001
  * 5672

En mi caso, la conexión a las instancias lo hago con la aplicación PuTTY, pueden usar cualquiera que deseen que les permita interactuar con la instancia. Vamos a ejecutar los siguientes comandos:

```ssh
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3
sudo apt-get install python3-pip
sudo apt install docker.io
sudo docker run -d --hostname my-rabbit -p 15672:15672 -p 5672:5672 --name rabbit-server rabbitmq:3-management
sudo git clone https://github.com/DannyMelguizo/Telematica-P2P.git
cd Telematica-P2P/Peer/
sudo python3 -m grpc_tools.protoc -I protobufs --python_out=. --pyi_out=. --grpc_python_out=. protobufs/service.proto
sudo python3 -m pip install -r requirements.txt
```

Una vez llegados a este punto, ya es posible ejecutar el proyecto usando el comando:

```ssh
sudo python3 main.py
```

Pero no existiría mucha interacción entre los peers, ya que ninguno tiene archivos para compartir dentro de la red, vamos a hacer una simulación, para ello, tomaremos una de las instancias de AWS como peer de arranque, las otras, serán peers que interactúen con el sistema, vamos a crear una carpeta llamada "shared_files" en la cual crearemos o almacenaremos los archivos que serán compartidos dentro de la red. Para efectos de la simulación podemos crear el mismo archivo en varios peers o diferentes para buscar varios archivos, utilizando el siguiente comando en las instancias que definimos como peers (aclarar que el servidor de arranque también se comporta como peer, solo que por lo general este no debería contener archivos).

```ssh
sudo mkdir shared_files
sudo nano file.txt
```

Cabe mencionar que este directorio se generara por defecto una vez ejecutado el main.py, pero se generara vacío, podemos crear tantos archivos como queramos dentro de esta ruta y serán compartidos dentro de la red.

Una vez hecho esto ahora si podemos ejecutar el archivo main.py con el comando especificado anteriormente, el primero que ejecutaremos será la instancia que definimos como servidor de arranque, cuando el programa nos solicite la IP del servidor de arranque, colocaremos lo siguiente incluyendo la mayúscula.

```ssh
Enter the IP of the Bootstrap Server:
Bootsp
```

Esto le especificara al sistema que somos un servidor de arranque y que atenderemos a los nuevos peers, una vez hecho esto, podemos ejecutar las demás instancias y esta vez, cuando solicite la IP colocaremos la IP del servidor de arranque proporcionada por AWS.

Se nos mostrara una interfaz como la siguiente.

```ssh
Select a number to navigate through the menu.
1. Search for a file
2. List all connections

0. Exit
```

Si introducimos el número 1, nos permite realizar una petición por un archivo, en la cual deberemos especificar el nombre del archivo, teniendo en cuenta que el sistema es case sensitive. Si el sistema no ha encontrado o no encuentra el archivo se nos mostrara un mensaje como el siguiente:

```ssh
Looking for the file...

If the file is found, we will show you a list below.

Press any key to go back to the menu.
```
En el cual podemos apretar cualquier tecla para realizar otra búsqueda, teniendo en cuenta que una vez se encuentre, nos llega una lista con los peers que tienen el archivo y el nombre del archivo para reconocer que búsqueda se realizó.

La otra opción que tiene la interfaz, en este caso el número 2, es para listar las conexiones que ese peer tiene, estas conexiones son a las que él le preguntara por el archivo y confía en que cada conexión le preguntara a su vez a las conexiones que ellos tengan.

Por último, si introducimos la opción 0 abandonaremos la red, pero antes de abandonarla el peer notifica a sus conexiones que saldrá de la red, por lo tanto, se tienen que reestructurar.


*******

<div id="referencias"/>
  
### ***referencias:***
* https://www.rabbitmq.com/tutorials/tutorial-one-python
* https://grpc.io/docs/languages/python/basics/
* https://github.com/jcmtya/st0263-20241/tree/main/Laboratorio%20N1-RPC
* https://interactivavirtual.eafit.edu.co/d2l/le/content/153212/viewContent/807959/View
