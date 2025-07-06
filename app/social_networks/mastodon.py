#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Implementación de la clase para publicar en Mastodon.
"""

import os
from mastodon import Mastodon as MastodonAPI
from . import SocialNetwork

class Mastodon(SocialNetwork):
    """
    Clase para publicar contenido en Mastodon.
    """
    
    def __init__(self):
        """
        Inicializo la conexión con Mastodon.
        """
        super().__init__()
    
    def publish(self, content, title=None, hashtags=None, project=None, images=None):
        """
        Publico contenido en Mastodon.
        
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
        
        # Verificar si Mastodon está habilitado
        if os.getenv('MASTODON_ENABLED', 'false').lower() != 'true':
            return {'status': 'skipped', 'message': 'Mastodon no está habilitado para este proyecto'}
        
        # Obtener credenciales
        api_base_url = os.getenv('MASTODON_API_BASE_URL')
        access_token = os.getenv('MASTODON_ACCESS_TOKEN')
        
        if not api_base_url or not access_token:
            return {'status': 'error', 'message': 'Faltan credenciales para Mastodon'}
        
        try:
            # Inicializo cliente de Mastodon
            mastodon = MastodonAPI(
                api_base_url=api_base_url,
                access_token=access_token
            )
            
            # Formateo contenido
            formatted_content = self.format_content(content, title, hashtags)
            
            # Subir imágenes si existen
            media_ids = []
            if images and len(images) > 0:
                for img_path in images:
                    media = mastodon.media_post(img_path)
                    media_ids.append(media['id'])
            
            # Publicar toot
            response = mastodon.status_post(
                status=formatted_content,
                media_ids=media_ids if media_ids else None,
                visibility='public'
            )
            
            return {
                'status': 'success',
                'message': 'Publicado correctamente en Mastodon',
                'post_id': response['id'],
                'url': response['url']
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error al publicar en Mastodon: {str(e)}'
            }