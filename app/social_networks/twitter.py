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
            # Autentico con Twitter
            auth = tweepy.OAuth1UserHandler(
                api_key, api_secret, access_token, access_token_secret
            )
            api = tweepy.API(auth)
            
            # Formateo contenido
            formatted_content = self.format_content(content, title, hashtags)
            
            # Verifico longitud del tweet (280 caracteres máximo) y reduzco
            if len(formatted_content) > 280:
                formatted_content = formatted_content[:277] + "..."
            
            # Subo imágenes si existen
            media_ids = []
            if images and len(images) > 0:
                for img_path in images:
                    media = api.media_upload(img_path)
                    media_ids.append(media.media_id)
            
            # Publico tweet
            if media_ids:
                response = api.update_status(
                    status=formatted_content,
                    media_ids=media_ids
                )
            else:
                response = api.update_status(formatted_content)
            
            return {
                'status': 'success',
                'message': 'Publicado correctamente en Twitter',
                'post_id': response.id,
                'url': f"https://twitter.com/user/status/{response.id}"
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error al publicar en Twitter: {str(e)}'
            }