# mic_handler.py
import pyaudio
import numpy as np
import math
import threading
import time
from collections import deque 

class MicrophoneHandler:
    def __init__(self, min_note=0, max_note=127):
        # --- CONFIGURACIÓN ---
        self.CHUNK = 4096       
        self.RATE = 44100       
        self.VOLUME_THRESHOLD = 200 
        
        self.min_note = min_note
        self.max_note = max_note

        # VARIABLES COMPARTIDAS (THREAD-SAFE)
        self.running = False
        self.latest_note = None # Aquí guardaremos la nota detectada
        self.lock = threading.Lock() # Para evitar conflictos de lectura/escritura
        
        # Historial para estabilizar
        self.history = deque(maxlen=2)

        self.p = pyaudio.PyAudio()
        try:
            self.stream = self.p.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=self.RATE,
                                      input=True,
                                      frames_per_buffer=self.CHUNK)
            print(f"🎤 Micrófono LISTO (Modo Hilo Independiente).")
        except Exception as e:
            print(f"❌ Error abriendo micrófono: {e}")
            self.stream = None

    def start(self):
        """Inicia el hilo de escucha en segundo plano"""
        if self.stream and not self.running:
            self.running = True
            # Creamos el hilo que ejecutará la función _listen_loop
            self.thread = threading.Thread(target=self._listen_loop, daemon=True)
            self.thread.start()
            print("🚀 Hilo de audio iniciado.")

    def stop(self):
        """Detiene el hilo y limpia recursos"""
        self.running = False
        if hasattr(self, 'thread'):
            self.thread.join(timeout=1.0)
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()

    def get_current_note(self):
        """
        El juego llama a esto. Retorna INSTANTÁNEAMENTE el último valor calculado.
        Ya no bloquea el juego esperando audio.
        """
        with self.lock:
            return self.latest_note

    def _calculate_hps(self, fft_data, harmonics=2):
        hps = np.copy(fft_data)
        for h in range(2, harmonics + 1):
            decimated = fft_data[::h] 
            hps[:len(decimated)] *= decimated
        return hps

    def _listen_loop(self):
        """
        ESTA FUNCIÓN CORRE EN PARALELO.
        Aquí es donde ocurre la espera de 92ms, pero ya no afecta al juego.
        """
        while self.running:
            try:
                if not self.stream: break

                # 1. Leer Audio (ESTO ES LO QUE BLOQUEABA ANTES)
                try:
                    raw_data = self.stream.read(self.CHUNK, exception_on_overflow=False)
                except IOError: continue

                # 2. Procesamiento Matemático
                data_int = np.frombuffer(raw_data, dtype=np.int16)
                data = data_int.astype(np.float64)
                
                volume = np.sqrt(np.mean(data**2))
                
                detected_note = None

                if volume >= self.VOLUME_THRESHOLD:
                    windowed = data * np.hanning(len(data))
                    fft_data = np.abs(np.fft.rfft(windowed))
                    fft_freq = np.fft.rfftfreq(self.CHUNK, 1.0 / self.RATE)

                    hps_spectrum = self._calculate_hps(fft_data)
                    
                    start_index = int(50 * self.CHUNK / self.RATE) 
                    
                    if start_index < len(hps_spectrum):
                        peak_idx = np.argmax(hps_spectrum[start_index:]) + start_index
                        frequency = fft_freq[peak_idx]

                        if frequency > 0:
                            midi_note = 69 + 12 * math.log2(frequency / 440.0)
                            midi_note = int(round(midi_note))
                            
                            if self.min_note <= midi_note <= self.max_note:
                                self.history.append(midi_note)
                                if len(self.history) == 2 and self.history[0] == self.history[1]:
                                    detected_note = midi_note
                else:
                    self.history.clear()

                # 3. Actualizar la variable compartida
                with self.lock:
                    self.latest_note = detected_note

                # Pequeño descanso para no quemar CPU innecesariamente
                time.sleep(0.001) 

            except Exception as e:
                print(f"Error en hilo de audio: {e}")
                break