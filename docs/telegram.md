# Configuración de Telegram

Este documento explica cómo configurar un bot de Telegram para su uso con Python Social Post Publisher.

## Requisitos previos

- Una cuenta en Telegram
- Acceso a la aplicación de Telegram (móvil o escritorio)

## Pasos para crear un bot de Telegram

1. **Inicia una conversación con BotFather**:
   - Abre Telegram y busca `@BotFather`
   - Inicia una conversación con BotFather

2. **Crea un nuevo bot**:
   - Envía el comando `/newbot` a BotFather
   - Proporciona un nombre para tu bot (por ejemplo, "Mi Publicador Social")
   - Proporciona un nombre de usuario para tu bot (debe terminar en "bot", por ejemplo, "MiPublicadorBot")

3. **Obtén el token del bot**:
   - BotFather te proporcionará un token de acceso para tu bot
   - Este token es necesario para que el publicador pueda enviar mensajes a través del bot
   - Guarda este token en un lugar seguro

4. **Crea un canal o grupo** (opcional):
   - Si quieres que tu bot publique en un canal o grupo, crea uno nuevo o usa uno existente
   - Añade tu bot como administrador del canal o grupo

5. **Obtén el ID del chat**:
   - Para obtener el ID del chat (canal o grupo), puedes usar varios métodos:
     - **Método 1**: Añade el bot `@getidsbot` al canal o grupo y te proporcionará el ID
     - **Método 2**: Envía un mensaje al canal o grupo, luego accede a `https://api.telegram.org/bot<TU_TOKEN>/getUpdates` (reemplaza `<TU_TOKEN>` con el token de tu bot) y busca el campo `chat.id` en la respuesta JSON
     - **Método 3**: Si es un canal público, el ID suele ser `-100` seguido del número que aparece en la URL del canal

## Configuración en el archivo .env

Añade las siguientes variables a tu archivo `.env` en el directorio `data/profiles/[nombre_proyecto].env`:

```
TELEGRAM_ENABLED=true
TELEGRAM_BOT_TOKEN=tu_token_del_bot
TELEGRAM_CHAT_ID=id_del_chat
```

Reemplaza:
- `tu_token_del_bot` con el token obtenido de BotFather
- `id_del_chat` con el ID del chat, canal o grupo donde quieres publicar

## Verificación

Para verificar que la configuración es correcta:

1. Asegúrate de que `TELEGRAM_ENABLED` está establecido en `true`
2. Ejecuta el publicador con un mensaje de prueba
3. Comprueba el canal o grupo de Telegram para ver si el mensaje se ha publicado correctamente

## Solución de problemas

Si encuentras problemas al publicar en Telegram:

1. **Verifica el token del bot**: Asegúrate de que el token del bot es correcto.
2. **Comprueba el ID del chat**: Verifica que el ID del chat es correcto.
3. **Permisos del bot**: Asegúrate de que el bot tiene permisos para publicar en el canal o grupo.
4. **Revisa los logs**: Consulta los logs del publicador para ver si hay mensajes de error específicos.
5. **Formato de mensajes**: Telegram tiene algunas limitaciones en el formato de los mensajes. Si estás usando formato HTML o Markdown, asegúrate de que está correctamente formateado.
6. **Tamaño de imágenes**: Telegram tiene límites en el tamaño de las imágenes. El publicador redimensiona automáticamente las imágenes, pero si tienes problemas, intenta con imágenes más pequeñas.

## Características adicionales

- **Formato de texto**: Telegram permite formato HTML básico o Markdown en los mensajes. Puedes usar estas opciones para dar formato a tus publicaciones.
- **Grupos de imágenes**: Telegram permite enviar hasta 10 imágenes en un solo mensaje como un álbum. El publicador está configurado para enviar hasta 4 imágenes como un álbum.
- **Bots en canales**: Los bots pueden publicar en canales, pero no pueden ver los mensajes de otros usuarios en el canal.

## Recursos adicionales

- [Documentación oficial de la API de Telegram para bots](https://core.telegram.org/bots/api)
- [Biblioteca python-telegram-bot](https://python-telegram-bot.readthedocs.io/)