# Previamente tenemos que descargarnos la libreria request si no la tenemos instalada con:
# pip install request

import request
import json

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


# Función que dado el nombre de la asignatra y el id de su profesor, crea la sala correspomdiente
# Actualmente solo está diseñada para devolver un usuario administrador en la creacion (profesor)
# Returnea el ID de la sala generada
def crear_sala_asignatura(nombre_asignatura, id_profesor):

    # url a la que se realiza la petición
    url = f"{MATRIX_URL}/_matrix/client/v3/createRoom"

    # definimos el json que enviaremos
    payload = {
        "name": nombre_asignatura,
        "preset": "private_chat",
        "creation_content": {
            "m.federate": False  # Para que solo se puedan unir usuarios de matrix.ugr.es
        },
        "initial_state": [
            {
                "type": "m.room.power_levels",
                "state_key": "",
                "content": {
                    "users": { # Aquí podríamos añadir tantos usuarios como queramos
                        id_profesor: 100  # El nivel 100 implica permisos de administrador
                    }
                }
            }
        ]
    }

    # Realizamos la petición
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        response.raise_for_status() # verifica si la solicitud HTTP no fue exitosa, y neesita lanzar una excepción

        datos = response.json()
        id_sala = datos.get("room_id") 

        print(f"SALA CREADA CON EXITO. Nombre de la asignatura: {nombre_asignatura} - ID de la sala: {id_sala}")

        return id_sala
    
    except requests.exceptions.RequestException as e:

        print(f"ERROR AL CREAR LA SALA. Nombre de la asignatura: {nombre_asignatura}")
        print(f"Detalles del error: {e}")
        return 


# Función el dado el id de la sala y el listado de sus alumnos los introduce en la sala como usuarios normales
def matricular_alumnos(sala_id, lista_alumnos):

    # url a la que se realiza la petición
    url = f"{MATRIX_URL}/_synapse/admin/v1/join/{sala_id}"

    # Recorremos todos los alumnos y para cada uno de ellos realizamos una peticion
    for alumno in lista_alumnos:

        # definimos el json que enviaremos
        payload = {"user_id": alumno}

        try:
            response = requests.post(url, headers=HEADERS, json=payload)
            response.raise_for_status() # verifica si la solicitud HTTP no fue exitosa, y neesita lanzar una excepción
            print(f"ALUMNO: {alumno} matriculado correctamente en la sala con id: {sala_id}")

        except requests.exceptions.RequestException as e:

            print(f"ERROR AL MATRICULAR EL ALUMNO: {alumno} - en la sala con id: {sala_id}")
            print(f"Detalles del error: {e}")



# Función main para comprobar la funcionalidad y que sirva como explicación para como crear salas y matricular alumnos
if __name__ == "__main__":

    # ESTOS DATOS SE LOS TENDRÍAMOS QUE PASAR DE LA INFORMACIÓN DE LA CLASE
    asignatura = "Ingeniería de Servidores"
    profesor = "@profesor:matrix.ugr.es"
    alumnos = [
        "@e.alumno1:matrix.ugr.es",
        "@e.alumno2:matrix.ugr.es",
        "@e.alumno3:matrix.ugr.es"
    ]

    # Creamos la sala
    id_sala = crear_sala_asignatura(asignatura, profesor)

    # Metemos a los alumnos si se ha creado bien la sala
    if id_sala:
        matricular_alumnos(id_sala, alumnos)

    
