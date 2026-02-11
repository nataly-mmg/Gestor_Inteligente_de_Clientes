class GICError(Exception):
    """Excepción base del sistema GIC."""
    pass


class EmailInvalidoError(GICError):
    """Se lanza cuando el email no cumple el formato requerido."""
    pass


class TelefonoInvalidoError(GICError):
    """Se lanza cuando el teléfono no cumple reglas (solo dígitos / largo)."""
    pass


class DireccionInvalidaError(GICError):
    """Se lanza cuando la dirección no cumple reglas mínimas."""
    pass



class DatoInvalidoError(GICError):
    """
    Se lanza cuando un dato ingresado no cumple con las reglas.
    Ejemplo: Un email sin '@' o un nombre vacío.
    """
    pass

class ClienteNoEncontradoError(GICError):
    """
    Se lanza cuando intentamos buscar, editar o borrar 
    un cliente que no existe en la lista.
    """
    pass

