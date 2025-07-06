"""
Implementación personalizada del módulo imghdr para Python 3.13.

Este módulo proporciona funciones para determinar el tipo de imagen contenida en un archivo o flujo de bytes.
Es una versión simplificada del módulo de la biblioteca estándar que fue eliminado en Python 3.13.
"""

import os
import struct

def what(file, h=None):
    """
    Compruebo el tipo de imagen contenida en un archivo o flujo de bytes.

    Args:
        file: Un nombre de archivo (string), un objeto file, o un objeto bytes.
        h: Opcional; un objeto bytes que contiene los primeros 32 bytes del archivo.
            Si se proporciona, uso esto en lugar de leer el archivo.

    Returns:
        Un string describiendo el tipo de imagen si el archivo contiene un tipo de imagen conocido,
        o None si no lo contiene.
    """
    if h is None:
        if isinstance(file, bytes):
            h = file[:32]
        else:
            if hasattr(file, 'read'):
                h = file.read(32)
                file.seek(0)
            else:
                with open(file, 'rb') as f:
                    h = f.read(32)

    if not h:
        return None

    # JPEG
    if h[0:2] == b'\xff\xd8':
        return 'jpeg'

    # PNG
    if h[:8] == b'\x89PNG\r\n\x1a\n':
        return 'png'

    # GIF
    if h[:6] in (b'GIF87a', b'GIF89a'):
        return 'gif'

    # TIFF
    if h[:2] in (b'MM', b'II'):
        if h[2:4] == b'\x00\x2a':
            return 'tiff'

    # BMP
    if h[:2] == b'BM':
        return 'bmp'

    # WEBP
    if h[:4] == b'RIFF' and h[8:12] == b'WEBP':
        return 'webp'

    return None

# Funciones adicionales que estaban en el módulo imghdr original
def test_jpeg(h):
    """Pruebo datos JPEG."""
    return h[0:2] == b'\xff\xd8'

def test_png(h):
    """Pruebo datos PNG."""
    return h[:8] == b'\x89PNG\r\n\x1a\n'

def test_gif(h):
    """Pruebo datos GIF."""
    return h[:6] in (b'GIF87a', b'GIF89a')

def test_tiff(h):
    """Pruebo datos TIFF."""
    return h[:2] in (b'MM', b'II') and h[2:4] == b'\x00\x2a'

def test_bmp(h):
    """Pruebo datos BMP."""
    return h[:2] == b'BM'

def test_webp(h):
    """Pruebo datos WebP."""
    return h[:4] == b'RIFF' and h[8:12] == b'WEBP'

tests = [
    test_jpeg,
    test_png,
    test_gif,
    test_tiff,
    test_bmp,
    test_webp,
]