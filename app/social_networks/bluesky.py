#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Implementación de la clase para publicar en Bluesky.
"""

import os
import json
import requests
from . import SocialNetwork

class Bluesky(SocialNetwork):
    """
    Clase para publicar contenido en Bluesky.
    """
    
    def __init__(self):
        """
        Inicializo la conexión con Bluesky.
        """
        super().__init__()
        self.api_url = "https://bsky.social/xrpc"
    
    def publish(self, content, title=None, hashtags=None, project=None, images=None):
        """
        Publica contenido en Bluesky.
        
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
        
        # Verificar si Bluesky está habilitado
        if os.getenv('BLUESKY_ENABLED', 'false').lower() != 'true':
            return {'status': 'skipped', 'message': 'Bluesky no está habilitado para este proyecto'}
        
        # Obtener credenciales
        identifier = os.getenv('BLUESKY_IDENTIFIER')  # Correo o handle
        password = os.getenv('BLUESKY_PASSWORD')  # Contraseña de la app
        
        if not identifier or not password:
            return {'status': 'error', 'message': 'Faltan credenciales para Bluesky'}
        
        try:
            # Autenticar con Bluesky
            session = self._create_session(identifier, password)
            if not session:
                return {'status': 'error', 'message': 'Error de autenticación en Bluesky'}
            
            # Formatear contenido
            formatted_content = self.format_content(content, title, hashtags)
            
            # Subir imágenes si existen
            image_refs = []
            if images and len(images) > 0:
                for img_path in images[:4]:  # Máximo 4 imágenes
                    blob_ref = self._upload_image(img_path, session)
                    if blob_ref:
                        image_refs.append(blob_ref)
            
            # Crear post
            post_data = {
                "repo": session["did"],
                "collection": "app.bsky.feed.post",
                "record": {
                    "$type": "app.bsky.feed.post",
                    "text": formatted_content,
                    "createdAt": self._get_iso_timestamp()
                }
            }
            
            # Añado imágenes si existen
            if image_refs:
                post_data["record"]["embed"] = {
                    "$type": "app.bsky.embed.images",
                    "images": image_refs
                }
            
            # Publico post
            response = requests.post(
                f"{self.api_url}/com.atproto.repo.createRecord",
                json=post_data,
                headers={"Authorization": f"Bearer {session['accessJwt']}"}
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'status': 'success',
                    'message': 'Publicado correctamente en Bluesky',
                    'post_id': result.get('uri', ''),
                    'url': f"https://bsky.app/profile/{session['handle']}/post/{result.get('uri', '').split('/')[-1]}"
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Error al publicar en Bluesky: {response.text}'
                }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error al publicar en Bluesky: {str(e)}'
            }
    
    def _create_session(self, identifier, password):
        """
        Crea una sesión en Bluesky.
        
        Args:
            identifier (str): Correo o handle
            password (str): Contraseña de la app
            
        Returns:
            dict: Datos de la sesión
        """
        try:
            response = requests.post(
                f"{self.api_url}/com.atproto.server.createSession",
                json={"identifier": identifier, "password": password}
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception:
            return None
    
    def _upload_image(self, img_path, session):
        """
        Sube una imagen a Bluesky.
        
        Args:
            img_path (str): Ruta de la imagen
            session (dict): Datos de la sesión
            
        Returns:
            dict: Referencia a la imagen
        """
        try:
            # Determinar el tipo MIME
            mime_type = "image/jpeg"  # Por defecto
            if img_path.lower().endswith(".png"):
                mime_type = "image/png"
            elif img_path.lower().endswith(".gif"):
                mime_type = "image/gif"
            
            # Leo la imagen
            with open(img_path, "rb") as f:
                img_data = f.read()
            
            # Subo la imagen
            response = requests.post(
                f"{self.api_url}/com.atproto.repo.uploadBlob",
                data=img_data,
                headers={
                    "Content-Type": mime_type,
                    "Authorization": f"Bearer {session['accessJwt']}"
                }
            )
            
            if response.status_code == 200:
                blob = response.json().get("blob")
                return {
                    "alt": "Imagen adjunta",
                    "image": blob
                }
            return None
        except Exception as e:
            print(f"Error al subir imagen a Bluesky: {str(e)}")
            return None
    
    def _get_iso_timestamp(self):
        """
        Obtiene la fecha y hora actual en formato ISO.
        
        Returns:
            str: Fecha y hora en formato ISO
        """
        from datetime import datetime
        return datetime.utcnow().isoformat().replace('+00:00', 'Z')