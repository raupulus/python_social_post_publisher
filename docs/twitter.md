# Configuración de Twitter

Este documento explica cómo configurar una cuenta de Twitter (X) para su uso con Python Social Post Publisher.

## Requisitos previos

- Una cuenta en Twitter
- Acceso al [Portal de Desarrolladores de Twitter](https://developer.twitter.com/)

## Pasos para obtener las credenciales

1. **Solicita acceso a la API de Twitter**:
   - Ve al [Portal de Desarrolladores de Twitter](https://developer.twitter.com/)
   - Inicia sesión con tu cuenta de Twitter
   - Solicita acceso a la API de Twitter (si aún no lo tienes)
   - Selecciona el nivel de acceso que necesitas (Basic es suficiente para publicar tweets)

2. **Crea un proyecto y una aplicación**:
   - Una vez aprobado, crea un nuevo proyecto
   - Dentro del proyecto, crea una nueva aplicación
   - Proporciona un nombre y una descripción para tu aplicación

3. **Configura los permisos de la aplicación**:
   - En la configuración de la aplicación, ve a la pestaña "App permissions"
   - Cambia los permisos a "Read and Write" para poder publicar tweets

4. **Genera las claves y tokens**:
   - Ve a la pestaña "Keys and tokens"
   - Genera o regenera las siguientes credenciales:
     - API Key y API Key Secret
     - Access Token y Access Token Secret

5. **Guarda tus credenciales**:
   - Guarda todas estas credenciales en un lugar seguro
   - Las necesitarás para configurar el publicador

## Configuración en el archivo .env

Añade las siguientes variables a tu archivo `.env` en el directorio `data/profiles/[nombre_proyecto].env`:

```
TWITTER_ENABLED=true
TWITTER_API_KEY=tu_api_key
TWITTER_API_SECRET=tu_api_secret
TWITTER_ACCESS_TOKEN=tu_access_token
TWITTER_ACCESS_TOKEN_SECRET=tu_access_token_secret
```

Reemplaza los valores con tus credenciales obtenidas en el paso anterior.

## Verificación

Para verificar que la configuración es correcta:

1. Asegúrate de que `TWITTER_ENABLED` está establecido en `true`
2. Ejecuta el publicador con un mensaje de prueba
3. Comprueba tu perfil de Twitter para ver si el mensaje se ha publicado correctamente

## Solución de problemas

Si encuentras problemas al publicar en Twitter:

1. **Verifica las credenciales**: Asegúrate de que todas las claves y tokens son correctos.
2. **Comprueba los permisos**: Verifica que la aplicación tiene permisos de lectura y escritura.
3. **Revisa los logs**: Consulta los logs del publicador para ver si hay mensajes de error específicos.
4. **Límites de caracteres**: Twitter tiene un límite de 280 caracteres por tweet. Asegúrate de que tu contenido no excede este límite.
5. **Límites de la API**: Twitter tiene límites en el número de solicitudes que puedes hacer a la API. Si publicas muchos tweets en poco tiempo, podrías alcanzar estos límites.
6. **Formato de imágenes**: Twitter acepta imágenes en formato JPG, PNG y GIF. Asegúrate de que tus imágenes están en uno de estos formatos.
7. **Tamaño de imágenes**: Twitter tiene límites en el tamaño de las imágenes. El publicador redimensiona automáticamente las imágenes, pero si tienes problemas, intenta con imágenes más pequeñas.

## Notas importantes

- Twitter (X) ha cambiado significativamente sus políticas de API. La versión gratuita tiene acceso muy limitado.
- Esta implementación utiliza un enfoque híbrido:
  - API v1.1 para subir imágenes (disponible en el nivel gratuito)
  - API v2 para publicar tweets (disponible en el nivel gratuito con limitaciones)
- Si encuentras errores de acceso, es posible que necesites actualizar a un plan de pago de la API de Twitter.
- El nivel gratuito tiene límites muy estrictos (actualmente 1,500 tweets/mes y 50 tweets/día).
- Asegúrate de seguir las [Reglas de Twitter para desarrolladores](https://developer.twitter.com/en/developer-terms/policy) para evitar que tu aplicación sea suspendida.

## Recursos adicionales

- [Documentación oficial de la API de Twitter](https://developer.twitter.com/en/docs)
- [Biblioteca Tweepy](https://www.tweepy.org/)
