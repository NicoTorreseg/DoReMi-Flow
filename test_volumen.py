# test_volumen.py
import pyaudio
import numpy as np
import time

def medidor_de_volumen():
    CHUNK = 2048
    RATE = 44100
    
    p = pyaudio.PyAudio()
    
    # Intentamos abrir el micrófono por defecto
    try:
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
    except Exception as e:
        print(f"❌ Error abriendo mic: {e}")
        return

    print("📊 MIDE TU VOLUMEN")
    print("---------------------------------")
    print("1. Quédate en SILENCIO (mira los números).")
    print("2. Toca el PIANO (mira los números).")
    print("---------------------------------")
    time.sleep(2)

    try:
        while True:
            # Leer datos
            raw_data = stream.read(CHUNK, exception_on_overflow=False)
            
            # Convertir a números manejables
            data_int = np.frombuffer(raw_data, dtype=np.int16)
            data = data_int.astype(np.float64)
            
            # Calcular volumen
            volumen = np.sqrt(np.mean(data**2))
            volumen = int(volumen)
            
            # Barra visual
            barra = "|" * (volumen // 100) # Una rayita cada 100 de volumen
            if len(barra) > 50: barra = barra[:50] + "..."
            
            print(f"Volumen: {volumen:4d} {barra}")
            
    except KeyboardInterrupt:
        print("\n🛑 Fin del test.")
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    medidor_de_volumen()