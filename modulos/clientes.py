#___________ importa clase

from modulos.logger import LoggerGIC
from modulos.validadores import Validador
from modulos.errores import  DatoInvalidoError

log = LoggerGIC()
ARCHIVO_TXT = "base_datos.txt"

#__________ Clase Padre

# =========================================
# CLIENTES + PERSISTENCIA TXT 
# =========================================


# --------- CLASE PADRE ---------
class Cliente:
    def __init__(self, nombre, apellido, email, telefono):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono

    # =========================
    # NOMBRE
    # =========================
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, value):
        value = str(value).strip()

        if not Validador.validar_campo_no_vacio(value):
            raise DatoInvalidoError("Nombre obligatorio.")
    
        if not Validador.validar_solo_letras(value):
            raise DatoInvalidoError("Nombre solo puede contener letras.")
    
        self._nombre = value

    # =========================
    # APELLIDO
    # =========================
    @property
    def apellido(self):
        return self._apellido

    @apellido.setter 
    def apellido(self, value):
        value = str(value).strip()

        if not Validador.validar_campo_no_vacio(value):
            raise DatoInvalidoError("El apellido no puede estar vacío.")
        
        if not Validador.validar_solo_letras(value):
            raise DatoInvalidoError("El apellido solo puede contener letras.")
        
        self._apellido = value

    # =========================
    # EMAIL
    # =========================
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        value = str(value).strip()

        if not Validador.validar_email(value):
            raise DatoInvalidoError(f"El email no tiene formato válido.")
        
        self._email = value

    # =========================
    # TELÉFONO
    # =========================
    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, value):
        value = str(value).strip()

        if not Validador.validar_telefono(value):
            raise DatoInvalidoError(f"El teléfono '{value}' debe ser numérico (8-15 dígitos)." )
        
        self._telefono = value




# ==================================================
# SUBCLASES
# ==================================================

class ClienteRegular(Cliente):
    """
    Firma: ClienteRegular(nombre, apellido, email, tel)
    Descuento: 10%
    """
    def obtener_descuento(self):
        return 0.10

    def convertir_a_texto(self):
        # Tipo|Nombre|Apellido|Email|Tel
        return f"ClienteRegular|{self.nombre}|{self.apellido}|{self.email}|{self.telefono}"

    def __str__(self):
        return f"[REGULAR 10%] {super().__str__()}"


class ClientePremium(Cliente):
    """
    Firma: ClientePremium(nombre, apellido, rut, email, tel, dirc)
    Descuento: 20%
    Atributos extra: rut (privado), direccion
    """

    def __init__(self, nombre, apellido, rut, email, telefono, direccion):
        super().__init__(nombre, apellido, email, telefono)
        self.rut = rut
        self.direccion = direccion

    # =========================
    # RUT (privado)
    # =========================
    @property
    def rut(self):
        return self.__rut

    @rut.setter
    def rut(self, value):
        value = str(value).strip()
        if not value:
            raise DatoInvalidoError("El RUT es obligatorio para clientes Premium.")
        self.__rut = value

    # =========================
    # DIRECCIÓN
    # =========================
    @property
    def direccion(self):
        return self._direccion

    @direccion.setter
    def direccion(self, value):
        value = str(value).strip()

        if not Validador.validar_campo_no_vacio(value):
            raise DatoInvalidoError("La dirección no puede estar vacío.")
        
        self._direccion = value
    



    def obtener_descuento(self):
        return 0.20

    def convertir_a_texto(self):
        # Tipo|Nombre|Apellido|RUT|Email|Tel|Direccion
        return f"ClientePremium|{self.nombre}|{self.apellido}|{self.rut}|{self.email}|{self.telefono}|{self.direccion}"

    def __str__(self):
        return f"[PREMIUM 20% 💎] {self.nombre} {self.apellido} | RUT: {self.rut} | Email: {self.email} | Tel: {self.telefono} | Dir: {self.direccion}"


