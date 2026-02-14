# ___________ importa logger + clases + errores

from modulos.logger import LoggerGIC

from modulos.clientes import (ClienteRegular, ClientePremium, ClienteCorporativo, guardar_clientes_txt, cargar_clientes_txt)

from modulos.errores import DatoInvalidoError, ClienteNoEncontradoError

from modulos.validadores import Validador

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

    # -------------------------
    # Búsqueda / duplicados
    # -------------------------
    def buscar_por_nombre_email(self, nombre, email):
        nombre = nombre.strip().lower()
        email = email.strip().lower()


        # -------- VALIDACIONES --------
        if not Validador.validar_campo_no_vacio(nombre):
            raise DatoInvalidoError("Nombre obligatorio.")

        if not Validador.validar_solo_letras(nombre):
            raise DatoInvalidoError("El nombre solo puede contener letras.")

        if not Validador.validar_email(email):
            raise DatoInvalidoError("Email con formato inválido.")

        # -------- BÚSQUEDA --------
        for c in self.clientes:  
            if c.nombre.lower() == nombre and c.email.lower() == email:
                return c
            
         # -------- NO ENCONTRADO --------
        raise ClienteNoEncontradoError("Cliente no encontrado con ese nombre y email.")


    def es_duplicado(self, nuevo_cliente):
        # usa __eq__ 
        return nuevo_cliente in self._clientes


    # -------------------------
    # Agregar - con persistencia + logs
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
        # -------------------------
        # DATOS BASE (con validación individual)
        # -------------------------
             
            nombre = self.pedir_dato(
                "Nombre: ",
                (Validador.validar_campo_no_vacio, "Nombre obligatorio."),
                (Validador.validar_solo_letras, "Nombre solo puede contener letras.")
            )
            
            apellido = self.pedir_dato(
                "Apellido: ",
                (Validador.validar_campo_no_vacio, "Apellido obligatorio."),
                (Validador.validar_solo_letras, "Apellido solo puede contener letras.")
            )

            email = self.pedir_dato(
                "Email: ",
                (Validador.validar_campo_no_vacio, "Email obligatorio."),
                (Validador.validar_email, "Email con formato inválido.")
            )

            tel = self.pedir_dato(
                "Teléfono: ",
                (Validador.validar_campo_no_vacio, "Teléfono obligatorio."),
                (Validador.validar_telefono, "Teléfono debe ser numérico (8-15 dígitos).")
            )


        # -------------------------
        # SEGÚN TIPO
        # -------------------------
         
            if tipo == "1":
                # ClienteRegular(nombre, apellido, email, tel)
                nuevo_cliente = ClienteRegular(nombre, apellido, email, tel)

            elif tipo == "2":
                # ClientePremium(nombre, apellido, rut, email, tel, dirc)
                
                rut = self.pedir_dato(
                    "RUT: ",
                    (Validador.validar_campo_no_vacio, "RUT obligatorio."),
                    (Validador.validar_rut, "RUT inválido.")
                )

                dirc = self.pedir_dato(
                    "Dirección: ",
                    (Validador.validar_campo_no_vacio, "Dirección obligatoria."),
                )

                nuevo_cliente = ClientePremium(nombre, apellido, rut, email, tel, dirc)

            elif tipo == "3":
                # ClienteCorporativo(nombre, apellido, email, tel, empresa, dirc, rut)

                empresa = self.pedir_dato(
                    "Empresa (Razón Social): ",
                    (Validador.validar_campo_no_vacio, "Empresa (Razón Social) obligatoria."),
                )

                rut = self.pedir_dato(
                    "RUT: ",
                    (Validador.validar_campo_no_vacio, "RUT obligatorio."),
                    (Validador.validar_rut, "RUT inválido.")
                )

                dirc = self.pedir_dato(
                    "Dirección: ",
                    (Validador.validar_campo_no_vacio, "Dirección obligatoria."),
                )

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
    

        try:
            nombre = self.pedir_dato("Nombre del cliente: ",
                (Validador.validar_campo_no_vacio, "Nombre obligatorio."),
                (Validador.validar_solo_letras, "Nombre solo puede contener letras.")
            )

            email = self.pedir_dato("Email del cliente: ",
                (Validador.validar_campo_no_vacio, "Email obligatorio."),
                (Validador.validar_email, "Email con formato inválido.")
            )


            # Busca (ideal: este método lanza ClienteNoEncontradoError si no existe)
            cliente = self.buscar_por_nombre_email(nombre, email)

            if cliente is None:
                raise ClienteNoEncontradoError("Cliente no encontrado con ese nombre y email.")

        except ClienteNoEncontradoError as e:
            print(f"❌ {e}")
            self._log.warning(str(e))
            return

        except DatoInvalidoError as e:
            print(f"❌ {e}")
            self._log.warning(f"Identificación inválida en edición: {e}")
            return
        
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            self._log.error(f"Error inesperado en identificación (editar): {e}")
            return


        print(f"\nEditando cliente: {cliente.nombre} {cliente.apellido}")
        print("Presione ENTER para mantener el valor actual.\n")


        # -------------------------
        # EDICIÓN (con pedir_dato y ENTER mantiene)
        # -------------------------

        try:
            # --- CAMPOS COMUNES ---
           
            nuevo_nombre = input(f"Nombre ({cliente.nombre}): ").strip()
            if nuevo_nombre:
                cliente.nombre = nuevo_nombre  # setter valida no vacío + solo letras


            nuevo_apellido = input(f"Apellido ({cliente.apellido}): ").strip()
            if nuevo_apellido:
                cliente.apellido = nuevo_apellido

            nuevo_email = input(f"Email ({cliente.email}): ").strip()
            if nuevo_email:
                cliente.email = nuevo_email

            nuevo_tel = input(f"Teléfono ({cliente.telefono}): ").strip()
            if nuevo_tel:
                cliente.telefono = nuevo_tel

            if isinstance(cliente, ClientePremium):
                nuevo_rut = input("RUT persona (ENTER para mantener): ").strip()
                if nuevo_rut:
                        cliente.rut = nuevo_rut

                nueva_dir = input(f"Dirección ({cliente.direccion}): ").strip()
                if nueva_dir:
                        cliente.direccion = nueva_dir

            elif isinstance(cliente, ClienteCorporativo):
                nueva_empresa = input(f"Empresa ({cliente.empresa}): ").strip()
                if nueva_empresa:
                        cliente.empresa = nueva_empresa

                nuevo_rut = input("RUT empresa (ENTER para mantener): ").strip()
                if nuevo_rut:
                        cliente.rut = nuevo_rut

                nueva_dir = input(f"Dirección ({cliente.direccion}): ").strip()
                if nueva_dir:
                        cliente.direccion = nueva_dir


            # Guardar cambios
            self.guardar()

            print("✅ Cliente actualizado correctamente.")
            self._log.info(f"Cliente editado: {cliente.nombre} {cliente.apellido} | {cliente.email}")

        except (ValueError, DatoInvalidoError) as e:
            print(f"❌ Error al editar cliente: {e}")
            self._log.warning(f"Error al editar cliente ({cliente.nombre} | {cliente.email}): {e}")


        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            self._log.error(f"Error inesperado editando cliente ({cliente.nombre} | {cliente.email}): {e}")


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
# Pedor dato Es una función que:

