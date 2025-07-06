#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Funciones auxiliares para el procesamiento de datos.
"""

import os
import base64
import uuid
from PIL import Image
from io import BytesIO
import requests
import shutil

# Directorio temporal para almacenar imágenes (data/temp)
TEMP_DIR = os.path.join('data', 'temp')

def process_hashtags(hashtags):
    """
    Proceso una lista de hashtags añadiendo el símbolo # al principio si no
    lo tienen.
    
    Args:
        hashtags (list): Lista de hashtags sin el símbolo #
        
    Returns:
        list: Lista de hashtags con el símbolo # al principio
    """
    if not hashtags:
        return []
    
    processed_hashtags = []
    for tag in hashtags:
        # Elimino espacios y caracteres especiales (intento slufy)
        tag = tag.strip().replace(' ', '')
        
        # Añado # si no lo tiene al comienzo de la palabra
        if not tag.startswith('#'):
            tag = f'#{tag}'
            
        processed_hashtags.append(tag)
    
    return processed_hashtags

def process_images(images):
    """
    Proceso una lista de imágenes, limitando a 4 como máximo.
    Puede recibir URLs o imágenes en base64.
    
    Args:
        images (list): Lista de imágenes (URLs o base64)
        
    Returns:
        list: Lista de rutas a las imágenes procesadas
    """
    if not images:
        return []
    
    # Creo el directorio temporal si no existe en "data/temp"
    os.makedirs(TEMP_DIR, exist_ok=True)
    
    # Limito a 4 imágenes (estándar para redes, descarto las demás)
    images = images[:4]
    
    processed_images = []
    for img in images:
        try:
            img_path = None
            
            # Compruebo si es una URL
            if img.startswith(('http://', 'https://')):
                img_path = download_image(img)
            # Compruebo si es base64
            elif img.startswith(('data:image', 'base64:')):
                img_path = save_base64_image(img)
            
            if img_path:
                # Optimizo imagen para redes sociales
                optimized_path = optimize_image(img_path)
                processed_images.append(optimized_path)
                
                # Elimino imagen original si es diferente de la optimizada
                if optimized_path != img_path:
                    os.remove(img_path)
        except Exception as e:
            print(f"Error procesando imagen: {str(e)}")
    
    return processed_images

def download_image(url):
    """
    Descarga una imagen desde una URL.
    
    Args:
        url (str): URL de la imagen
        
    Returns:
        str: Ruta local de la imagen descargada
    """
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        # Genero nombre único para la imagen
        file_ext = os.path.splitext(url.split('/')[-1])[-1]
        if not file_ext:
            file_ext = '.jpg'  # Extensión por defecto... a ver si esto no falla XD
        
        filename = f"{uuid.uuid4()}{file_ext}"
        filepath = os.path.join(TEMP_DIR, filename)
        
        # Guardo imagen
        with open(filepath, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)
            
        return filepath
    else:
        raise Exception(f"No se pudo descargar la imagen: {response.status_code}")

def save_base64_image(base64_str):
    """
    Guarda una imagen en base64.
    
    Args:
        base64_str (str): Imagen en formato base64
        
    Returns:
        str: Ruta local de la imagen guardada
    """
    # Extraigo datos de base64
    if 'base64,' in base64_str:
        base64_str = base64_str.split('base64,')[1]
    
    # Decodifico base64
    img_data = base64.b64decode(base64_str)
    
    # Determino formato de imagen
    img = Image.open(BytesIO(img_data))
    img_format = img.format.lower() if img.format else 'jpeg'
    
    # Genero nombre único para la imagen
    filename = f"{uuid.uuid4()}.{img_format}"
    filepath = os.path.join(TEMP_DIR, filename)
    
    # Guardo imagen
    img.save(filepath)
    
    return filepath

def optimize_image(img_path):
    """
    Optimizo una imagen para redes sociales.
    
    Args:
        img_path (str): Ruta de la imagen a optimizar
        
    Returns:
        str: Ruta de la imagen optimizada
    """
    try:
        img = Image.open(img_path)
        
        # Redimensiono si es demasiado grande
        max_size = 1280  # Tamaño máximo para la mayoría de redes sociales, debería bastar en calidad (espero...)
        if img.width > max_size or img.height > max_size:
            img.thumbnail((max_size, max_size), Image.LANCZOS)
        
        # Convierto a RGB si es necesario (para PNG con transparencia)
        if img.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])  # 3 es el canal alfa
            img = background
        
        # Genero nombre para la imagen optimizada
        filename = os.path.basename(img_path)
        optimized_path = os.path.join(TEMP_DIR, f"opt_{filename}")
        
        # Guardo imagen optimizada
        img.save(optimized_path, quality=85, optimize=True)
        
        return optimized_path
    except Exception as e:
        print(f"Error optimizando imagen: {str(e)}")
        return img_path  # Devuelvo la ruta original si hay error

def cleanup_images(image_paths):
    """
    Elimina las imágenes temporales.
    
    Args:
        image_paths (list): Lista de rutas de imágenes a eliminar
    """
    for path in image_paths:
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception as e:
            print(f"Error eliminando imagen {path}: {str(e)}")