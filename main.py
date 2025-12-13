

# main.py
import pygame
import time
import sys
import ctypes

try:
    ctypes.windll.user32.SetProcessDPIAware()
except AttributeError: pass

from config import *
from midi_handler import MidiLoader
from input_handler import KeyboardInput

class FallingNote:
    def __init__(self, note_data, speed_factor):
        self.name = note_data['note_name']
        self.val = note_data['midi_val']
        self.is_sharp = note_data['is_sharp']
        self.speed_factor = speed_factor
        self.key_label = MIDI_TO_KEY_LABEL.get(self.val, "?")
        
        # Spawn: Aparece arriba del todo (-50px)
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

def show_menu(screen, font_title, font_opt):
    selected_speed = None
    while selected_speed is None:
        screen.fill(BLACK)
        title = font_title.render("PyAno Hero", True, YELLOW)
        subtitle = font_opt.render("Selecciona Dificultad:", True, WHITE)
        opt1 = font_opt.render("[1] Normal (1.0x)", True, GREEN)
        opt2 = font_opt.render("[2] Fácil   (0.75x)", True, CYAN)
        
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
        screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 300))
        screen.blit(opt1, (SCREEN_WIDTH//2 - opt1.get_width()//2, 400))
        screen.blit(opt2, (SCREEN_WIDTH//2 - opt2.get_width()//2, 450))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1: selected_speed = 1.0
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2: selected_speed = 0.75
    return selected_speed

def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("🎹 PyAno Hero - AutoSync")
    
    font_notes = pygame.font.SysFont("Arial", 11, bold=True) 
    font_keys = pygame.font.SysFont("Arial", 14, bold=True)
    font_score = pygame.font.SysFont("Arial", 30, bold=True)
    font_menu_big = pygame.font.SysFont("Arial", 80, bold=True)
    font_menu_opt = pygame.font.SysFont("Arial", 40)

    # 1. MENU
    current_speed = show_menu(screen, font_menu_big, font_menu_opt)
    
    # 2. CARGA DE DATOS
    loader = MidiLoader("cancion.mid", speed_factor=current_speed)
    all_notes = loader.parse_midi()
    if not all_notes: return

    audio_filename = f"cancion_{current_speed}.wav"
    try:
        pygame.mixer.music.load(audio_filename)
        pygame.mixer.music.set_volume(0.5)
    except pygame.error as e:
        print(f"❌ Error audio: {e}")

    # 3. CÁLCULO FÍSICO DE CAÍDA (LA MAGIA MATEMÁTICA) 🧮
    # Calculamos exactamente cuánto tarda una nota en caer desde Y=-50 hasta la línea roja
    pixels_to_travel = (SCREEN_HEIGHT - PIANO_HEIGHT) - (-50) # Distancia total
    pixels_per_frame = BASE_NOTE_SPEED * current_speed
    frames_to_fall = pixels_to_travel / pixels_per_frame
    
    # Convertimos frames a segundos (asumiendo 60 FPS)
    time_to_fall = frames_to_fall / 60.0
    print(f"⏱️ Tiempo de caída calculado: {time_to_fall:.2f} segundos")

    # 4. CUENTA REGRESIVA
    for i in range(3, 0, -1):
        screen.fill(BLACK)
        text = font_menu_big.render(str(i), True, WHITE)
        screen.blit(text, (SCREEN_WIDTH//2 - 20, SCREEN_HEIGHT//2 - 50))
        pygame.display.flip()
        time.sleep(1)

    # 5. INICIO SINCRONIZADO
    input_handler = KeyboardInput()
    falling_notes = []
    
    score = 0
    combo = 0
    max_combo = 0
    
    # IMPORTANTE: No damos Play todavía.
    music_started = False
    
    # Definimos el tiempo de inicio en el FUTURO.
    # El juego "empieza" ahora, pero la música (tiempo 0.0) será en 'time_to_fall' segundos.
    real_start_time = time.time() + time_to_fall
    
    note_index = 0 
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)
        
        # song_time será negativo al principio (mientras caen las primeras notas)
        # y se volverá positivo (0.0) justo cuando la primera nota toque la línea.
        current_time = time.time()
        song_time = current_time - real_start_time

        # --- GESTOR DE AUDIO ---
        # Si el tiempo de la canción llegó a 0.0 y no ha sonado, DALE PLAY
        if song_time >= 0 and not music_started:
            try:
                pygame.mixer.music.play()
                print("🎵 ¡Música Iniciada! Sincronización exacta.")
                music_started = True
            except: pass

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT: running = False
        
        input_handler.process_events(events)
        user_pressed_notes = input_handler.get_pressed_notes()

        # --- SPAWN DE NOTAS (PREDICCIÓN) ---
        # Aquí miramos hacia el futuro. Si la canción va por el segundo -2.0,
        # necesitamos spawnear la nota que en el MIDI está marcada como 0.0
        # Formula: Spawn si (MidiTime <= SongTime + TimeToFall)
        spawn_threshold = song_time + time_to_fall
        
        while note_index < len(all_notes) and all_notes[note_index]['spawn_time'] <= spawn_threshold:
            new_note_data = all_notes[note_index]
            if START_NOTE <= new_note_data['midi_val'] <= END_NOTE:
                falling_notes.append(FallingNote(new_note_data, current_speed))
            note_index += 1

        # --- LOGICA DE JUEGO ---
        hit_line_y = SCREEN_HEIGHT - PIANO_HEIGHT
        
        for note in falling_notes:
            if note.active:
                if hit_line_y - 20 < note.y < hit_line_y + 30:
                    if note.val in user_pressed_notes:
                        note.active = False
                        combo += 1
                        if combo > max_combo: max_combo = combo
                        score += 10 + (combo * 2)

        # --- DIBUJAR ---
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

    print(f"Juego Terminado. Puntaje Final: {score}")
    pygame.quit()

if __name__ == "__main__":
    main()