#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Implementación de la clase para publicar en Telegram.
"""

import os
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
            
            # Formateo contenido
            formatted_content = self.format_content(content, title, hashtags)
            
            # Publicar mensaje con imágenes si existen
            if images and len(images) > 0:
                # Si hay una sola imagen, envío como foto con texto
                if len(images) == 1:
                    response = bot.send_photo(
                        chat_id=chat_id,
                        photo=open(images[0], 'rb'),
                        caption=formatted_content,
                        parse_mode=ParseMode.HTML
                    )
                # Si hay múltiples imágenes, envío como un grupo de medios
                else:
                    media_group = []
                    for i, img_path in enumerate(images):
                        # El primer elemento del grupo lleva el texto añadido
                        if i == 0:
                            media_group.append(
                                telegram.InputMediaPhoto(
                                    media=open(img_path, 'rb'),
                                    caption=formatted_content,
                                    parse_mode=ParseMode.HTML
                                )
                            )
                        else:
                            media_group.append(
                                telegram.InputMediaPhoto(
                                    media=open(img_path, 'rb')
                                )
                            )
                    
                    response = bot.send_media_group(
                        chat_id=chat_id,
                        media=media_group
                    )
            # Si no hay imágenes, envío solo texto
            else:
                response = bot.send_message(
                    chat_id=chat_id,
                    text=formatted_content,
                    parse_mode=ParseMode.HTML
                )
            
            # Cierro archivos de imágenes
            if images and len(images) > 0:
                for img_path in images:
                    try:
                        open(img_path, 'rb').close()
                    except:
                        pass
            
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