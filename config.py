# config.py
import pygame

# --- PANTALLA ---
# Dimensiones "HD Ready" (1280x720)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720  

PIANO_HEIGHT = 150
BASE_NOTE_SPEED = 5  # Velocidad base

# --- COLORES (RGB) ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
GREEN = (0, 255, 0)     
CYAN = (0, 200, 255)    
RED = (255, 0, 0)       
YELLOW = (255, 200, 0)  
BLUE = (50, 50, 255) 

# --- AUDIO & NOTAS ---
NOTE_NAMES = ["DO", "DO#", "RE", "RE#", "MI", "FA", "FA#", "SOL", "SOL#", "LA", "LA#", "SI"]

# Rango del teclado (4 Octavas)
START_NOTE = 36 # C2 
END_NOTE = 84   # C6
TOTAL_KEYS = END_NOTE - START_NOTE

# AJUSTE DE SINCRONIZACIÓN (Segundos)
# Cambia esto si sientes que las notas no caen a tiempo con la música
GLOBAL_OFFSET = 0

# --- MAPEO DE TECLAS (Configuración de Usuario) ---
# Aquí definimos qué tecla física de tu PC activa qué nota MIDI.
KEY_MAPPING = {
    # === OCTAVA CENTRAL (Donde ocurre la mayoría de la melodía) ===
    # Teclas Blancas (Fila QWERTY)
    pygame.K_q: 60, # La tecla 'Q' es el DO  (Central)
    pygame.K_w: 62, # La tecla 'W' es el RE
    pygame.K_e: 64, # La tecla 'E' es el MI
    pygame.K_r: 65, # La tecla 'R' es el FA
    pygame.K_t: 67, # La tecla 'T' es el SOL
    pygame.K_y: 69, # La tecla 'Y' es el LA
    pygame.K_u: 71, # La tecla 'U' es el SI

    # Teclas Negras (Fila de Números)
    pygame.K_2: 61, # El '2' es DO Sostenido (DO#)
    pygame.K_3: 63, # El '3' es RE Sostenido (RE#)
    pygame.K_5: 66, # El '5' es FA Sostenido (FA#)
    pygame.K_6: 68, # El '6' es SOL Sostenido (SOL#)
    pygame.K_7: 70, # El '7' es LA Sostenido (LA#)
    
    # === OCTAVA AGUDA (Notas más altas) ===
    # Sigue en la misma fila a la derecha
    pygame.K_i: 72, # La tecla 'I' es el DO (Agudo)
    pygame.K_o: 74, # La tecla 'O' es el RE (Agudo)
    pygame.K_p: 76, # La tecla 'P' es el MI (Agudo)
    
    # Teclas Negras Agudas
    pygame.K_9: 73, # El '9' es DO# (Agudo)
    pygame.K_0: 75  # El '0' es RE# (Agudo)
}

# --- DICCIONARIO VISUAL ---
# Esto sirve para que el juego sepa qué letra pintar en pantalla según la nota MIDI
MIDI_TO_KEY_LABEL = {
    60: "Q", 61: "2", 
    62: "W", 63: "3", 
    64: "E", 
    65: "R", 66: "5", 
    67: "T", 68: "6", 
    69: "Y", 70: "7", 
    71: "U",
    
    72: "I", 73: "9", 
    74: "O", 75: "0", 
    76: "P"
}