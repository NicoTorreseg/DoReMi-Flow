# main.py
import pygame
import time
import sys
import ctypes
import os 
import random # Necesario para las partículas

try:
    ctypes.windll.user32.SetProcessDPIAware()
except AttributeError: pass

from config import *
from midi_handler import MidiLoader
from input_handler import KeyboardInput
from mic_handler import MicrophoneHandler 

# --- SISTEMA DE PARTÍCULAS (EFECTOS VISUALES) ---
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.life = 255 # Opacidad inicial
        self.size = random.randint(4, 8)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 10 # Se desvanece rápido
        self.size -= 0.1

    def draw(self, surface):
        if self.life > 0 and self.size > 0:
            s = pygame.Surface((int(self.size), int(self.size)), pygame.SRCALPHA)
            s.fill((*self.color, self.life)) # Color con transparencia
            surface.blit(s, (self.x, self.y))

# --- CLASE NOTA MEJORADA ---
# --- CLASE NOTA (VISUALIZACION CORREGIDA) ---
class FallingNote:
    def __init__(self, note_data, speed_factor):
        self.name = note_data['note_name']
        self.val = note_data['midi_val']
        self.is_sharp = note_data['is_sharp']
        self.speed_factor = speed_factor
        
        # Recuperamos el nombre AMIGABLE (DO, RE...)
        self.key_label = MIDI_TO_KEY_LABEL.get(self.val, "")
        
        relative_pos = self.val - START_NOTE
        self.key_width = (SCREEN_WIDTH / TOTAL_KEYS)
        self.x = (relative_pos * self.key_width) + 2 
        self.width = self.key_width - 4
        self.y = -50 
        
        # Color según si es sostenido (Negra) o natural (Blanca)
        self.color = NOTE_BLACK_COLOR if self.is_sharp else NOTE_WHITE_COLOR
        self.active = True 

    def update(self):
        self.y += BASE_NOTE_SPEED * self.speed_factor

    def draw(self, surface, font):
        if not self.active: return
        
        rect = pygame.Rect(self.x, self.y, self.width, 35) # Un poco más altas para que entre el texto
        
        # 1. Dibujar Rectángulo de Color
        pygame.draw.rect(surface, self.color, rect, border_radius=6)
        
        # 2. Dibujar Borde Blanco
        pygame.draw.rect(surface, WHITE, rect, width=2, border_radius=6)
        
        # 3. DIBUJAR EL TEXTO (DO, RE, MI...)
        if self.key_label:
            # Usamos color NEGRO para el texto para que contraste con los colores neón
            text = font.render(self.key_label, True, BLACK)
            text_x = self.x + (self.width // 2) - (text.get_width() // 2)
            text_y = self.y + (rect.height // 2) - (text.get_height() // 2)
            surface.blit(text, (text_x, text_y))

# --- FUNCIONES AUXILIARES ---
def scan_songs():
    available_songs = []
    if not os.path.exists(SONGS_FOLDER):
        os.makedirs(SONGS_FOLDER)
        return []
    for item in os.listdir(SONGS_FOLDER):
        path = os.path.join(SONGS_FOLDER, item)
        if os.path.isdir(path):
            if "cancion.mid" in os.listdir(path):
                available_songs.append(item)
    return available_songs

# --- PANTALLA TEST (Estilo actualizado) ---
def microphone_test_screen(screen, font_big, font_med, font_keys):
    mic = MicrophoneHandler(min_note=START_NOTE, max_note=END_NOTE)
    mic.start()
    running = True
    clock = pygame.time.Clock()
    
    while running:
        screen.fill(BACKGROUND_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mic.stop(); pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: running = False

        detected_note = mic.get_current_note()
        active_notes = set()
        note_text = "Escuchando..."
        
        if detected_note:
            active_notes.add(detected_note)
            note_name = NOTE_NAMES[detected_note % 12]
            octave = (detected_note // 12) - 1
            note_text = f"🎵 {note_name} {octave} (MIDI: {detected_note})"

        # UI
        pygame.draw.rect(screen, PIANO_BG, (0, SCREEN_HEIGHT - PIANO_HEIGHT, SCREEN_WIDTH, PIANO_HEIGHT))
        
        title = font_big.render("TEST DE MICROFONO", True, NOTE_WHITE_COLOR)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        
        lbl = font_big.render(note_text, True, KEY_ACTIVE_COLOR if detected_note else GRAY)
        screen.blit(lbl, (SCREEN_WIDTH//2 - lbl.get_width()//2, 300))

        # Dibujar Piano (Simplificado para el test)
        for i in range(TOTAL_KEYS):
            x_pos = i * (SCREEN_WIDTH / TOTAL_KEYS)
            midi_note = START_NOTE + i
            note_in_octave = midi_note % 12
            is_black_key = note_in_octave in [1, 3, 6, 8, 10]

            color = BLACK_KEY_COLOR if is_black_key else WHITE_KEY_COLOR
            if midi_note in active_notes: color = KEY_ACTIVE_COLOR
            
            # Chequeo de tolerancia visual
            if midi_note not in active_notes:
                for p in active_notes:
                    if p % 12 == midi_note % 12: color = KEY_TOLERANCE_COLOR

            key_width = (SCREEN_WIDTH/TOTAL_KEYS) - 1
            key_height = PIANO_HEIGHT if not is_black_key else PIANO_HEIGHT * 0.65
            
            pygame.draw.rect(screen, color, (x_pos, SCREEN_HEIGHT - PIANO_HEIGHT, key_width, key_height), border_radius=4)

        pygame.display.flip()
        clock.tick(60)
    mic.stop()

# --- MENUS ---
def main_menu(screen, font_big, font_med):
    while True:
        screen.fill(BACKGROUND_COLOR)
        title = font_big.render("PYANO HERO", True, KEY_ACTIVE_COLOR)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        
        # Efecto de sombra en texto
        opt1_shadow = font_med.render("[1] JUGAR CANCIONES", True, (50, 50, 50))
        opt1 = font_med.render("[1] JUGAR CANCIONES", True, WHITE)
        screen.blit(opt1_shadow, (SCREEN_WIDTH//2 - opt1.get_width()//2 + 2, 302))
        screen.blit(opt1, (SCREEN_WIDTH//2 - opt1.get_width()//2, 300))
        
        opt2 = font_med.render("[2] TEST DE MICROFONO", True, NOTE_WHITE_COLOR)
        screen.blit(opt2, (SCREEN_WIDTH//2 - opt2.get_width()//2, 400))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1: return "GAME"
                if event.key == pygame.K_2 or event.key == pygame.K_KP2: return "TEST"

def select_song_menu(screen, font_title, font_list):
    songs = scan_songs()
    if not songs: return None
    selected_index = 0
    chosen_song = None
    while chosen_song is None:
        screen.fill(BACKGROUND_COLOR)
        title = font_title.render("Elige una Canción", True, KEY_ACTIVE_COLOR)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        for i, song_name in enumerate(songs):
            color = KEY_ACTIVE_COLOR if i == selected_index else GRAY
            prefix = "> " if i == selected_index else "  "
            text = font_list.render(f"{prefix}{song_name}", True, color)
            screen.blit(text, (100, 150 + (i * 50)))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: selected_index = max(0, selected_index - 1)
                elif event.key == pygame.K_DOWN: selected_index = min(len(songs) - 1, selected_index + 1)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER: chosen_song = songs[selected_index]
                elif event.key == pygame.K_ESCAPE: return None
    return chosen_song

def show_difficulty_menu(screen, font_title, font_opt):
    selected_speed = None
    while selected_speed is None:
        screen.fill(BACKGROUND_COLOR)
        title = font_title.render("Velocidad", True, KEY_ACTIVE_COLOR)
        opt1 = font_opt.render("[1] Normal (1.0x)", True, WHITE)
        opt2 = font_opt.render("[2] Fácil   (0.75x)", True, NOTE_WHITE_COLOR)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
        screen.blit(opt1, (SCREEN_WIDTH//2 - opt1.get_width()//2, 300))
        screen.blit(opt2, (SCREEN_WIDTH//2 - opt2.get_width()//2, 400))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1: selected_speed = 1.0
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2: selected_speed = 0.75
                elif event.key == pygame.K_ESCAPE: return None
    return selected_speed

# --- GAME LOOP PRINCIPAL ---
# --- GAME LOOP ---
def run_game(screen, font_notes, font_keys, font_score, font_big):
    font_med = pygame.font.SysFont("Arial", 30)
    song_folder_name = select_song_menu(screen, font_big, font_med)
    if not song_folder_name: return 

    current_speed = show_difficulty_menu(screen, font_big, font_med)
    if not current_speed: return

    base_path = os.path.join(SONGS_FOLDER, song_folder_name)
    midi_path = os.path.join(base_path, "cancion.mid")
    wav_path = os.path.join(base_path, f"cancion_{current_speed}.wav")
    
    loader = MidiLoader(midi_path, speed_factor=current_speed)
    all_notes = loader.parse_midi()
    if not all_notes: return

    try:
        pygame.mixer.music.load(wav_path)
        pygame.mixer.music.set_volume(0.5)
    except: pass

    mic = MicrophoneHandler(min_note=START_NOTE, max_note=END_NOTE)
    mic.start()

    pixels_to_travel = (SCREEN_HEIGHT - PIANO_HEIGHT) - (-50)
    pixels_per_frame = BASE_NOTE_SPEED * current_speed
    time_to_fall = (pixels_to_travel / pixels_per_frame) / 60.0

    for i in range(3, 0, -1):
        screen.fill(BACKGROUND_COLOR)
        text = font_big.render(str(i), True, KEY_ACTIVE_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - 20, SCREEN_HEIGHT//2 - 50))
        pygame.display.flip()
        time.sleep(1)

    input_handler = KeyboardInput()
    falling_notes = []
    particles = []
    score = 0; combo = 0; max_combo = 0
    music_started = False
    real_start_time = time.time() + time_to_fall
    note_index = 0 
    clock = pygame.time.Clock()
    running = True

    # 1. Definimos la línea base del piano
    piano_top_y = SCREEN_HEIGHT - PIANO_HEIGHT
    
    # 2. DEFINIMOS LA COMPENSACIÓN DE LAG
    # 60 píxeles = ~150ms a velocidad normal.
    # Esto expande la zona de acierto hacia ARRIBA.
    LAG_COMPENSATION = 60 

    while running:
        screen.fill(BACKGROUND_COLOR)
        
        # Carriles
        for i in range(TOTAL_KEYS):
            x_pos = i * (SCREEN_WIDTH / TOTAL_KEYS)
            pygame.draw.line(screen, (30, 30, 40), (x_pos, 0), (x_pos, SCREEN_HEIGHT - PIANO_HEIGHT), 1)

        current_time = time.time()
        song_time = current_time - real_start_time

        if song_time >= 0 and not music_started:
            try: pygame.mixer.music.play(); music_started = True
            except: pass

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: running = False

        input_handler.process_events(events)
        
        keyboard_notes = input_handler.get_pressed_notes()
        active_notes = set(keyboard_notes)
        mic_note = mic.get_current_note()
        if mic_note is not None: active_notes.add(mic_note)

        spawn_threshold = song_time + time_to_fall
        while note_index < len(all_notes) and all_notes[note_index]['spawn_time'] <= spawn_threshold:
            new_note_data = all_notes[note_index]
            if START_NOTE <= new_note_data['midi_val'] <= END_NOTE:
                falling_notes.append(FallingNote(new_note_data, current_speed))
            note_index += 1

        # LOGICA ACIERTOS (CON COMPENSACIÓN DE LAG)
        for note in falling_notes:
            if note.active:
                # Modificamos la condición:
                # Si la nota pasa la línea de (piano - 60px), YA SE PUEDE TOCAR.
                # Y sigue siendo válida hasta que sale de la pantalla.
                if note.y > (piano_top_y - LAG_COMPENSATION) and note.y < SCREEN_HEIGHT:
                    
                    hit_confirmed = False
                    if note.val in active_notes: hit_confirmed = True
                    else: 
                        for p in active_notes:
                            if p % 12 == note.val % 12: hit_confirmed = True; break
                    
                    if hit_confirmed:
                        note.active = False
                        combo += 1
                        if combo > max_combo: max_combo = combo
                        score += 10 + (combo * 2)
                        # Partículas visuales
                        for _ in range(10): particles.append(Particle(note.x + note.width//2, note.y, KEY_ACTIVE_COLOR))

        # DIBUJAR PIANO
        pygame.draw.rect(screen, PIANO_BG, (0, SCREEN_HEIGHT - PIANO_HEIGHT, SCREEN_WIDTH, PIANO_HEIGHT))
        pygame.draw.line(screen, HIT_LINE_COLOR, (0, SCREEN_HEIGHT - PIANO_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT - PIANO_HEIGHT), 4)

        for i in range(TOTAL_KEYS):
            x_pos = i * (SCREEN_WIDTH / TOTAL_KEYS)
            midi_note = START_NOTE + i
            note_in_octave = midi_note % 12
            is_black_key = note_in_octave in [1, 3, 6, 8, 10]
            
            is_pressed = False
            if midi_note in active_notes: is_pressed = True
            else:
                 for p in active_notes:
                    if p % 12 == midi_note % 12: is_pressed = True; break

            color = BLACK_KEY_COLOR if is_black_key else WHITE_KEY_COLOR
            if is_pressed: color = KEY_ACTIVE_COLOR
            elif not is_black_key and is_pressed: color = (255, 255, 200)

            key_width = (SCREEN_WIDTH/TOTAL_KEYS) - 1 
            key_height = PIANO_HEIGHT if not is_black_key else PIANO_HEIGHT * 0.65
            
            pygame.draw.rect(screen, color, (x_pos, SCREEN_HEIGHT - PIANO_HEIGHT, key_width, key_height), border_radius=4)
            
            key_label = MIDI_TO_KEY_LABEL.get(midi_note, "")
            if key_label: 
                text_col = WHITE if (is_black_key or color == BLACK_KEY_COLOR) else BLACK
                label_surf = font_keys.render(key_label, True, text_col)
                text_x = x_pos + (key_width // 2) - (label_surf.get_width() // 2)
                text_y = SCREEN_HEIGHT - 30 
                screen.blit(label_surf, (text_x, text_y))

        for note in falling_notes[:]: 
            note.update()
            note.draw(screen, font_notes) 
            if note.y > SCREEN_HEIGHT + 50: 
                if note.active: combo = 0; falling_notes.remove(note)
        
        for p in particles[:]:
            p.update()
            p.draw(screen)
            if p.life <= 0: particles.remove(p)

        score_text = font_score.render(f"Puntos: {score}", True, WHITE)
        screen.blit(score_text, (20, 20))
        if combo > 1:
            combo_text = font_score.render(f"COMBO x{combo} 🔥", True, KEY_ACTIVE_COLOR)
            screen.blit(combo_text, (20, 60))

        pygame.display.flip()
        clock.tick(60) 

    mic.stop()
    pygame.mixer.music.stop()

# --- MAIN ---
def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("🎹 PyAno Hero - VISUAL UPDATE")
    
    font_notes = pygame.font.SysFont("Arial", 10, bold=True) 
    font_keys = pygame.font.SysFont("Arial", 12, bold=True)
    font_score = pygame.font.SysFont("Arial", 30, bold=True)
    font_big = pygame.font.SysFont("Arial", 60, bold=True)
    font_med = pygame.font.SysFont("Arial", 30)

    while True:
        opcion = main_menu(screen, font_big, font_med)
        if opcion == "GAME":
            run_game(screen, font_notes, font_keys, font_score, font_big)
        elif opcion == "TEST":
            microphone_test_screen(screen, font_big, font_med, font_keys)

if __name__ == "__main__":
    main()