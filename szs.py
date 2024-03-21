import os

def reconstruir_archivo(nombre_archivo_original):
    bloques = []
    # Buscamos todos los archivos que siguen el formato de nombre generado en la división
    for filename in os.listdir('.'):
        if filename.startswith(nombre_archivo_original):
            bloques.append(filename)

    # Ordenamos los bloques según su número
    bloques.sort(key=lambda x: int(x.rsplit('.', 1)[1]))

    print(bloques)

    datos_reconstruidos = b""
    for bloque in bloques:
        with open(bloque, 'rb') as f:
            nombre_archivo, tamano_original, posicion = f.readline().decode().strip(), int(f.readline().decode().strip()), f.readline().decode().strip()
            datos_reconstruidos += f.read()
    
    # Guardamos los datos reconstruidos en un nuevo archivo
    with open(nombre_archivo_original, 'wb') as f:
        f.write(datos_reconstruidos)


reconstruir_archivo("Aerosmith - Dream On.mp3")