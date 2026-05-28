import logging
from synapse.handlers.saml import DefaultSamlMappingProvider

logger = logging.getLogger(__name__)

class UgrSamlMappingProvider(DefaultSamlMappingProvider):
    def __init__(self, parsed_config, module_api):
        super().__init__(parsed_config, module_api)
        logger.warning("[UGR SAML] Mapeador UGR inicializado correctamente.")

    # Función que genera el vínculo con la base de datos
    def get_remote_user_id(self, saml_response, cliente_redirect_url):
        uid = saml_response.ava.get("uid", [None])[0]
        logger.warning(f"[UGR SAML] Vinculando usuario de la base de dato con uid: {uid}")

        if not uid:
           raise Exception("ERROR: Atributo uid no encontrado.")

        return uid

    # Función para crear el nombre de usuario en Matrix
    def saml_response_to_user_attributes(self, saml_response, failures, client_redirect_url):
        uid = saml_response.ava.get("uid",[None])[0]
        logger.warning(f"[UGR SAML] Generando nombre matrix para: {uid}")

        if not uid:
            raise Exception("ERROR: atributo uid no encontrado tras la traducción de PySAML2")

        email = uid.lower() # Lo pasamos todo a minúscula 
        nombre, dominio = email.split('@')

        if dominio == "ugr.es":
            nuevo_nombre = nombre # Para los profesores devolvemos el nombre antes del @ exclusivamente
        elif dominio == "correo.ugr.es":
            nuevo_nombre = f"e.{nombre}" # Para los alumnos devolvemos el nombre con "e.nombre" de antes del @
        else:
            raise Exception ("CUIDADO: se ha detectado un login con un correo con dominio distinto de 'ugr.es' o 'correo.ugr.es'")

        # Si el nombre ya existe, añadimos el número de fallos al final para evitar colisiones
        if failures > 0:
            nuevo_nombre = f"{nuevo_nombre}{failures}"

        logger.warning(f"[UGR SAML] Nombre asignado (mxid_localpart): {nuevo_nombre}")

        # Devolvemos el diccionario exacto que nos pide la documentación de Synapse
        return {
            "mxid_localpart": nuevo_nombre, # ID interno (ej. @e.pepe:matrix.ugr.es)
            "displayname": nuevo_nombre,  # Nombre visual en la aplicación
            "emails": [email]       # Vincula el correo real a la cuenta
        }