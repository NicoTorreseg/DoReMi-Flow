# main.py
import pygame
import time
import sys
import ctypes
import os # Necesario para buscar archivos

try:
    ctypes.windll.user32.SetProcessDPIAware()
except AttributeError: pass

from config import *
from midi_handler import MidiLoader
from input_handler import KeyboardInput

# --- CLASE NOTA ---
class FallingNote:
    def __init__(self, note_data, speed_factor):
        self.name = note_data['note_name']
        self.val = note_data['midi_val']
        self.is_sharp = note_data['is_sharp']
        self.speed_factor = speed_factor
        self.key_label = MIDI_TO_KEY_LABEL.get(self.val, "?")
        
        relative_pos = self.val - START_NOTE
        self.x = (relative_pos * (SCREEN_WIDTH / TOTAL_KEYS))
        self.y = -50 
        self.color = CYAN if self.is_sharp else GREEN
        self.active = True 

    def update(self):
        self.y += BASE_NOTE_SPEED * self.speed_factor

    def draw(self, surface, font):
        if not self.active: return
        rect = pygame.Rect(self.x, self.y, 40, 20)
        pygame.draw.rect(surface, self.color, rect, border_radius=5)
        
        display_text = f"{self.name} ({self.key_label})"
        text_color = BLACK 
        text = font.render(display_text, True, text_color)
        text_x = self.x + (rect.width // 2) - (text.get_width() // 2)
        surface.blit(text, (text_x, self.y + 2))

# --- FUNCIONES DE SISTEMA ---

def scan_songs():
    """Busca subcarpetas dentro de 'canciones/' que tengan un archivo .mid"""
    available_songs = []
    
    # Si la carpeta no existe, la creamos y avisamos
    if not os.path.exists(SONGS_FOLDER):
        os.makedirs(SONGS_FOLDER)
        print(f"📁 Carpeta '{SONGS_FOLDER}' creada. Coloca tus canciones ahí.")
        return []

    # Escanear carpetas
    for item in os.listdir(SONGS_FOLDER):
        path = os.path.join(SONGS_FOLDER, item)
        if os.path.isdir(path):
            # Verificamos si tiene el MIDI obligatorio
            if "cancion.mid" in os.listdir(path):
                available_songs.append(item)
    
    return available_songs

def select_song_menu(screen, font_title, font_list):
    """Muestra lista de canciones encontradas"""
    songs = scan_songs()
    
    if not songs:
        # Pantalla de error si no hay canciones
        screen.fill(BLACK)
        text = font_list.render(f"No hay canciones en '{SONGS_FOLDER}/'", True, RED)
        screen.blit(text, (50, 300))
        pygame.display.flip()
        time.sleep(3)
        return None

    selected_index = 0
    chosen_song = None
    
    while chosen_song is None:
        screen.fill(BLACK)
        title = font_title.render("Elige una Canción", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        
        # Dibujar lista
        for i, song_name in enumerate(songs):
            color = GREEN if i == selected_index else WHITE
            prefix = "> " if i == selected_index else "  "
            
            text = font_list.render(f"{prefix}{song_name}", True, color)
            screen.blit(text, (100, 150 + (i * 50)))
            
        help_txt = font_list.render("[Flechas] Mover  -  [Enter] Seleccionar", True, GRAY)
        screen.blit(help_txt, (100, SCREEN_HEIGHT - 100))
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = max(0, selected_index - 1)
                elif event.key == pygame.K_DOWN:
                    selected_index = min(len(songs) - 1, selected_index + 1)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    chosen_song = songs[selected_index]

    return chosen_song

def show_difficulty_menu(screen, font_title, font_opt):
    selected_speed = None
    while selected_speed is None:
        screen.fill(BLACK)
        title = font_title.render("Velocidad", True, YELLOW)
        opt1 = font_opt.render("[1] Normal (1.0x)", True, GREEN)
        opt2 = font_opt.render("[2] Fácil   (0.75x)", True, CYAN)
        
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
        screen.blit(opt1, (SCREEN_WIDTH//2 - opt1.get_width()//2, 300))
        screen.blit(opt2, (SCREEN_WIDTH//2 - opt2.get_width()//2, 400))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1: selected_speed = 1.0
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2: selected_speed = 0.75
    return selected_speed

# --- JUEGO PRINCIPAL ---
def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("🎹 PyAno Hero - Song Selector")
    
    font_notes = pygame.font.SysFont("Arial", 11, bold=True) 
    font_keys = pygame.font.SysFont("Arial", 14, bold=True)
    font_score = pygame.font.SysFont("Arial", 30, bold=True)
    font_big = pygame.font.SysFont("Arial", 60, bold=True)
    font_med = pygame.font.SysFont("Arial", 30)

    # 1. SELECCIONAR CANCIÓN
    song_folder_name = select_song_menu(screen, font_big, font_med)
    if not song_folder_name: return # Si cerró o falló

    # 2. SELECCIONAR DIFICULTAD
    current_speed = show_difficulty_menu(screen, font_big, font_med)
    
    # 3. CONSTRUIR RUTAS DE ARCHIVOS
    # Ahora las rutas dependen de la carpeta elegida
    base_path = os.path.join(SONGS_FOLDER, song_folder_name)
    midi_path = os.path.join(base_path, "cancion.mid")
    wav_path = os.path.join(base_path, f"cancion_{current_speed}.wav")
    
    print(f"📂 Cargando desde: {base_path}")

    # 4. CARGA DE DATOS
    loader = MidiLoader(midi_path, speed_factor=current_speed)
    all_notes = loader.parse_midi()
    if not all_notes: return

    try:
        pygame.mixer.music.load(wav_path)
        pygame.mixer.music.set_volume(0.5)
    except pygame.error as e:
        print(f"❌ Error audio: {e}")
        print(f"   Buscaba: {wav_path}")

    # 5. CÁLCULO FÍSICO
    pixels_to_travel = (SCREEN_HEIGHT - PIANO_HEIGHT) - (-50)
    pixels_per_frame = BASE_NOTE_SPEED * current_speed
    time_to_fall = (pixels_to_travel / pixels_per_frame) / 60.0
    print(f"⏱️ Tiempo de caída: {time_to_fall:.2f}s")

    # 6. CUENTA REGRESIVA
    for i in range(3, 0, -1):
        screen.fill(BLACK)
        text = font_big.render(str(i), True, WHITE)
        screen.blit(text, (SCREEN_WIDTH//2 - 20, SCREEN_HEIGHT//2 - 50))
        pygame.display.flip()
        time.sleep(1)

    # 7. INICIO DE JUEGO
    input_handler = KeyboardInput()
    falling_notes = []
    
    score = 0
    combo = 0
    max_combo = 0
    
    music_started = False
    real_start_time = time.time() + time_to_fall
    
    note_index = 0 
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)
        
        current_time = time.time()
        song_time = current_time - real_start_time

        # GESTOR DE AUDIO
        if song_time >= 0 and not music_started:
            try:
                pygame.mixer.music.play()
                music_started = True
            except: pass

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT: running = False
        
        input_handler.process_events(events)
        user_pressed_notes = input_handler.get_pressed_notes()

        # SPAWN
        spawn_threshold = song_time + time_to_fall
        while note_index < len(all_notes) and all_notes[note_index]['spawn_time'] <= spawn_threshold:
            new_note_data = all_notes[note_index]
            if START_NOTE <= new_note_data['midi_val'] <= END_NOTE:
                falling_notes.append(FallingNote(new_note_data, current_speed))
            note_index += 1

        # LOGICA
        hit_line_y = SCREEN_HEIGHT - PIANO_HEIGHT
        for note in falling_notes:
            if note.active:
                if hit_line_y - 20 < note.y < hit_line_y + 30:
                    if note.val in user_pressed_notes:
                        note.active = False
                        combo += 1
                        if combo > max_combo: max_combo = combo
                        score += 10 + (combo * 2)

        # DIBUJAR
        pygame.draw.rect(screen, GRAY, (0, SCREEN_HEIGHT - PIANO_HEIGHT, SCREEN_WIDTH, PIANO_HEIGHT))
        pygame.draw.line(screen, RED, (0, SCREEN_HEIGHT - PIANO_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT - PIANO_HEIGHT), 3)

        for i in range(TOTAL_KEYS):
            x_pos = i * (SCREEN_WIDTH / TOTAL_KEYS)
            midi_note = START_NOTE + i
            is_black_key = '#' in loader.get_note_name(midi_note)
            
            if midi_note in user_pressed_notes: color = YELLOW
            else: color = BLACK if is_black_key else WHITE
            
            key_width = (SCREEN_WIDTH/TOTAL_KEYS) - 2
            key_height = PIANO_HEIGHT if not is_black_key else PIANO_HEIGHT * 0.6
            pygame.draw.rect(screen, color, (x_pos, SCREEN_HEIGHT - PIANO_HEIGHT, key_width, key_height))
            
            key_label = MIDI_TO_KEY_LABEL.get(midi_note, "")
            if key_label: 
                text_col = WHITE if (is_black_key or color == BLACK) else BLACK
                label_surf = font_keys.render(key_label, True, text_col)
                text_x = x_pos + (key_width // 2) - (label_surf.get_width() // 2)
                text_y = SCREEN_HEIGHT - 30 
                screen.blit(label_surf, (text_x, text_y))

        for note in falling_notes[:]: 
            note.update()
            note.draw(screen, font_notes) 
            if note.y > SCREEN_HEIGHT:
                if note.active: combo = 0
                falling_notes.remove(note)

        score_text = font_score.render(f"Puntos: {score}", True, WHITE)
        screen.blit(score_text, (20, 20))
        combo_color = GREEN if combo < 10 else (CYAN if combo < 20 else YELLOW)
        if combo > 1:
            combo_text = font_score.render(f"COMBO x{combo}", True, combo_color)
            screen.blit(combo_text, (20, 60))

        pygame.display.flip()
        clock.tick(60) 

    pygame.quit()

if __name__ == "__main__":
    main()