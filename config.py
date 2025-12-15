# config.py
import pygame

#mario bros: https://bitmidi.com/mario-bros-super-mario-bros-theme-mid
#https://tuneonmusic.com/music-tools/midi-to-audio/ 
#convertir de mp3 a wav https://convertio.co/es/download/a7c44b1b0ffabf0c161f0e59a2b5bde4afd7f4/
#https://onlinesequencer.net/4782252

#cambiar velocidad https://audioalter.com/tempo
#https://mp3cut.net/es/change-speed

#paso 1: https://bitmidi.com/beethoven-symphony9-4-ode-to-joy-piano-solo-mid descargar el midi
#paso 2: convertir el midi a mp3 https://tuneonmusic.com/music-tools/midi-to-audio/ 
#paso 3: convertir el mp3 a wav  https://convertio.co/es/download/ed86181f922e1a2f81bb55de48e0474ffbf917/ 
#paso 4: cambiar la velocidad del wav a 0.75  https://audioalter.com/tempo

SONGS_FOLDER = "canciones"

# --- PANTALLA ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720  

PIANO_HEIGHT = 150
BASE_NOTE_SPEED = 5 

# --- COLORES ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
GREEN = (0, 255, 0)     
CYAN = (0, 200, 255)    
RED = (255, 0, 0)       
YELLOW = (255, 200, 0)  

# --- AUDIO & NOTAS ---
NOTE_NAMES = ["DO", "DO#", "RE", "RE#", "MI", "FA", "FA#", "SOL", "SOL#", "LA", "LA#", "SI"]

# Rango: 2 Octavas exactas (12 + 12 = 24 notas)
# Empieza en DO Central (60) y termina justo al final de la segunda octava
START_NOTE = 48 
END_NOTE = 84   
TOTAL_KEYS = END_NOTE - START_NOTE

GLOBAL_OFFSET = 0

# --- MAPEO DE TECLAS (DOBLE PISO) ---
# Esto se mantiene igual para que puedas seguir usando el teclado de PC si quieres
KEY_MAPPING = {
    # === OCTAVA 1 (CENTRAL) ===
    pygame.K_q: 60, # DO
    pygame.K_2: 61, # DO#
    pygame.K_w: 62, # RE
    pygame.K_3: 63, # RE#
    pygame.K_e: 64, # MI
    pygame.K_r: 65, # FA
    pygame.K_5: 66, # FA#
    pygame.K_t: 67, # SOL
    pygame.K_6: 68, # SOL#
    pygame.K_y: 69, # LA
    pygame.K_7: 70, # LA#
    pygame.K_u: 71, # SI

    # === OCTAVA 2 (AGUDA) ===
    pygame.K_z: 72, # DO
    pygame.K_s: 73, # DO#
    pygame.K_x: 74, # RE
    pygame.K_d: 75, # RE#
    pygame.K_c: 76, # MI
    pygame.K_v: 77, # FA
    pygame.K_g: 78, # FA#
    pygame.K_b: 79, # SOL
    pygame.K_h: 80, # SOL#
    pygame.K_n: 81, # LA
    pygame.K_j: 82, # LA#
    pygame.K_m: 83, # SI
}

# --- DICCIONARIO VISUAL (ESTETICA MUSICAL) ---
# Aquí cambiamos las letras Q, W, E... por DO, RE, MI...
MIDI_TO_KEY_LABEL = {
    # Octava 1 (Antes QWERTY)
    60: "DO", 61: "DO#", 
    62: "RE", 63: "RE#", 
    64: "MI", 
    65: "FA", 66: "FA#", 
    67: "SOL", 68: "SOL#", 
    69: "LA", 70: "LA#", 
    71: "SI",
    
    # Octava 2 (Antes ZXCV)
    72: "DO", 73: "DO#", 
    74: "RE", 75: "RE#", 
    76: "MI", 
    77: "FA", 78: "FA#", 
    79: "SOL", 80: "SOL#", 
    81: "LA", 82: "LA#", 
    83: "SI"
}