#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Implementación de la clase para publicar en Twitter.
"""

import os
import tweepy
from . import SocialNetwork

class Twitter(SocialNetwork):
    """
    Clase para publicar contenido en Twitter.
    """

    def __init__(self):
        """
        Inicializo la conexión con Twitter.
        """
        super().__init__()

    def publish(self, content, title=None, hashtags=None, project=None, images=None):
        """
        Publico contenido en Twitter.

        Args:
            content (str): Contenido a publicar
            title (str, optional): Título del contenido
            hashtags (list, optional): Lista de hashtags
            project (str): Nombre del proyecto
            images (list, optional): Lista de rutas a imágenes

        Returns:
            dict: Resultado de la publicación
        """
        # Cargar configuración del proyecto
        self.load_config(project)

        # Verificar si Twitter está habilitado
        if os.getenv('TWITTER_ENABLED', 'false').lower() != 'true':
            return {'status': 'skipped', 'message': 'Twitter no está habilitado para este proyecto'}

        # Obtengo credenciales
        api_key = os.getenv('TWITTER_API_KEY')
        api_secret = os.getenv('TWITTER_API_SECRET')
        access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

        if not api_key or not api_secret or not access_token or not access_token_secret:
            return {'status': 'error', 'message': 'Faltan credenciales para Twitter'}

        try:
            # Verifico si el contenido supera el límite de caracteres (280 para Twitter)
            if len(content) > 280:
                # Si supera el límite, solo envío el contenido truncado sin título ni hashtags
                formatted_content = content[:277] + "..."
            else:
                # Si no supera el límite, formateo normalmente con título y hashtags
                formatted_content = self.format_content(content, title, hashtags)

                # Verifico si después de añadir título y hashtags supera el límite
                if len(formatted_content) > 280:
                    formatted_content = formatted_content[:277] + "..."

            # Uso la API v1.1 solo para subir imágenes (disponible en el nivel gratuito)
            auth = tweepy.OAuth1UserHandler(
                api_key, api_secret, access_token, access_token_secret
            )
            api_v1 = tweepy.API(auth)

            # Subo imágenes si existen
            media_ids = []
            if images and len(images) > 0:
                for img_path in images:
                    media = api_v1.media_upload(img_path)
                    media_ids.append(media.media_id)

            # Uso la API v2 para publicar el tweet
            client = tweepy.Client(
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret
            )

            # Publico tweet
            if media_ids:
                response = client.create_tweet(
                    text=formatted_content,
                    media_ids=media_ids
                )
            else:
                response = client.create_tweet(
                    text=formatted_content
                )

            # Extraigo el ID del tweet de la respuesta de la API v2
            tweet_id = response.data['id']

            return {
                'status': 'success',
                'message': 'Publicado correctamente en Twitter',
                'post_id': tweet_id,
                'url': f"https://twitter.com/user/status/{tweet_id}"
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error al publicar en Twitter: {str(e)}'
            }
