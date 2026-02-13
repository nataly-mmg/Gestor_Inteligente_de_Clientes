# ___________ importa logger + clases + errores

from modulos.logger import LoggerGIC

from modulos.clientes import (ClienteRegular, ClientePremium, ClienteCorporativo, guardar_clientes_txt, cargar_clientes_txt)

from modulos.errores import DatoInvalidoError, ClienteNoEncontradoError

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



    def es_duplicado(self, nuevo_cliente):
        # usa __eq__ 
        return nuevo_cliente in self._clientes


    # -------------------------
    # Alta (agregar) - con persistencia + logs
    # -------------------------
    def agregar_cliente(self, nuevo_cliente):
        if nuevo_cliente is None:
            return False

        if self.es_duplicado(nuevo_cliente):
            self._log.warning(f"Duplicado evitado: {nuevo_cliente.nombre} | {nuevo_cliente.email}")
            return False

        self._clientes.append(nuevo_cliente)
        self.guardar()
        self._log.info(f"Cliente creado: {nuevo_cliente.nombre} | {nuevo_cliente.email}")
        return True





 # -------------------------
    # CREACIÓN INTERACTIVA 
    # -------------------------
    def crear_cliente_interactivo(self):
        print("\nSeleccione un tipo de cliente a crear:")
        print("1. Cliente Regular")
        print("2. Cliente Premium")
        print("3. Cliente Corporativo")
        print("X. Volver al menú principal")

        tipo = input(">> Seleccione opción: ").strip().lower()

        # usuario vuelve
        if tipo == "x":
            return None

        try:
            # Datos base (siempre)
            nombre = input("Nombre: ").strip()
            apellido = input("Apellido: ").strip()
            email = input("Email: ").strip()
            tel = input("Teléfono: ").strip()

         
            if tipo == "1":
                # ClienteRegular(nombre, apellido, email, tel)
                nuevo_cliente = ClienteRegular(nombre, apellido, email, tel)

            elif tipo == "2":
                # ClientePremium(nombre, apellido, rut, email, tel, dirc)
                rut = input("RUT persona: ").strip()
                dirc = input("Dirección: ").strip()
                nuevo_cliente = ClientePremium(nombre, apellido, rut, email, tel, dirc)

            elif tipo == "3":
                # ClienteCorporativo(nombre, apellido, email, tel, empresa, dirc, rut)
                empresa = input("Razón Social (Empresa): ").strip()
                dirc = input("Dirección: ").strip()
                rut = input("RUT empresa: ").strip()
                nuevo_cliente = ClienteCorporativo(nombre, apellido, email, tel, empresa, dirc, rut)

            else:
                print("❌ Tipo de cliente inválido.")
                self._log.warning(f"Selección de tipo inválida: {tipo}")
                return None

            return nuevo_cliente

        except (ValueError, DatoInvalidoError) as e:
            print(f"🛑 Error de datos: {e}")
            self._log.warning(f"Fallo al crear cliente: {e}")
            return None

        except Exception as e:
            print(f"🔥 Error inesperado: {e}")
            self._log.error(f"Error crítico creando cliente: {e}")
            return None



# -------------------------
    # Editar
    # -------------------------

    def editar_interactivo(self):
        print("\n--- ✏️ EDITAR CLIENTE ---")

        if not self._clientes:
            print("❌ No hay clientes registrados.")
            return

        # Identificación del cliente
        nombre = input("Nombre del cliente: ").strip()
        email = input("Email del cliente: ").strip()

        cliente = None
        for c in self._clientes:
            if c.nombre.lower() == nombre.lower() and c.email.lower() == email.lower():
                cliente = c
                break

        if cliente is None:
            try:
                raise ClienteNoEncontradoError("Cliente no encontrado con ese nombre y email.")
            except ClienteNoEncontradoError as e:
                print(f"❌ {e}")
                self._log.warning(str(e))
                return

        print(f"\nEditando cliente: {cliente.nombre} {cliente.apellido}")
        print("Presione ENTER para mantener el valor actual.\n")

        try:
            # --- CAMPOS COMUNES ---
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

            # --- CAMPOS SEGÚN TIPO ---
            if isinstance(cliente, ClientePremium):
                nuevo_rut = input(f"RUT ({cliente.rut}): ").strip()
                if nuevo_rut:
                    cliente.rut = nuevo_rut

                nueva_dir = input(f"Dirección ({cliente.direccion}): ").strip()
                if nueva_dir:
                    cliente.direccion = nueva_dir

            elif isinstance(cliente, ClienteCorporativo):
                nueva_empresa = input(f"Empresa ({cliente.empresa}): ").strip()
                if nueva_empresa:
                    cliente.empresa = nueva_empresa

                nuevo_rut = input(f"RUT Empresa ({cliente.rut}): ").strip()
                if nuevo_rut:
                    cliente.rut = nuevo_rut

                nueva_dir = input(f"Dirección ({cliente.direccion}): ").strip()
                if nueva_dir:
                    cliente.direccion = nueva_dir

            print("✅ Cliente actualizado correctamente.")
            self._log.info(f"Cliente editado: {cliente.nombre} {cliente.apellido} | {cliente.email}")

        except (ValueError, DatoInvalidoError) as e:
            print(f"❌ Error al editar cliente: {e}")
            self._log.warning(f"Error al editar cliente ({cliente.nombre} | {cliente.email}): {e}")


    # -------------------------
    # Listar
    # -------------------------
    def listar_clientes(self):
        print("\n--- LISTADO DE CLIENTES ---")

        if not self.clientes:
            print("(Sin clientes registrados)")
            return

        for i, c in enumerate(self.clientes, 1):
            print(f"\n{i}. {c.__class__.__name__}")
            print(f"   Nombre   : {c.nombre} {c.apellido}")
            print(f"   Email    : {c.email}")
            print(f"   Teléfono : {c.telefono}")

            if hasattr(c, "empresa"):
                print(f"   Empresa  : {c.empresa}")

            if hasattr(c, "rut"):
                print(f"   RUT      : {c.rut}")

            if hasattr(c, "direccion"):
                print(f"   Dirección: {c.direccion}")

            print(f"   Descuento: {int(c.obtener_descuento()*100)}%")


    # --------------