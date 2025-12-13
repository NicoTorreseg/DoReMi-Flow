# config.py
import pygame

#mario bros: https://bitmidi.com/mario-bros-super-mario-bros-theme-mid
#https://tuneonmusic.com/music-tools/midi-to-audio/ 
#convertir de mp3 a wav https://convertio.co/es/download/a7c44b1b0ffabf0c161f0e59a2b5bde4afd7f4/
#https://onlinesequencer.net/4782252

#cambiar velocidad https://audioalter.com/change-speed
#https://mp3cut.net/es/change-speed

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
KEY_MAPPING = {
    # === OCTAVA 1 (CENTRAL) ===
    # Ubicación: Fila Superior (QWERTY) + Números
    # Ideal para mano izquierda
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
    # Ubicación: Fila Inferior (ZXCV) + Fila Media (ASDF)
    # Ideal para mano derecha. Sigue la misma lógica visual.
    pygame.K_z: 72, # DO (Antes era la 'I')
    pygame.K_s: 73, # DO# (Tecla negra sobre DO y RE)
    pygame.K_x: 74, # RE
    pygame.K_d: 75, # RE#
    pygame.K_c: 76, # MI
    pygame.K_v: 77, # FA
    pygame.K_g: 78, # FA# (Saltamos la F porque entre Mi y Fa no hay negra)
    pygame.K_b: 79, # SOL
    pygame.K_h: 80, # SOL#
    pygame.K_n: 81, # LA
    pygame.K_j: 82, # LA#
    pygame.K_m: 83, # SI
}

# --- DICCIONARIO VISUAL ---
MIDI_TO_KEY_LABEL = {
    # Octava 1
    60: "Q", 61: "2", 
    62: "W", 63: "3", 
    64: "E", 
    65: "R", 66: "5", 
    67: "T", 68: "6", 
    69: "Y", 70: "7", 
    71: "U",
    
    # Octava 2
    72: "Z", 73: "S", 
    74: "X", 75: "D", 
    76: "C", 
    77: "V", 78: "G", 
    79: "B", 80: "H", 
    81: "N", 82: "J", 
    83: "M"
}