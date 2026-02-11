#____________ Le pregunta a Windows si el archivo ya está creado
import os
from datetime import datetime

# ==========================================
#____________ Sistema de logs
# ==========================================

class LoggerGIC:

    def __init__(self, archivo_log=None):
        if archivo_log is None:
            carpeta_modulos = os.path.dirname(__file__)
            archivo_log = os.path.join(carpeta_modulos, "actividad.log")
        self.archivo_log = archivo_log

    def _escribir(self, nivel, mensaje):
    #    Método privado que maneja la apertura del archivo (Encapsulamiento).
        try:
            with open(self.archivo_log, "a", encoding="utf-8") as f:
                # Formato: FECHA | NIVEL | MENSAJE
                f.write(f"{datetime.now()} | {nivel.upper()} | {mensaje}\n")
        except IOError as e:
            # Si falla el log, lo mostramos en consola para no perder la alerta
            print(f"⚠️ Error crítico: No se pudo escribir en el log: {e}")

    # --- MÉTODOS PÚBLICOS (La interfaz para el resto del sistema) ---

    def info(self, mensaje):
        self._escribir("INFO", mensaje)

    def warning(self, mensaje):
        self._escribir("WARNING", mensaje)

    def error(self, mensaje):
        self._escribir("ERROR", mensaje)