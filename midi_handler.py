# midi_handler.py
import mido
from config import NOTE_NAMES

class MidiLoader:
    def __init__(self, filename, speed_factor=1.0):
        self.filename = filename
        self.speed_factor = speed_factor 

    def get_note_name(self, midi_number):
        index = midi_number % 12
        return NOTE_NAMES[index]

    def is_sharp(self, midi_number):
        name = self.get_note_name(midi_number)
        return '#' in name

    def parse_midi(self):
        """
        Lee el MIDI y ajusta los tiempos de aparición según la velocidad.
        Fórmula: Nuevo Tiempo = Tiempo Original / Factor de Velocidad
        """
        try:
            mid = mido.MidiFile(self.filename)
            print(f"🎵 Procesando MIDI para velocidad: {self.speed_factor}x")
        except FileNotFoundError:
            print(f"❌ ERROR: No encontré el archivo {self.filename}")
            return []

        events = []
        current_time = 0

        for msg in mid:
            # Sumamos el tiempo delta del mensaje
            current_time += msg.time

            if msg.type == 'note_on' and msg.velocity > 0:
                # AJUSTE DE TIEMPO:
                # Si va lento (0.75), el tiempo se alarga (dividir por < 1 agranda el número)
                real_spawn_time = current_time / self.speed_factor 

                events.append({
                    'note_name': self.get_note_name(msg.note),
                    'midi_val': msg.note,
                    'is_sharp': self.is_sharp(msg.note),
                    'spawn_time': real_spawn_time 
                })
        
        # Ordenamos cronológicamente
        events.sort(key=lambda x: x['spawn_time'])
        return events