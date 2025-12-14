# mic_handler.py
import pyaudio
import numpy as np
import math
from collections import deque 

class MicrophoneHandler:
    def __init__(self, min_note=0, max_note=127):
        # --- CALIBRACIÓN DE AUDIO ---
        self.CHUNK = 2048       
        self.RATE = 44100       
        
        # UMBRAL DE RUIDO (CALIBRADO CON TUS DATOS)
        # Tu silencio es ~30. Tu piano es ~1000.
        # 200 es el punto dulce: ignora el aire, capta el piano.
        self.VOLUME_THRESHOLD = 200 
        
        self.min_note = min_note
        self.max_note = max_note

        # Memoria a corto plazo (Estabilizador)
        # Necesitamos 2 detecciones seguidas para confirmar la nota
        self.history = deque(maxlen=2)

        self.p = pyaudio.PyAudio()
        try:
            self.stream = self.p.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=self.RATE,
                                      input=True,
                                      frames_per_buffer=self.CHUNK)
            print(f"🎤 Micrófono LISTO. Umbral: {self.VOLUME_THRESHOLD}")
        except Exception as e:
            print(f"❌ Error abriendo micrófono: {e}")
            self.stream = None

    def _calculate_hps(self, fft_data, harmonics=2):
        """Algoritmo HPS para eliminar notas fantasma"""
        hps = np.copy(fft_data)
        for h in range(2, harmonics + 1):
            decimated = fft_data[::h] 
            hps[:len(decimated)] *= decimated
        return hps

    def get_current_note(self):
        if not self.stream: return None

        try:
            try:
                raw_data = self.stream.read(self.CHUNK, exception_on_overflow=False)
            except IOError: return None

            # 1. Convertir a float64 para evitar errores matemáticos
            data_int = np.frombuffer(raw_data, dtype=np.int16)
            data = data_int.astype(np.float64)
            
            # 2. CALCULAR VOLUMEN (RMS)
            volume = np.sqrt(np.mean(data**2))
            
            # Si el volumen es bajo, limpiamos la memoria y salimos
            if volume < self.VOLUME_THRESHOLD:
                self.history.clear() 
                return None

            # 3. ANÁLISIS DE FRECUENCIA (FFT)
            windowed = data * np.hanning(len(data))
            fft_data = np.abs(np.fft.rfft(windowed))
            fft_freq = np.fft.rfftfreq(self.CHUNK, 1.0 / self.RATE)

            # 4. HPS (Limpieza de señal)
            hps_spectrum = self._calculate_hps(fft_data)
            
            # Ignorar frecuencias graves (< 60Hz)
            start_index = int(60 * self.CHUNK / self.RATE) 
            if start_index >= len(hps_spectrum): return None
            
            peak_idx = np.argmax(hps_spectrum[start_index:]) + start_index
            frequency = fft_freq[peak_idx]

            # 5. CONVERSIÓN A MIDI
            if frequency > 0:
                midi_note = 69 + 12 * math.log2(frequency / 440.0)
                midi_note = int(round(midi_note))
                
                # 6. FILTRO DE RANGO Y ESTABILIDAD
                if self.min_note <= midi_note <= self.max_note:
                    self.history.append(midi_note)
                    
                    # Confirmación rápida (con 2 coincidencias basta)
                    if len(self.history) == 2:
                        if self.history[0] == self.history[1]:
                            return midi_note 
                        
            
        except Exception:
            pass
        
        return None

    def close(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()