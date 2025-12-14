# test_mic.py
import time
from mic_handler import MicrophoneHandler
from config import NOTE_NAMES

def probar_microfono():
    print("🎤 Iniciando prueba de micrófono...")
    print("🎹 Toca una tecla en tu piano (Una a la vez)...")
    print("---------------------------------------------")

    mic = MicrophoneHandler()
    
    # Bucle de prueba
    try:
        while True:
            midi_val = mic.get_current_note()
            
            if midi_val:
                # Traducir número a nombre (ej: 60 -> DO)
                note_name = NOTE_NAMES[midi_val % 12]
                octave = (midi_val // 12) - 1
                
                print(f"🔊 Detectado: {note_name}{octave} (MIDI: {midi_val})")
            
            # Pequeña pausa para no saturar la consola
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\n🛑 Prueba terminada.")
        mic.close()

if __name__ == "__main__":
    probar_microfono()