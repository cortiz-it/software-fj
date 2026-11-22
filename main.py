# main.py
# Programa principal de Software FJ.
# Aqui pruebo mas de 10 operaciones (buenas y malas) para ver que el programa
# no se cae aunque haya errores.
# Para ejecutar:  python main.py

from sistema import GestorSoftwareFJ
from registro_logs import logger, RUTA_LOG
from excepciones import SoftwareFJError

contador = {"exitosas": 0, "fallidas": 0}  # para contar como salieron las operaciones


def ejecutar(numero, descripcion, operacion):
    # cada operacion va dentro de try/except/else/finally para que el programa siga
    print(f"\n[{numero:02d}] {descripcion}")
    try:
        resultado = operacion()
    except SoftwareFJError as error:  # errores que ya tengo controlados
        contador["fallidas"] += 1
        print(f"     [ERROR CONTROLADO] {error}")
        if error.__cause__:  # si viene de un raise ... from ... muestro el error original
            print(f"       Causa original: {error.__cause__}")
        logger.error(f"Operación {numero} fallida: {error} | causa: {error.__cause__}")
    except Exception as error:  # por si pasa algo que no esperaba
        contador["fallidas"] += 1
        print(f"     [ERROR INESPERADO] {type(error).__name__}: {error}")
        logger.critical(f"Operación {numero} - error inesperado: {error!r}")
    else:  # si todo salio bien
        contador["exitosas"] += 1
        print(f"     [OK] -> {resultado}")
    finally:  # esto siempre se ejecuta
        logger.debug(f"Operación {numero} finalizada: {descripcion}")


