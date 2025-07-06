#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Implementación de la clase para publicar en Telegram.
"""

import os
import asyncio
import telegram
from telegram.constants import ParseMode
from . import SocialNetwork

class Telegram(SocialNetwork):
    """
    Clase para publicar contenido en Telegram.
    """

    def __init__(self):
        """
        Inicializo la conexión con Telegram.
        """
        super().__init__()

    async def _send_telegram_message(self, bot, chat_id, formatted_content, images=None):
        """
        Envía un mensaje a Telegram de forma asíncrona.

        Args:
            bot: Instancia del bot de Telegram
            chat_id: ID del chat donde enviar el mensaje
            formatted_content: Contenido formateado del mensaje
            images: Lista de rutas a imágenes (opcional)

        Returns:
            El resultado de la operación de envío
        """
        # Publicar mensaje con imágenes si existen
        if images and len(images) > 0:
            # Si hay una sola imagen, envío como foto con texto
            if len(images) == 1:
                with open(images[0], 'rb') as photo:
                    response = await bot.send_photo(
                        chat_id=chat_id,
                        photo=photo,
                        caption=formatted_content,
                        parse_mode=ParseMode.HTML
                    )
                return response
            # Si hay múltiples imágenes, envío como un grupo de medios
            else:
                media_group = []
                file_handles = []

                try:
                    for i, img_path in enumerate(images):
                        file_handle = open(img_path, 'rb')
                        file_handles.append(file_handle)

                        # El primer elemento del grupo lleva el texto añadido
                        if i == 0:
                            media_group.append(
                                telegram.InputMediaPhoto(
                                    media=file_handle,
                                    caption=formatted_content,
                                    parse_mode=ParseMode.HTML
                                )
                            )
                        else:
                            media_group.append(
                                telegram.InputMediaPhoto(
                                    media=file_handle
                                )
                            )

                    response = await bot.send_media_group(
                        chat_id=chat_id,
                        media=media_group
                    )
                    return response
                finally:
                    # Cierro los manejadores de archivos
                    for handle in file_handles:
                        handle.close()
        # Si no hay imágenes, envío solo texto
        else:
            response = await bot.send_message(
                chat_id=chat_id,
                text=formatted_content,
                parse_mode=ParseMode.HTML
            )
            return response

    def publish(self, content, title=None, hashtags=None, project=None, images=None):
        """
        Publica contenido en Telegram.

        Args:
            content (str): Contenido a publicar
            project (str): Nombre del proyecto
            title (str, optional): Título del contenido
            hashtags (list, optional): Lista de hashtags
            images (list, optional): Lista de rutas a imágenes

        Returns:
            dict: Resultado de la publicación
        """
        # Cargar configuración del proyecto
        self.load_config(project)

        # Verificar si Telegram está habilitado
        if os.getenv('TELEGRAM_ENABLED', 'false').lower() != 'true':
            return {'status': 'skipped', 'message': 'Telegram no está habilitado para este proyecto'}

        # Obtener credenciales
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')

        if not bot_token or not chat_id:
            return {'status': 'error', 'message': 'Faltan credenciales para Telegram'}

        try:
            # Inicializo bot de Telegram
            bot = telegram.Bot(token=bot_token)

            # Verifico si el contenido supera el límite de caracteres (4096 para Telegram)
            if len(content) > 4096:
                # Si supera el límite, solo envío el contenido truncado sin título ni hashtags
                formatted_content = content[:4093] + "..."
            else:
                # Si no supera el límite, formateo normalmente con título y hashtags
                formatted_content = self.format_content(content, title, hashtags)

                # Verifico si después de añadir título y hashtags supera el límite
                if len(formatted_content) > 4096:
                    formatted_content = formatted_content[:4093] + "..."

            # Ejecuto la función asíncrona en un contexto síncrono
            response = asyncio.run(self._send_telegram_message(bot, chat_id, formatted_content, images))

            return {
                'status': 'success',
                'message': 'Publicado correctamente en Telegram',
                'post_id': response.message_id if isinstance(response, telegram.Message) else response[0].message_id
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error al publicar en Telegram: {str(e)}'
            }
