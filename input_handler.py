# input_handler.py
import pygame
from config import KEY_MAPPING

class KeyboardInput:
    def __init__(self):
        self.pressed_notes = set()

    def process_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in KEY_MAPPING:
                    midi_val = KEY_MAPPING[event.key]
                    self.pressed_notes.add(midi_val)
            
            elif event.type == pygame.KEYUP:
                if event.key in KEY_MAPPING:
                    midi_val = KEY_MAPPING[event.key]
                    self.pressed_notes.discard(midi_val)

    def get_pressed_notes(self):
        return self.pressed_notes