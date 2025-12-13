# config.py
import pygame

# Dimensiones
# Dimensiones "HD Ready" (1600x900)
# Esto deja espacio de sobra para la barra de tareas en una pantalla 1080p
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720  

PIANO_HEIGHT = 150  # Hacemos el teclado un poco más alto para que se vea mejor
NOTE_SPEED = 5      # Al ser la pantalla más alta, aumentamos un poco la velocidad

# Colores (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
GREEN = (0, 255, 0)     # Notas naturales (teclas blancas)
CYAN = (0, 200, 255)    # Notas sostenidas (teclas negras)
RED = (255, 0, 0)       # Línea de "hit"
YELLOW = (255, 200, 0)  # Color para cuando la nota "golpea"
# Notas en español
NOTE_NAMES = ["DO", "DO#", "RE", "RE#", "MI", "FA", "FA#", "SOL", "SOL#", "LA", "LA#", "SI"]

# Mapeo básico de teclado (Octavas centrales)
# Un piano completo tiene 88 teclas. Aquí mostraremos unas 4 octavas (aprox 48 teclas)
START_NOTE = 36 # C2 (Do en la segunda octava)
END_NOTE = 84   # C6
TOTAL_KEYS = END_NOTE - START_NOTE
KEY_WIDTH = SCREEN_WIDTH // (TOTAL_KEYS // 12 * 7) # Calculo aprox para teclas blancas