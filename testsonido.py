import pygame
import time
import os

def probar_modo_hibrido():
    print("🎧 Iniciando prueba de sistema HÍBRIDO...")
    print("-----------------------------------------")
    
    # 1. VERIFICACIÓN DE ARCHIVOS
    # El juego necesita ambos para funcionar en modo híbrido
    archivos = {
        "MP3 (Audio)": "cancion.mp3",
        "MIDI (Notas)": "cancion.mid"
    }
    
    todos_ok = True
    for tipo, nombre in archivos.items():
        if os.path.exists(nombre):
            print(f"✅ {tipo}: Encontrado ('{nombre}')")
        else:
            print(f"❌ {tipo}: FALTANTE ('{nombre}')")
            if tipo == "MP3 (Audio)":
                print("   👉 TIP: Si tu archivo se llama 'cancionmario.mp3', renómbralo a 'cancion.mp3'")
            todos_ok = False
            
    if not todos_ok:
        print("\n⚠️ Faltan archivos. El test de audio podría fallar.")
        print("-----------------------------------------")

    # 2. INICIALIZACIÓN DE AUDIO (Estándar para MP3)
    try:
        pygame.init()
        pygame.mixer.init() # Dejamos que Pygame elija la mejor config automáticamente
        print(f"⚙️ Motor de Audio iniciado: {pygame.mixer.get_init()}")
    except Exception as e:
        print(f"❌ Error fatal iniciando Mixer: {e}")
        return

    # 3. REPRODUCCIÓN MP3
    mp3_file = "cancion.mp3"
    print(f"\n▶️ Intentando reproducir '{mp3_file}'...")
    
    try:
        pygame.mixer.music.load(mp3_file)
        pygame.mixer.music.set_volume(0.5) # Volumen al 50% por seguridad
        pygame.mixer.music.play()
    except Exception as e:
        print(f"❌ Error cargando MP3: {e}")
        print("   -> Asegúrate de que el archivo no esté corrupto y sea un MP3 real.")
        return

    # 4. BUCLE DE ESCUCHA
    print("🎶 REPRODUCIENDO... (Deberías escuchar la canción con calidad real)")
    print("   (Presiona Ctrl+C en la terminal para detener)")
    
    try:
        start = time.time()
        while pygame.mixer.music.get_busy():
            time.sleep(1)
            print("🎵", end="", flush=True)
            # Cortamos a los 15 segundos automáticamente
            if time.time() - start > 15:
                print("\n⏹️ Prueba finalizada con éxito.")
                break
    except KeyboardInterrupt:
        print("\n⏹️ Prueba detenida por usuario.")
    
    pygame.quit()

if __name__ == "__main__":
    probar_modo_hibrido()