# Muestra el mensaje

# Ejecuta una validación

# Si falla → muestra error

# Si pasa → retorna el valor

# Repite hasta que sea válido
    # --------------

    def pedir_dato(self, mensaje, *reglas):

    # reglas: tuplas (funcion_validacion, mensaje_error)

        while True:
            valor = input(mensaje).strip()

            try:
                for funcion, msg_error in reglas:
                    if not funcion(valor):
                        raise DatoInvalidoError(msg_error)

                return valor  # ✅ pasó todas las validaciones

            except DatoInvalidoError as e:
                print(f"🛑 {e}")
                self._log.warning(str(e))


    # -------------------------
    # Eliminar (por nombre+email)
    # -------------------------
    def eliminar_interactivo(self):
        print("\n--- 🗑️  ELIMINAR CLIENTE ---")

        try:
            nombre = self.pedir_dato(
                "Nombre: ",
                (Validador.validar_campo_no_vacio, "Nombre obligatorio."),
                (Validador.validar_solo_letras, "Nombre solo puede contener letras.")
            )

            email = self.pedir_dato(
                "Email: ",
                (Validador.validar_campo_no_vacio, "Email obligatorio."),
                (Validador.validar_email, "Email no tiene formato válido.")
            )

            self._log.info(f"Solicitud de eliminación: {nombre} | {email}")

            cliente = self.buscar_por_nombre_email(nombre, email)

            if not cliente:
                raise ClienteNoEncontradoError("Cliente no encontrado con ese nombre y email.")

            self._clientes.remove(cliente)
            self.guardar()

            self._log.info(f"Cliente eliminado: {cliente.nombre} | {cliente.email}")
            print("✅ Cliente eliminado.")
            return True

        except (DatoInvalidoError, ValueError) as e:
            print(f"🛑 Error de datos: {e}")
            self._log.warning(f"Eliminar cliente | datos inválidos: {e}")
            return False

        except ClienteNoEncontradoError as e:
            print(f"❌ {e}")
            self._log.warning(f"Eliminar cliente | no encontrado: {nombre} | {email}")
            return False

        except Exception as e:
            print(f"🔥 Error inesperado: {e}")
            self._log.error(f"Eliminar cliente | error crítico: {e}")
            return False