def main():
    gestor = GestorSoftwareFJ()
    print("=" * 60)
    print("  SOFTWARE FJ - Gestión de Clientes, Servicios y Reservas")
    print("=" * 60)

    # ---------- clientes ----------
    ejecutar(1, "Registrar cliente válido (Ana Gómez)",
             lambda: gestor.registrar_cliente("ana gómez", "1012345678", "ana@correo.com", "3001234567"))
    ejecutar(2, "Registrar cliente válido (Luis Pérez)",
             lambda: gestor.registrar_cliente("Luis Pérez", "79123456", "luis.perez@mail.co", "3109876543"))
    ejecutar(3, "Registrar cliente con correo inválido",  # al correo le falta el @
             lambda: gestor.registrar_cliente("Marta Ruiz", "52111222", "marta-correo.com", "3201112233"))
    ejecutar(4, "Registrar cliente sin nombre",
             lambda: gestor.registrar_cliente("", "52333444", "x@y.com", "3201112233"))
    ejecutar(5, "Registrar cliente duplicado (mismo documento de Ana)",
             lambda: gestor.registrar_cliente("Ana María", "1012345678", "otra@correo.com", "3001112222"))

    # ---------- servicios ----------
    ejecutar(6, "Crear servicio Sala de Juntas",
             lambda: gestor.crear_servicio("sala", "Sala Juntas", 50000, capacidad=10))
    ejecutar(7, "Crear servicio Alquiler de Portátiles",
             lambda: gestor.crear_servicio("equipo", "Portatiles", 15000, tipo_equipo="Portátil", unidades=5))
    ejecutar(8, "Crear servicio Asesoría en Ciberseguridad (experto)",
             lambda: gestor.crear_servicio("asesoria", "Ciberseguridad", 80000, especialidad="Seguridad", nivel="experto"))
    ejecutar(9, "Crear servicio con tarifa negativa",
             lambda: gestor.crear_servicio("sala", "Sala Mala", -100, capacidad=5))
    ejecutar(10, "Crear servicio de tipo inexistente",
             lambda: gestor.crear_servicio("transporte", "Bus", 10000))
    ejecutar(11, "Crear asesoría con nivel no permitido",
             lambda: gestor.crear_servicio("asesoria", "Redes", 60000, especialidad="Redes", nivel="master"))
    ejecutar(12, "Crear equipo Proyectores sin unidades (queda no disponible)",
             lambda: gestor.crear_servicio("equipo", "Proyectores", 10000, tipo_equipo="Proyector", unidades=0))

    # ---------- costos (las formas de cotizar) ----------
    ejecutar(13, "Cotizar sala 3 h (solo horas, con IVA)",
             lambda: gestor.buscar_servicio("Sala Juntas").cotizar(3))
    ejecutar(14, "Cotizar asesoría 2 h sin IVA y 10 % desc. (con tupla)",
             lambda: gestor.buscar_servicio("Ciberseguridad").cotizar((2, 0, 0.10)))
    ejecutar(15, "Cotizar 3 portátiles por 4 h (con diccionario)",
             lambda: gestor.buscar_servicio("Portatiles").cotizar({"horas": 4, "cantidad": 3}))
    ejecutar(16, "Cotizar con descuento del 150 %",  # esto no deberia dejar
             lambda: gestor.buscar_servicio("Sala Juntas").calcular_costo(2, descuento=1.5))

    # ---------- reservas ----------
    def reserva_exitosa():  # crear, confirmar y pagar
        r = gestor.crear_reserva("1012345678", "Sala Juntas", 4, personas=8)
        r.confirmar()
        cambio = r.procesar(300000)
        return f"{r.describir()} | cambio ${cambio:,.2f}"

    def reserva_con_descuento():
        r = gestor.crear_reserva("79123456", "Ciberseguridad", 2)
        r.confirmar(descuento=0.15)
        return r.describir()

    def reserva_excede_capacidad():  # 25 personas en una sala de 10
        r = gestor.crear_reserva("79123456", "Sala Juntas", 2, personas=25)
        return r.confirmar()

    def reserva_servicio_no_disponible():  # los proyectores tienen 0 unidades
        r = gestor.crear_reserva("1012345678", "Proyectores", 3)
        return r.confirmar()

    def reserva_cliente_inexistente():
        return gestor.crear_reserva("99999999", "Sala Juntas", 2)

    def reserva_duracion_invalida():  # la asesoria es maximo 8 horas
        r = gestor.crear_reserva("1012345678", "Ciberseguridad", 20)
        return r.confirmar()

    def cancelar_dos_veces():
        r = gestor.crear_reserva("79123456", "Portatiles", 5, cantidad=2)
        r.cancelar("El cliente cambió de fecha")
        r.cancelar("Intento repetido")  # aqui tiene que salir error

    def pago_insuficiente():
        r = gestor.crear_reserva("79123456", "Portatiles", 2, cantidad=1)
        r.confirmar()
        return r.procesar(1000)

    def procesar_sin_confirmar():
        r = gestor.crear_reserva("1012345678", "Sala Juntas", 1)
        return r.procesar(100000)

    ejecutar(17, "Reserva exitosa completa (crear, confirmar y pagar)", reserva_exitosa)
    ejecutar(18, "Reserva de asesoría con 15 % de descuento", reserva_con_descuento)
    ejecutar(19, "Reserva que excede la capacidad de la sala", reserva_excede_capacidad)
    ejecutar(20, "Reserva de servicio no disponible (Proyectores)", reserva_servicio_no_disponible)
    ejecutar(21, "Reserva para cliente inexistente", reserva_cliente_inexistente)
    ejecutar(22, "Reserva con duración inválida (20 h de asesoría)", reserva_duracion_invalida)
    ejecutar(23, "Cancelar una reserva dos veces", cancelar_dos_veces)
    ejecutar(24, "Procesar pago insuficiente", pago_insuficiente)
    ejecutar(25, "Procesar reserva sin confirmar", procesar_sin_confirmar)

    # ---------- resumen final ----------
    print(gestor.resumen())
    print(f"\nOperaciones exitosas: {contador['exitosas']} | fallidas (controladas): {contador['fallidas']}")
    print(f"El programa terminó sin cerrarse. El log quedó en: {RUTA_LOG}")
    logger.info(f"=== Fin de la simulación: {contador} ===")


if __name__ == "__main__":
    main()
