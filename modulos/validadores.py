
import re

class Validador:

    @staticmethod
    def validar_email(email):
    # Verifica si el string tiene formato de correo electrónico.
    # Retorna True si es válido, False si no.
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(patron, str(email).strip()))

    @staticmethod
    def validar_telefono(telefono):
    # Verifica que el teléfono solo tenga números y un largo razonable
        telefono = str(telefono).strip()
        return telefono.isdigit() and 8 <= len(telefono) <= 15

    @staticmethod
    def validar_campo_no_vacio(texto):
        return bool(texto and str(texto).strip())

    @staticmethod
    def validar_solo_letras(texto):
        texto = str(texto).strip()
        patron = r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$'
        return bool(re.match(patron, texto))

