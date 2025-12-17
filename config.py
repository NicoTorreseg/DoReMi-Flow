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
# --- CAMBIO 1: PIANO MÁS GRANDE ---
PIANO_HEIGHT = 180 
BASE_NOTE_SPEED = 6 

# --- JUGABILIDAD ---
HIT_WINDOW = 70 

# --- COLORES BÁSICOS ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
GREEN = (0, 255, 0)     
CYAN = (0, 200, 255)    
RED = (255, 0, 0)       
YELLOW = (255, 200, 0)

# --- COLORES ESTILO NEON ---
BACKGROUND_COLOR = (20, 20, 30) 
PIANO_BG = (10, 10, 10)
HIT_LINE_COLOR = (255, 50, 80) 

# Teclas del Piano
WHITE_KEY_COLOR = (240, 240, 240)
BLACK_KEY_COLOR = (40, 40, 50)
KEY_ACTIVE_COLOR = (255, 200, 50) # Dorado al tocar
KEY_TOLERANCE_COLOR = (255, 100, 0) 

# --- CAMBIO 2: COLORES DIFERENCIADOS PARA NOTAS QUE CAEN ---
# Cyan fuerte para naturales, Violeta fuerte para sostenidos
NOTE_WHITE_COLOR = (0, 255, 255)   
NOTE_BLACK_COLOR = (200, 0, 255)   
TEXT_COLOR = (0, 0, 0) # Texto negro para contraste máximo

# --- AUDIO & NOTAS ---
NOTE_NAMES = ["DO", "DO#", "RE", "RE#", "MI", "FA", "FA#", "SOL", "SOL#", "LA", "LA#", "SI"]

START_NOTE = 48 
END_NOTE = 84   
TOTAL_KEYS = END_NOTE - START_NOTE

GLOBAL_OFFSET = 0

# --- ETIQUETAS DE TEXTO (DO, RE, MI...) ---
MIDI_TO_KEY_LABEL = {
    # === OCTAVA BAJA (C3 - MIDI 48-59) === <--- ESTO FALTABA
    48: "DO", 49: "DO#", 50: "RE", 51: "RE#", 52: "MI", 53: "FA", 54: "FA#",
    55: "SOL", 56: "SOL#", 57: "LA", 58: "LA#", 59: "SI",

    # === OCTAVA CENTRAL (C4 - MIDI 60-71) ===
    60: "DO", 61: "DO#", 62: "RE", 63: "RE#", 64: "MI", 65: "FA", 66: "FA#", 
    67: "SOL", 68: "SOL#", 69: "LA", 70: "LA#", 71: "SI",
    
    # === OCTAVA ALTA (C5 - MIDI 72-83) ===
    72: "DO", 73: "DO#", 74: "RE", 75: "RE#", 76: "MI", 77: "FA", 78: "FA#", 
    79: "SOL", 80: "SOL#", 81: "LA", 82: "LA#", 83: "SI"
}

# MAPEO TECLADO PC
KEY_MAPPING = {
    pygame.K_q: 60, pygame.K_2: 61, pygame.K_w: 62, pygame.K_3: 63,
    pygame.K_e: 64, pygame.K_r: 65, pygame.K_5: 66, pygame.K_t: 67,
    pygame.K_6: 68, pygame.K_y: 69, pygame.K_7: 70, pygame.K_u: 71,
    pygame.K_z: 72, pygame.K_s: 73, pygame.K_x: 74, pygame.K_d: 75,
    pygame.K_c: 76, pygame.K_v: 77, pygame.K_g: 78, pygame.K_b: 79,
    pygame.K_h: 80, pygame.K_n: 81, pygame.K_j: 82, pygame.K_m: 83,
}