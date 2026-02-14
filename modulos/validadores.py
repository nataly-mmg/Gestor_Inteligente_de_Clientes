
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

    @staticmethod
    def validar_rut(rut):
        """
        Valida RUT chileno con dígito verificador.
        Retorna True si es válido, False si no.
        """
        rut = str(rut).strip().upper()
        
        # Eliminar puntos y guión
        rut = rut.replace(".", "").replace("-", "")
        
        # Debe tener al menos 8 caracteres (7 números + DV)
        if len(rut) < 8:
            return False
        
        cuerpo = rut[:-1]
        dv_ingresado = rut[-1]

        # El cuerpo debe ser numérico
        if not cuerpo.isdigit():
            return False

        # Cálculo del dígito verificador
        suma = 0
        multiplicador = 2

        for digito in reversed(cuerpo):
            suma += int(digito) * multiplicador
            multiplicador += 1
            if multiplicador > 7:
                multiplicador = 2

        resto = suma % 11
        dv_calculado = 11 - resto

        if dv_calculado == 11:
            dv_calculado = "0"
        elif dv_calculado == 10:
            dv_calculado = "K"
        else:
            dv_calculado = str(dv_calculado)

        return dv_ingresado == dv_calculado
