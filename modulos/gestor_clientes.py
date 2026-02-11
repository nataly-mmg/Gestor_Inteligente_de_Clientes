# ___________ importa logger + clases + errores

from modulos.logger import LoggerGIC

from modulos.clientes import ClienteRegular, ClientePremium, ClienteCorporativo, guardar_clientes_txt, cargar_clientes_txt
from modulos.errores import EmailInvalidoError, TelefonoInvalidoError, DireccionInvalidaError
from modulos.errores import DatoInvalidoError 


#___________ Registro de eventos

ARCHIVO_TXT = "base_datos.txt"


class GestorClientes:
    def __init__(self, archivo_txt=ARCHIVO_TXT):
        self._archivo_txt = archivo_txt
        self._clientes = []
        self._log = LoggerGIC()

    # -------------------------
    # Encapsulación de lista
    # -------------------------
    @property
    def clientes(self):
        # lectura controlada (si quieres, puedes devolver copia: return list(self._clientes))
        return self._clientes

    # -------------------------
    # Persistencia
    # -------------------------
    def cargar(self):
        self._clientes = cargar_clientes_txt(self._archivo_txt)
        self._log.info(f"Clientes cargados: {len(self._clientes)}")

    def guardar(self):
        guardar_clientes_txt(self._clientes, self._archivo_txt)
        self._log.info("Clientes guardados en archivo TXT")

    # -------------------------
    # Búsqueda / duplicados
    # -------------------------
    def buscar_por_nombre_email(self, nombre, email):
        nombre = nombre.strip().lower()
        email = email.strip().lower()

        for c in self.clientes:   # ✅ AQUÍ
            if c.nombre.lower() == nombre and c.email.lower() == email:
                return c
        return None
    

    def editar_interactivo(self):
        print("\n--- ✏️EDITAR CLIENTE ---")
        nombre = input("Nombre del cliente: ").strip()
        email = input("Email del cliente: ").strip()

        cliente = self.buscar_por_nombre_email(nombre, email)  # ✅

        if cliente is None:
            print("❌ Cliente no encontrado.")
            return

        try:
            nuevo_nombre = input(f"Nombre ({cliente.nombre}): ").strip()
            if nuevo_nombre:
                cliente.nombre = nuevo_nombre

            nuevo_apellido = input(f"Apellido ({cliente.apellido}): ").strip()
            if nuevo_apellido:
                cliente.apellido = nuevo_apellido

            nuevo_email = input(f"Email ({cliente.email}): ").strip()
            if nuevo_email:
                cliente.email = nuevo_email

            nuevo_tel = input(f"Teléfono ({cliente.telefono}): ").strip()
            if nuevo_tel:
                cliente.telefono = nuevo_tel

            if hasattr(cliente, "direccion"):
                nueva_dir = input(f"Dirección ({cliente.direccion}): ").strip()
                if nueva_dir:
                    cliente.direccion = nueva_dir

            if hasattr(cliente, "empresa"):
                nueva_emp = input(f"Empresa ({cliente.empresa}): ").strip()
                if nueva_emp:
                    cliente.empresa = nueva_emp

            if hasattr(cliente, "rut"):
                nuevo_rut = input("RUT (ENTER para mantener): ").strip()
                if nuevo_rut:
                    cliente.rut = nuevo_rut

            print("✅ Cliente actualizado.")
            self.log.info(f"Editar cliente: {cliente.nombre} | {cliente.email}")

        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            self.log.error(f"Editar cliente: {e}")

