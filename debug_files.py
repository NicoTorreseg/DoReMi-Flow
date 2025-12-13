import os

def ver_archivos():
    carpeta = os.getcwd()
    print(f"📂 Carpeta actual: {carpeta}")
    print("-------------------------------------------------")
    
    archivos = os.listdir(carpeta)
    
    # Archivos que buscamos
    buscados = ["cancion_1.0.mp3", "cancion_0.75.mp3", "cancion.mid"]
    
    for buscado in buscados:
        if buscado in archivos:
            print(f"✅ ENCONTRADO: '{buscado}'")
        else:
            print(f"❌ FALTANTE:   '{buscado}'")
            
            # Buscamos culpables parecidos (doble extensión)
            for real in archivos:
                if buscado in real and real != buscado:
                    print(f"   ⚠️ ¿Quizás quisiste decir '{real}'?")
                    print(f"      (Windows a veces oculta el .mp3 final)")

    print("-------------------------------------------------")
    print("📜 Lista completa de archivos en esta carpeta:")
    for a in archivos:
        if ".mp3" in a or ".mid" in a:
            print(f"   - {a}")

if __name__ == "__main__":
    ver_archivos()