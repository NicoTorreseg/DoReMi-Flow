# main.py
import pygame
import time
from config import *
from midi_handler import MidiLoader

# --- CLASE PARA LA NOTA QUE CAE ---
class FallingNote:
    def __init__(self, note_data, screen_height):
        self.name = note_data['note_name']
        self.val = note_data['midi_val']
        self.is_sharp = note_data['is_sharp']
        
        # Calcular posición X basada en el teclado
        # (Lógica simplificada para posicionar sobre teclas blancas/negras)
        # Nota: Ajustar esto perfectamente requiere matemáticas de piano,
        # aquí usamos una aproximación lineal para el MVP.
        relative_pos = self.val - START_NOTE
        self.x = (relative_pos * (SCREEN_WIDTH / TOTAL_KEYS))
        
        self.y = -50 # Empieza arriba fuera de pantalla
        self.color = CYAN if self.is_sharp else GREEN
        self.active = True

    def update(self):
        self.y += NOTE_SPEED

    def draw(self, surface, font):
        # Dibujamos el rectángulo
        rect = pygame.Rect(self.x, self.y, 30, 20)
        pygame.draw.rect(surface, self.color, rect, border_radius=5)
        
        # Dibujamos el texto (DO, RE, MI)
        text = font.render(self.name, True, BLACK)
        surface.blit(text, (self.x + 2, self.y + 2))

# --- INICIO DEL JUEGO ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("🎹 PianoHero - Nico's Project")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 12, bold=True)

    # 1. CARGAR CANCIÓN (Necesitas un archivo 'cancion.mid' en la carpeta)
    # Si no tienes uno, descarga uno simple de internet (ej: Twinkle Twinkle Little Star)
    loader = MidiLoader("cancion.mid") 
    all_notes = loader.parse_midi()
    
    # Si no hay notas, salimos
    if not all_notes:
        print("⚠️ No se cargaron notas. Asegúrate de tener 'cancion.mid'")
        return

    falling_notes = []
    start_time = time.time()
    note_index = 0 # Puntero para saber qué nota toca generar

    running = True
    while running:
        screen.fill(BLACK)
        elapsed_time = time.time() - start_time

        # --- EVENTOS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- GENERADOR DE NOTAS ---
        # Si todavía hay notas en la lista y el tiempo coincide...
        while note_index < len(all_notes) and all_notes[note_index]['spawn_time'] <= elapsed_time:
            new_note_data = all_notes[note_index]
            # Filtramos para que solo caigan notas dentro de nuestras 4 octavas visibles
            if START_NOTE <= new_note_data['midi_val'] <= END_NOTE:
                falling_notes.append(FallingNote(new_note_data, SCREEN_HEIGHT))
            note_index += 1

        # --- DIBUJAR TECLADO ESTÁTICO (Fondo) ---
        # --- DETECTAR GOLPES (HIT DETECTION) ---
        # Creamos una lista con los números MIDI que están tocando la línea roja AHORA
        keys_being_hit = []
        for note in falling_notes:
            # Si la nota está cruzando la línea del piano (con un margen de error de 20px)
            hit_line_y = SCREEN_HEIGHT - PIANO_HEIGHT
            if hit_line_y - 10 < note.y < hit_line_y + 20:
                keys_being_hit.append(note.val)

        # --- DIBUJAR TECLADO ---
        pygame.draw.rect(screen, GRAY, (0, SCREEN_HEIGHT - PIANO_HEIGHT, SCREEN_WIDTH, PIANO_HEIGHT))
        pygame.draw.line(screen, RED, (0, SCREEN_HEIGHT - PIANO_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT - PIANO_HEIGHT), 3)

        for i in range(TOTAL_KEYS):
            x_pos = i * (SCREEN_WIDTH / TOTAL_KEYS)
            midi_note = START_NOTE + i
            
            # Lógica de colores
            is_black_key = '#' in loader.get_note_name(midi_note)
            
            # COLOREADO DINÁMICO: Si la nota está cayendo, PINTARLA
            if midi_note in keys_being_hit:
                color = YELLOW
            else:
                color = BLACK if is_black_key else WHITE
            
            # Dibujamos la tecla
            key_height = PIANO_HEIGHT if not is_black_key else PIANO_HEIGHT * 0.6
            pygame.draw.rect(screen, color, (x_pos, SCREEN_HEIGHT - PIANO_HEIGHT, (SCREEN_WIDTH/TOTAL_KEYS)-2, key_height))
            
            # Etiqueta en el teclado (Solo en blancas para no saturar)
            if not is_black_key: 
                lbl = font.render(loader.get_note_name(midi_note), True, BLACK)
                screen.blit(lbl, (x_pos, SCREEN_HEIGHT - 20))
        # --- ACTUALIZAR Y DIBUJAR NOTAS QUE CAEN ---
        for note in falling_notes[:]: # Iteramos sobre copia para poder borrar
            note.update()
            note.draw(screen, font)
            
            # Eliminar si sale de pantalla
            if note.y > SCREEN_HEIGHT:
                falling_notes.remove(note)

        pygame.display.flip()
        clock.tick(60) # 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()