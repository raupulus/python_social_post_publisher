#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Aplicación Flask para publicar contenido en redes sociales.
"""

import os
import json
from flask import Flask, request, jsonify
from social_networks.mastodon import Mastodon
from social_networks.twitter import Twitter
from social_networks.telegram import Telegram
from social_networks.bluesky import Bluesky
from functions import process_hashtags, process_images, cleanup_images

app = Flask(__name__)

@app.route('/', methods=['GET'])
def health():
    return {'status': 'healthy', 'message': 'Social Post Publisher running'}, 200

@app.route('/publish', methods=['POST'])
def publish():
    """
    Endpoint para publicar contenido en redes sociales.
    Recibe un JSON con los siguientes parámetros:
    - content: (requerido) Contenido a publicar
    - project: (requerido) Nombre del proyecto para cargar el archivo .env correspondiente
    - title: (opcional) Título del contenido
    - hashtags: (opcional) Lista de hashtags sin el símbolo #, estos se añaden
                luego automáticamente por mi aplicación
    - images: (opcional) Lista de imágenes en base64 o URLs. Ideal no más de 4.
    """
    try:
        data = request.json

        # Verifico parámetros requeridos
        if not data.get('content'):
            return jsonify({'success': False, 'error': 'El contenido es requerido'})

        if not data.get('project'):
            return jsonify({'success': False, 'error': 'El proyecto es requerido'})

        # Proceso datos
        content = data.get('content')
        title = data.get('title', '')
        hashtags = process_hashtags(data.get('hashtags', []))
        project = data.get('project')
        images = process_images(data.get('images', []))

        # Cargo configuración del proyecto
        env_file = os.path.join('data', 'profiles', f'{project}.env')
        if not os.path.exists(env_file):
            return jsonify({'success': False, 'error': f'No se encontró el archivo de configuración para el proyecto {project}'})

        # Cargo variables de entorno desde el archivo .env del proyecto
        from dotenv import load_dotenv
        load_dotenv(env_file)

        # Inicializo redes sociales
        networks = []

        # Mastodon
        if os.getenv('MASTODON_ENABLED', 'false').lower() == 'true':
            networks.append(Mastodon())

        # Twitter
        if os.getenv('TWITTER_ENABLED', 'false').lower() == 'true':
            networks.append(Twitter())

        # Telegram
        if os.getenv('TELEGRAM_ENABLED', 'false').lower() == 'true':
            networks.append(Telegram())

        # Bluesky
        if os.getenv('BLUESKY_ENABLED', 'false').lower() == 'true':
            networks.append(Bluesky())

        # Publico en cada red social habilitada
        results = []
        for network in networks:
            try:
                result = network.publish(content=content, title=title, hashtags=hashtags, project=project, images=images)
                results.append({
                    'network': network.__class__.__name__,
                    'success': True,
                    'result': result
                })
            except Exception as e:
                results.append({
                    'network': network.__class__.__name__,
                    'success': False,
                    'error': str(e)
                })

        # Limpio imágenes temporales
        cleanup_images(images)

        # Verifico si al menos una publicación se hizo bien para responder estado
        success = any(result['success'] for result in results)

        return jsonify({
            'success': success,
            'results': results
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
