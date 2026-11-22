# reserva.py
# Clase Reserva: junta cliente, servicio, horas y estado.

from entidad import Entidad
from cliente import Cliente
from servicios import Servicio
from registro_logs import logger
from excepciones import SoftwareFJError, ReservaInvalidaError, OperacionNoPermitidaError


class Reserva(Entidad):
    # estados posibles
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    PROCESADA = "PROCESADA"

    def __init__(self, cliente, servicio, horas, **extras):
        super().__init__("RES")
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un servicio válido.")
        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._extras = extras  # aqui van cosas como personas o cantidad
        self._estado = Reserva.PENDIENTE  # empieza pendiente
        self._costo = None  # se calcula al confirmar

    @property
    def estado(self):
        return self._estado

    @property
    def costo(self):
        return self._costo

    def validar(self):
        self._servicio.verificar_disponibilidad()
        self._servicio.validar_parametros(self._horas, **self._extras)
        return True

    def confirmar(self, descuento=0.0):
        if self._estado != Reserva.PENDIENTE:  # solo se confirma si esta pendiente
            raise OperacionNoPermitidaError(f"No se puede confirmar la reserva {self.id} en estado {self._estado}.")
        # try / except / else
        try:
            self.validar()
            costo = self._servicio.calcular_costo(self._horas, descuento=descuento, **self._extras)
        except SoftwareFJError as error:
            logger.error(f"Fallo al confirmar {self.id}: {error}")
            # encadeno la excepcion para no perder el error original
            raise ReservaInvalidaError(f"No se pudo confirmar la reserva {self.id}.") from error
        else:
            # esto solo pasa si no hubo error
            self._costo = costo
            self._estado = Reserva.CONFIRMADA
            logger.info(f"Reserva {self.id} confirmada. Costo: ${costo:,.2f}")
            return costo

    def cancelar(self, motivo="Sin motivo"):
        if self._estado in (Reserva.CANCELADA, Reserva.PROCESADA):  # no se puede cancelar dos veces ni si ya se pago
            raise OperacionNoPermitidaError(f"La reserva {self.id} ya está {self._estado} y no se puede cancelar.")
        self._estado = Reserva.CANCELADA
        logger.warning(f"Reserva {self.id} cancelada. Motivo: {motivo}")

    def procesar(self, pago):
        # try / except / finally
        try:
            if self._estado != Reserva.CONFIRMADA:
                raise OperacionNoPermitidaError(f"La reserva {self.id} no está confirmada (estado: {self._estado}).")
            if not isinstance(pago, (int, float)) or pago < self._costo:  # el pago tiene que alcanzar
                raise ReservaInvalidaError(f"Pago insuficiente: ${pago} para un costo de ${self._costo:,.2f}.")
            self._estado = Reserva.PROCESADA
            cambio = round(pago - self._costo, 2)
            logger.info(f"Reserva {self.id} procesada. Pago ${pago:,.2f}, cambio ${cambio:,.2f}")
            return cambio
        except SoftwareFJError as error:
            logger.error(f"Error al procesar {self.id}: {error}")
            raise  # lo vuelvo a lanzar para que lo maneje main
        finally:
            # el finally se ejecuta siempre, haya error o no
            logger.debug(f"Intento de procesamiento de {self.id} finalizado (estado: {self._estado}).")

    def describir(self):
        costo = f"${self._costo:,.2f}" if self._costo is not None else "sin calcular"
        return (f"Reserva {self.id}: {self._cliente.nombre} -> {self._servicio.nombre} | "
                f"{self._horas} h | {self._estado} | {costo}")
