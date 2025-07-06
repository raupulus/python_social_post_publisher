# Configuración de Mastodon

Este documento explica cómo configurar una cuenta de Mastodon para su uso con Python Social Post Publisher.

## Requisitos previos

- Una cuenta en una instancia de Mastodon (por ejemplo, [mastodon.social](https://mastodon.social/))
- Acceso a la configuración de desarrollador de tu cuenta

## Pasos para obtener las credenciales

1. **Inicia sesión** en tu cuenta de Mastodon.

2. **Accede a la configuración de desarrollador**:
   - Ve a `Preferencias` (icono de engranaje)
   - Selecciona `Desarrollo`
   - Haz clic en `Aplicaciones nuevas`

3. **Crea una nueva aplicación**:
   - **Nombre**: Python Social Post Publisher (o el nombre que prefieras)
   - **Sitio web**: Puedes dejar este campo en blanco o poner la URL de tu proyecto
   - **Permisos**: Marca las siguientes casillas:
     - `read:accounts` - Para leer información de la cuenta
     - `write:media` - Para subir imágenes
     - `write:statuses` - Para publicar contenido

4. **Haz clic en "Enviar"** para crear la aplicación.

5. **Obtén las credenciales**:
   - Una vez creada la aplicación, verás una página con tus credenciales.
   - Necesitarás el `Token de acceso` para configurar el publicador.

## Configuración en el archivo .env

Añade las siguientes variables a tu archivo `.env` en el directorio `data/profiles/[nombre_proyecto].env`:

```
MASTODON_ENABLED=true
MASTODON_API_BASE_URL=https://mastodon.social
MASTODON_ACCESS_TOKEN=tu_token_de_acceso
```

Reemplaza:
- `https://mastodon.social` con la URL de tu instancia de Mastodon
- `tu_token_de_acceso` con el token obtenido en el paso anterior

## Verificación

Para verificar que la configuración es correcta:

1. Asegúrate de que `MASTODON_ENABLED` está establecido en `true`
2. Ejecuta el publicador con un mensaje de prueba
3. Comprueba tu perfil de Mastodon para ver si el mensaje se ha publicado correctamente

## Solución de problemas

Si encuentras problemas al publicar en Mastodon:

1. **Verifica las credenciales**: Asegúrate de que el token de acceso es correcto y no ha expirado.
2. **Comprueba los permisos**: Verifica que la aplicación tiene los permisos necesarios.
3. **Revisa los logs**: Consulta los logs del publicador para ver si hay mensajes de error específicos.
4. **Límites de caracteres**: Mastodon tiene un límite de 500 caracteres por publicación. Asegúrate de que tu contenido no excede este límite.
5. **Formato de imágenes**: Mastodon acepta imágenes en formato JPG, PNG y GIF. Asegúrate de que tus imágenes están en uno de estos formatos.

## Recursos adicionales

- [Documentación oficial de la API de Mastodon](https://docs.joinmastodon.org/api/)
- [Biblioteca Mastodon.py](https://mastodonpy.readthedocs.io/en/stable/)