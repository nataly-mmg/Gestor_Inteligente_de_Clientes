class GICError(Exception):
    """Excepción base del sistema GIC."""
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

