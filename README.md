# Python Social Post Publisher

Herramienta para publicar contenido en múltiples redes sociales (Mastodon, 
Twitter, Telegram, Bluesky) con soporte para múltiples perfiles. 

Este servicio está diseñado para ser consumido por otras aplicaciones en un 
entorno local, proporcionando un endpoint API simple para publicar contenido en 
varias redes sociales simultáneamente.

El proyecto permite configurar diferentes perfiles para diferentes proyectos, 
cada uno con sus propias credenciales y configuraciones para las redes sociales. 
Esto facilita la gestión de múltiples cuentas y la publicación selectiva en 
diferentes plataformas según las necesidades de cada proyecto.

## Características

- Publicación simultánea en múltiples redes sociales:
  - Mastodon
  - Twitter (X)
  - Telegram
  - Bluesky
- Soporte para múltiples perfiles/proyectos
- Procesamiento de hashtags
- Soporte para imágenes (hasta 4 por publicación)
- API REST simple para integración con otras aplicaciones
- Despliegue fácil con Docker y Docker Compose

## Requisitos

- Python 3.13 o superior
- Docker y Docker Compose (para despliegue en contenedor)
- Credenciales para las redes sociales que deseas utilizar

## Instalación

### Usando venv (entorno virtual)

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/python_social_post_publisher.git
   cd python_social_post_publisher
   ```

2. Crea un entorno virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura tus perfiles en el directorio `data/profiles/`:
   ```bash
   mkdir -p data/profiles
   # Crea un archivo .env para cada proyecto, por ejemplo:
   # data/profiles/proyecto1.env
   # data/profiles/proyecto2.env
   # data/profiles/proyecto3.env
   # Ten en cuenta que ese nombre lo pasarás luego a la api en el campo "project"
   ```

5. Ejecuta la aplicación:
   ```bash
   python app/app.py
   ```

### Usando Docker

1. Clona el repositorio:
   ```bash
   git clone https://github.com/raupulus/python_social_post_publisher.git
   cd python_social_post_publisher
   ```

2. Configura tus perfiles en el directorio `data/profiles/`:
   ```bash
   mkdir -p data/profiles
   # Crea un archivo .env para cada proyecto, por ejemplo:
   # data/profiles/proyecto1.env
   # data/profiles/proyecto2.env
   # data/profiles/proyecto3.env
   # Ten en cuenta que ese nombre lo pasarás luego a la api en el campo "project"
   ```

3. Construye y ejecuta el contenedor:
   ```bash
   docker-compose up -d
   ```

## Uso

### Endpoint API

La API expone un único endpoint:

- **URL**: `/publish`
- **Método**: `POST`
- **Cuerpo de la solicitud (JSON)**:
  ```json
  {
    "content": "Contenido a publicar",
    "title": "Título opcional",
    "hashtags": ["tag1", "tag2", "tag3"],
    "project": "nombre_del_proyecto",
    "images": ["url_imagen1", "url_imagen2", "data:image/jpeg;base64,base64_encoded_image"]
  }
  ```

- **Respuesta (JSON)**:
  ```json
  {
    "success": true,
    "results": [
      {
        "network": "Mastodon",
        "success": true,
        "result": { ... }
      },
      {
        "network": "Twitter",
        "success": true,
        "result": { ... }
      }
    ]
  }
  ```

### Ejemplo de uso con curl

```bash
curl -X POST http://localhost:8080/publish \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Este es un mensaje de prueba",
    "hashtags": ["test", "ejemplo"],
    "project": "proyecto1",
    "images": ["https://ejemplo.com/imagen.jpg"]
  }'
```

## Configuración

Cada proyecto debe tener su propio archivo `.env` en el directorio `data/profiles/`. Por ejemplo, para un proyecto llamado "proyecto1", el archivo sería `data/profiles/proyecto1.env`.

Consulta la documentación específica para cada red social en el directorio `docs/` para obtener instrucciones detalladas sobre cómo configurar cada plataforma.

## Documentación

- [Configuración de Mastodon](docs/mastodon.md)
- [Configuración de Twitter](docs/twitter.md)
- [Configuración de Telegram](docs/telegram.md)
- [Configuración de Bluesky](docs/bluesky.md)

## Licencia

Este proyecto está licenciado bajo la [GNU General Public License v3.0](LICENSE).
