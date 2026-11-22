# sistema.py
# GestorSoftwareFJ: guarda clientes, servicios y reservas en listas (no hay base de datos)

from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from reserva import Reserva
from registro_logs import logger
from excepciones import (SoftwareFJError, ClienteDuplicadoError, DatoInvalidoError,
                         ServicioNoDisponibleError, ReservaInvalidaError)


class GestorSoftwareFJ:
    # para crear el servicio segun el texto que llegue
    TIPOS_SERVICIO = {"sala": ReservaSala, "equipo": AlquilerEquipo, "asesoria": Asesoria}

    def __init__(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []
        logger.info("=== Sistema Software FJ iniciado ===")

    # ----- clientes -----
    def registrar_cliente(self, nombre, documento, correo, telefono):
        # primero miro que no este repetido
        if any(c.documento == str(documento).strip() for c in self._clientes):
            raise ClienteDuplicadoError(documento)
        try:
            cliente = Cliente(nombre, documento, correo, telefono)
        except SoftwareFJError as error:
            logger.error(f"Registro de cliente rechazado: {error}")
            raise
        self._clientes.append(cliente)
        logger.info(f"Cliente registrado: {cliente.describir()}")
        return cliente

    def buscar_cliente(self, documento):
        for cliente in self._clientes:
            if cliente.documento == str(documento):
                return cliente
        raise DatoInvalidoError("documento", documento, "Cliente no encontrado.")

    # ----- servicios -----
    def crear_servicio(self, tipo, *args, **kwargs):
        clase = self.TIPOS_SERVICIO.get(tipo)
        if clase is None:
            raise DatoInvalidoError("tipo", tipo, f"Tipos válidos: {list(self.TIPOS_SERVICIO)}.")
        try:
            servicio = clase(*args, **kwargs)
        except TypeError as error:  # pasa si mandan mal los argumentos
            raise DatoInvalidoError("parámetros", args, "Argumentos incorrectos para el servicio.") from error
        self._servicios.append(servicio)
        logger.info(f"Servicio creado: {servicio.describir()}")
        return servicio

    def buscar_servicio(self, nombre):
        for servicio in self._servicios:
            if servicio.nombre.lower() == str(nombre).lower():  # sin importar mayusculas
                return servicio
        raise ServicioNoDisponibleError(nombre)

    # ----- reservas -----
    def crear_reserva(self, documento, nombre_servicio, horas, **extras):
        try:
            cliente = self.buscar_cliente(documento)
            servicio = self.buscar_servicio(nombre_servicio)
        except SoftwareFJError as error:
            raise ReservaInvalidaError("No se pudo crear la reserva: datos de origen incorrectos.") from error
        reserva = Reserva(cliente, servicio, horas, **extras)
        self._reservas.append(reserva)
        logger.info(f"Reserva creada: {reserva.describir()}")
        return reserva

    def resumen(self):
        lineas = ["", "========== RESUMEN DEL SISTEMA =========="]
        lineas.append(f"Clientes registrados: {len(self._clientes)}")
        lineas += [f"  - {c.describir()}" for c in self._clientes]
        lineas.append(f"Servicios creados: {len(self._servicios)}")
        lineas += [f"  - {s.describir()}" for s in self._servicios]  # cada servicio se describe distinto
        lineas.append(f"Reservas: {len(self._reservas)}")
        lineas += [f"  - {r.describir()}" for r in self._reservas]
        ingresos = sum(r.costo for r in self._reservas if r.estado == Reserva.PROCESADA)  # solo lo que se pago
        lineas.append(f"Ingresos procesados: ${ingresos:,.2f}")
        return "\n".join(lineas)
