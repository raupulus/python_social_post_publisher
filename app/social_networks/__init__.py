#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Inicializador del paquete de redes sociales.
"""

from abc import ABC, abstractmethod
import os
from dotenv import load_dotenv

class SocialNetwork(ABC):
    """
    Clase base abstracta para todas las redes sociales.
    Define la interfaz común que deben implementar todas las redes sociales.
    Así simplifico el sistema para publicar en cada red social.
    """
    
    def __init__(self):
        """
        Inicializo la red social.
        """
        self.name = self.__class__.__name__
    
    def load_config(self, project):
        """
        Cargo la configuración de la red social desde el archivo .env del
        proyecto.
        
        Args:
            project (str): Nombre del proyecto (Debe corresponder con el nombre del archivo .env)
        """
        env_file = os.path.join('data', 'profiles', f'{project}.env')
        load_dotenv(env_file)
    
    @abstractmethod
    def publish(self, content, title=None, hashtags=None, project=None, images=None):
        """
        Publica contenido en la red social.
        
        Args:
            content (str): Contenido a publicar
            project (str): Nombre del proyecto (Debe corresponder con el nombre del archivo .env)
            title (str, optional): Título del contenido
            hashtags (list, optional): Lista de hashtags
            images (list, optional): Lista de rutas a imágenes
            
        Returns:
            dict: Resultado de la publicación
        """
        pass
    
    def format_content(self, content, title=None, hashtags=None):
        """
        Formatea el contenido para la publicación.
        
        Args:
            content (str): Contenido a publicar
            title (str, optional): Título del contenido
            hashtags (list, optional): Lista de hashtags
            
        Returns:
            str: Contenido formateado
        """
        formatted_content = content
        
        # Añado título si existe
        if title:
            formatted_content = f"{title}\n\n{formatted_content}"
        
        # Añado hashtags si existen (convierto "tag" en "#tag" de lo recibido)
        if hashtags and len(hashtags) > 0:
            hashtags_text = ' '.join(hashtags)
            formatted_content = f"{formatted_content}\n\n{hashtags_text}"
        
        return formatted_content