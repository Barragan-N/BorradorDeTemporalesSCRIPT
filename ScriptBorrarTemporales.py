import os
import shutil
import ctypes
import winshell

def vaciar_papelera():
    print("\n--- Vaciando Papelera de Reciclaje ---")
    try:
        # Esta función de winshell hace todo el trabajo pesado
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
        print("Papelera vaciada con éxito.")
    except Exception as e:
        # A veces la papelera ya está vacía y puede lanzar un error
        print("La papelera ya está vacía o no se pudo acceder.")
 
def es_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def borrar_contenido(directorio):
    print(f"\n--- Limpiando: {directorio} ---")
    
    if not os.path.exists(directorio):
        print(f"La ruta no existe: {directorio}")
        return

    for nombre in os.listdir(directorio):
        ruta_completa = os.path.join(directorio, nombre)
        try:
            if os.path.isfile(ruta_completa) or os.path.islink(ruta_completa):
                os.unlink(ruta_completa) # Borra archivo o enlace simbólico
                print(f"Borrado: {nombre}")
            elif os.path.isdir(ruta_completa):
                shutil.rmtree(ruta_completa) # Borra carpeta y todo su contenido
                print(f"Carpeta borrada: {nombre}")
        except Exception as e:
            # Es normal que algunos archivos estén bloqueados por el sistema
            print(f"No se pudo borrar {nombre}: Archivo en uso")


def main():
    if not es_admin():
        print("ERROR! Se necesitan permisos")
        return
    rutas_a_limpiar = [os.environ.get('TEMP'),os.path.join(os.environ.get('SystemRoot'), 'TEMP'), os.path.join(os.environ.get('SystemRoot'), 'Prefetch')]
    for ruta in rutas_a_limpiar:
        borrar_contenido(ruta)
    vaciar_papelera()
    print("\n PROCESO FINALIZADO CORRECTAMENTE")
    input("Presione enter para salir")
    

if __name__ == "__main__":
    main()
        