## Apuntes charla matrix

Estos son los apuntes de ayuda para la implementación de la charla de matrix.


1. Actualizamos e insatalamos los comandos básicos

``` bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg 
```


2. Instalamos Docker y Docker-compose(q coñazo)

``` bash
# Añadimos la clave GPG oficial de Docker
sudo mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Añadimos el repositorio a las fuentes de apt
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalamos Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

3. Hay que comprobar que esta guay y activarlo

``` bash
sudo systemctl start docker
sudo systemctl enable docker
sudo systemctl status docker # Pulsa 'q' para salir de esta vista
```

4. Creamos y encendemos un nuevo contenedor Docker

``` bash
sudo docker run -it --rm \
    -v "$PWD/data:/data" \
    -e SYNAPSE_SERVER_NAME=localhost \
    -e SYNAPSE_REPORT_STATS=no \
    matrixdotorg/synapse:latest generate
```

5. Tenemos que ajustar los permisos (nos lo chiva los logs)

``` bash
sudo chown -R 991:991 ./data
```

Se nos han creado estos archivos:

localhost.log.config: Es el archivo que almacena los logs de Synapse

localhost.signing.key: Este archivo contiene una clave de identidad propia a nuestro servidor. Si se filtra nos podrían suplantar el servidor

homeserver.yaml: El archivo de configuración principal

6. Tenemos que editar el homeserver y añadir el pará  metro:

``` homeserver.yaml
enable_registration: true
enable_registration_without_verification: true
```

7. Creamos el docker-compose.yml:

``` docker-compose.yml

services:
  synapse:
    image: matrixdotorg/synapse:latest
    ports:
      - "8008:8008"
    volumes:
      - "./data:/data"

  element:
    image: vectorim/element-web:latest
    ports:
      - "8080:80"
```

8. Lanzamos el docker y refrescamos el synapse porque editamos el archivo homeserver:

``` bash
sudo docker-compose up -d
sudo docker ps
sudo docker-compose restart synapse
```

9. Entramos al localhost:8080 y debería estar todo funcionando

SI HUBIESE QUE REVISAR LOS LOGS:

``` bash
sudo chown -R 991:991 ./data
```




