#___________ importa 

from modulos.gestor_clientes import GestorClientes
from modulos.logger import LoggerGIC
from modulos.errores import GICError


def main():
    log = LoggerGIC()
    log.info("Sistema GIC iniciado")
             
    gestor = GestorClientes()   # usa base_datos.txt por defecto
    gestor.cargar()             # carga clientes desde TXT 

    while True:
        print("\n" + "=" * 30)
        print(" 🖥️  GESTOR DE CLIENTES (GIC)")
        print("=" * 30)
        print("1) Crear cliente")
        print("2) Listar clientes")
        print("3) Editar cliente")
        print("4) Eliminar cliente")
        print("5) Salir")
        print("=" * 30)

        op = input("Seleccione opción (1-5): ").strip()

        try:
            if op == "1":
                log.info("Menú | Crear cliente")
                nuevo = gestor.crear_cliente_interactivo()

                if nuevo is None:
                    continue

                if gestor.agregar_cliente(nuevo):
                    print("✅ Cliente creado.")
                else:
                    print("⚠️ Cliente duplicado.")

            elif op == "2":
                log.info("Menú | Listar clientes")
                print("\n--- LISTADO DE CLIENTES ---")
                gestor.listar_clientes()


            elif op == "3":
                log.info("Menú | Editar cliente")
                gestor.editar_interactivo()


            elif op == "4":
                log.info("Menú | Eliminar cliente")
                gestor.eliminar_interactivo()


            elif op == "5":
                gestor.guardar()
                log.info("Menú | Salir del sistema")
                print("👋 Hasta luego.")
                break

            else:
                print("Opción inválida.")
                log.warning(f"Menú | Opción inválida ingresada: {op}")

        except GICError as e:
            log.error(f"Error crítico no controlado en main: {e}")
            print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    main()