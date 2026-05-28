# Previamente tenemos que descargarnos la libreria request si no la tenemos instalada con:
# pip install request

import requests
import json
import secrets

# Para que funcione tenemos que crear un usuario vacío a nivel de "bot" dentro de la base de datos
# Este bot con permisos de adminsitrador será el encargado de crear salas automáticamente

# ACLARACIION IMPORTANTE:
# Tenemo que obtener el token del usuario bot que hemos creado, como esto es un scrip te prueba
# lo hemos inyectado directamente en el código, lo cual nos ocasiona un problema gordo de seguridad
# esto hay que arreglarlo para la implementación final.


# VARIABLES GLOBALES
MATRIX_URL = "https://matrix.ugr.es"
TOKEN = "syt_INSERTA-AQUI-EL-TOKEN"

# Tiene la sigueinte estructura
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# función auxiliar para transformar el correo electronico con el ID de matrix
# aquí se diferencia a alumnos de profesores de la siguinte manera:
# alumno@correo.ugr.es -> e.alumno:matrix.ugr.es
# profesor@ugr.es -> profesor:matrix.ugr.es
def obtener_ids_desde_correos(correo):

    # separamos el nombre del dominio
    nombre, dominio = correo.split("@")

    
    if dominio == "correo.ugr.es":

        id = f"@e.{nombre}:matrix.ugr.es"

    elif dominio == "ugr.es":

        id = f"@{nombre}:matrix.ugr.es"

    else:
        print(f"CUIDADO, EL CORREO: '{correo}' - ha intentado insertarse con un DOMINIO NO PERMITIDO")
        return
        
    return id

# Funcion que dado unlistado de correos, los registra en la base de datos de Matrix
# nos returnea una lista con todos los ids listos para usar dentro de la creación de las salas de "prado_requests.py"

def registrar_usuarios(correos):

    # Para ir guardando los correos
    ids = []

    for correo in correos:

        id = obtener_ids_desde_correos(correo)

        # Ha pasado el filtro y hemos verificado que tiene un id valido
        if id:

            # url a la que se realiza la petición para interactuar con el usuario
            url_usuario = f"{MATRIX_URL}/_synapse/admin/v2/users/{id}"

            try:

                # Comprobamos si el usuario ya existe o no
                comprobador = requests.get(url_usuario, headers=HEADERS)
                codigo = comprobador.status_code

                #Si nos devuelve el codigo de confirmación 200 implica que si existe
                if codigo == 200: 

                    print(f" EL usuario {id} con correo {correo} ya existe, así que nos saltamos su creación")
                    ids.append(id)
                
                # Si nos devuelve el codigo 404 implica que no se ha encontrado, así que lo creamos
                elif codigo == 404:


                    # Le asignamos una contraseña aleatoria de 16 caracteres. 
                    # (Como usarán SAML de la UGR, esta contraseña nunca la usarán ni la sabrán así que tampoco es relevante)
                    password_aleatoria = secrets.token_urlsafe(16)


                    # definimos el json que enviaremos
                    payload = {
                        "password": password_aleatoria,
                        "displayname": correo.split("@")[0] # Nombre a mostrar provisional
                    }

                    # Realizamos la petición para insertar el usuario
                    respuesta_crear = requests.put(url_usuario, headers=HEADERS, json=payload)
                    respuesta_crear.raise_for_status()

                    print(f"Usuario {id} con correo {correo} SE HA CREADO CON EXITO")
                    ids.append(id)

                else:

                    print(f"ERROR: se ha detectado un codigo de respuesta desconocido al crear al usuario {id}")
                    print(f"Codigo de respuesta: {codigo}")

            except requests.exceptions.RequestException as e: 

                print(f"ERROR: ha habido algun error al procesar el correo {correo}: {e} ") 

    return ids

if __name__ == "__main__":

# Listado de correos para la prueba
    correos = [
        "profesor@ugr.es",
        "alumno1@correo.ugr.es",
        "alumno2@correo.ugr.es"
    ]

    ids =  registrar_usuarios(correos)

    print("Los siguientes IDs de Matrix se ha insertado correctamente y están listos para ser insertados en las sala correspondientes:")

    for id in ids:
        print(f"{id}")
        



