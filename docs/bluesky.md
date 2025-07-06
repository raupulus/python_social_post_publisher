# Configuración de Bluesky

Este documento explica cómo configurar una cuenta de Bluesky para su uso con Python Social Post Publisher.

## Requisitos previos

- Una cuenta en [Bluesky](https://bsky.app/)
- Acceso a la configuración de tu cuenta

## Pasos para obtener las credenciales

1. **Inicia sesión** en tu cuenta de Bluesky.

2. **Crea una contraseña de aplicación**:
   - Ve a la configuración de tu cuenta (icono de perfil > "Settings")
   - Selecciona "App passwords"
   - Haz clic en "Add app password"
   - Proporciona un nombre para la aplicación (por ejemplo, "Python Social Post Publisher")
   - Guarda la contraseña generada en un lugar seguro

3. **Obtén tu identificador**:
   - Tu identificador es tu nombre de usuario (handle) o el correo electrónico asociado a tu cuenta
   - Por ejemplo: `usuario.bsky.social` o `correo@ejemplo.com`

## Configuración en el archivo .env

Añade las siguientes variables a tu archivo `.env` en el directorio `data/profiles/[nombre_proyecto].env`:

```
BLUESKY_ENABLED=true
BLUESKY_IDENTIFIER=tu_identificador
BLUESKY_PASSWORD=tu_contraseña_de_app
```

Reemplaza:
- `tu_identificador` con tu nombre de usuario o correo electrónico
- `tu_contraseña_de_app` con la contraseña de aplicación generada en el paso anterior

## Verificación

Para verificar que la configuración es correcta:

1. Asegúrate de que `BLUESKY_ENABLED` está establecido en `true`
2. Ejecuta el publicador con un mensaje de prueba
3. Comprueba tu perfil de Bluesky para ver si el mensaje se ha publicado correctamente

## Solución de problemas

Si encuentras problemas al publicar en Bluesky:

1. **Verifica las credenciales**: Asegúrate de que el identificador y la contraseña de la aplicación son correctos.
2. **Regenera la contraseña**: Si la contraseña no funciona, intenta generar una nueva contraseña de aplicación.
3. **Revisa los logs**: Consulta los logs del publicador para ver si hay mensajes de error específicos.
4. **Límites de caracteres**: Bluesky tiene un límite de 300 caracteres por publicación. Asegúrate de que tu contenido no excede este límite.
5. **Formato de imágenes**: Bluesky acepta imágenes en formato JPG, PNG y GIF. Asegúrate de que tus imágenes están en uno de estos formatos.
6. **Tamaño de imágenes**: Bluesky tiene límites en el tamaño de las imágenes. El publicador redimensiona automáticamente las imágenes, pero si tienes problemas, intenta con imágenes más pequeñas.

## Características específicas de Bluesky

- **Límite de imágenes**: Bluesky permite hasta 4 imágenes por publicación.
- **Etiquetas**: Bluesky no utiliza hashtags de la misma manera que otras redes sociales, pero el publicador convertirá tus hashtags en texto con el símbolo # para mantener la consistencia.
- **Formato de texto**: Bluesky no admite formato de texto enriquecido (como negrita o cursiva) en este momento.

## Notas importantes

- Bluesky es una plataforma relativamente nueva y su API puede cambiar con el tiempo.
- Las contraseñas de aplicación son específicas para cada aplicación y pueden ser revocadas individualmente desde la configuración de tu cuenta.
- Nunca compartas tu contraseña de aplicación con nadie.

## Recursos adicionales

- [Sitio web oficial de Bluesky](https://bsky.app/)
- [Documentación de la API de Bluesky (AT Protocol)](https://atproto.com/docs)