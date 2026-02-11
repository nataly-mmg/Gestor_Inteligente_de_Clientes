
import re

def validar_email(email):
    """
    Verifica si el string tiene formato de correo electrónico.
    Retorna True si es válido, False si no.
    """
    # Explicación Regex: 
    # ^        : Inicio del texto
    # [\w\.-]+ : Letras, números, puntos o guiones
    # @        : Arroba obligatoria
    # [\w\.-]+ : Dominio (ej: gmail)
    # \.       : Punto obligatorio
    # \w+      : Extensión (ej: com, cl)
    # $        : Fin del texto
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    
    # re.match devuelve un objeto si coincide, o None si no.
    # Usamos bool() para convertir eso a True/False.
    return bool(re.match(patron, email))

def validar_telefono(telefono):
    """
    Verifica que el teléfono solo tenga números y un largo razonable.
    """
    # 1. .isdigit() revisa que sean solo números (sin letras ni símbolos)
    # 2. len() revisa que el largo esté entre 8 y 15 caracteres
    return telefono.isdigit() and 8 <= len(telefono) <= 15



def validar_direccion(direccion):
    direccion = str(direccion).strip()
    if not direccion:
        raise ValueError("La dirección no puede estar vacía.")
    return direccion
                

def validar_campo_no_vacio(texto):
    """
    Verifica que el texto no esté vacío ni sea solo espacios en blanco.
    """
    # texto.strip() elimina espacios al inicio y final.
    # Si queda algo, es True. Si queda vacío "", es False.
    return bool(texto and texto.strip())




