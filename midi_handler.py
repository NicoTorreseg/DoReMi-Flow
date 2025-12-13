# midi_handler.py
import mido
from config import NOTE_NAMES

class MidiLoader:
    def __init__(self, filename):
        self.filename = filename
        self.notes_to_spawn = [] # Lista de notas procesadas

    def get_note_name(self, midi_number):
        """Traduce 60 -> 'DO', 61 -> 'DO#'"""
        index = midi_number % 12
        return NOTE_NAMES[index]

    def is_sharp(self, midi_number):
        """Devuelve True si es tecla negra (#)"""
        name = self.get_note_name(midi_number)
        return '#' in name

    def parse_midi(self):
        """
        Lee el MIDI y convierte los eventos en una lista simple:
        [{'note': 'DO', 'time': 1.5, 'midi_val': 60}, ...]
        """
        try:
            mid = mido.MidiFile(self.filename)
            print(f"🎵 Cargando: {self.filename}")
        except FileNotFoundError:
            print(f"❌ ERROR: No encontré el archivo {self.filename}")
            return []

        events = []
        current_time = 0

        # Iteramos sobre los mensajes del MIDI
        for msg in mid:
            # Sumamos el tiempo (delta time) para saber el tiempo absoluto en segundos
            current_time += msg.time

            # Solo nos importan las notas que empiezan a sonar (note_on con velocidad > 0)
            if msg.type == 'note_on' and msg.velocity > 0:
                events.append({
                    'note_name': self.get_note_name(msg.note),
                    'midi_val': msg.note,
                    'is_sharp': self.is_sharp(msg.note),
                    'spawn_time': current_time # Momento exacto en que debe aparecer
                })
        
        # Ordenamos por tiempo (por seguridad)
        events.sort(key=lambda x: x['spawn_time'])
        return events