class ClienteCorporativo(Cliente):
    """
    Firma: ClienteCorporativo(nombre, apellido, email, tel, empresa, dirc, rut)
    Descuento: 30%
    Atributos extra: empresa, direccion, rut (privado)
    """

    def __init__(self, nombre, apellido, email, telefono, empresa, direccion, rut):
        super().__init__(nombre, apellido, email, telefono)

        if not Validador.validar_campo_no_vacio(empresa):
            raise DatoInvalidoError("Indicar la empresa (Razón Social) es obligatorio.")
        self.empresa = str(empresa).strip()

        self.direccion = direccion
        self.rut = rut

    # =========================
    # RUT (privado)
    # =========================
    @property
    def rut(self):
        return self.__rut

    @rut.setter
    def rut(self, value):
        value = str(value).strip()
        if not value:
            raise DatoInvalidoError("El RUT empresa es obligatorio para clientes corporativos.")
        self.__rut = value

    # =========================
    # DIRECCIÓN
    # =========================
    @property
    def direccion(self):
        return self._direccion

    @direccion.setter
    def direccion(self, value):
        self._direccion = Validador.validar_campo_no_vacio(value)

    def obtener_descuento(self):
        return 0.30

    def convertir_a_texto(self):
        # Tipo|Nombre|Apellido|Email|Tel|Empresa|Direccion|RUT
        return f"ClienteCorporativo|{self.nombre}|{self.apellido}|{self.email}|{self.telefono}|{self.empresa}|{self.direccion}|{self.rut}"

    def __str__(self):
        return f"[CORPORATIVO 30% 🏢] {self.empresa} | Contacto: {self.nombre} {self.apellido} | Email: {self.email} | Tel: {self.telefono} | Dir: {self.direccion} | RUT: {self.rut}"



# ==================================================
# PERSISTENCIA TXT
# ==================================================

def guardar_clientes_txt(clientes, ruta=ARCHIVO_TXT):
    """
    Guarda una línea por cliente en TXT (separado por '|').
    """
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            for c in clientes:
                f.write(c.convertir_a_texto() + "\n")

        log.info(f"Persistencia OK: guardados {len(clientes)} clientes en '{ruta}'")

    except Exception as e:
        log.error(f"Persistencia ERROR al guardar en '{ruta}': {e}")
        print("❌ No se pudo guardar el archivo de clientes.-prueba----")


def cargar_clientes_txt(ruta=ARCHIVO_TXT):
    """
    Carga clientes desde TXT
    """
    clientes = []
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            for nro_linea, linea in enumerate(f, start=1):
                linea = linea.strip()
                if not linea:
                    continue

                partes = linea.split("|")
                tipo = partes[0]

                try:
                    if tipo == "ClienteRegular":
                        _, nombre, apellido, email, tel = partes
                        clientes.append(ClienteRegular(nombre, apellido, email, tel))

                    elif tipo == "ClientePremium":
                        _, nombre, apellido, rut, email, tel, dirc = partes
                        clientes.append(ClientePremium(nombre, apellido, rut, email, tel, dirc))

                    elif tipo == "ClienteCorporativo":
                        _, nombre, apellido, email, tel, empresa, dirc, rut = partes
                        clientes.append(ClienteCorporativo(nombre, apellido, email, tel, empresa, dirc, rut))

                    else:
                        log.warning(f"TXT línea {nro_linea}: tipo desconocido '{tipo}' (omitido)")

                except Exception as e:
                    log.error(f"TXT línea {nro_linea}: error al reconstruir cliente: {e}")

        log.info(f"Persistencia OK: cargados {len(clientes)} clientes desde '{ruta}'")
        return clientes

    except FileNotFoundError:
        log.warning(f"Persistencia: no existe '{ruta}', se inicia lista vacía")
        return []

    except Exception as e:
        log.error(f"Persistencia ERROR al cargar '{ruta}': {e}")
        return []
