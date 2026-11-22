# entidad.py
# Clase abstracta Entidad. Cliente, Servicio y Reserva heredan de aqui.

from abc import ABC, abstractmethod
from datetime import datetime


class Entidad(ABC):  # no se puede crear un objeto Entidad directamente
    _contadores = {}  # un contador por cada prefijo (CLI, SRV, RES)

    def __init__(self, prefijo):
        Entidad._contadores[prefijo] = Entidad._contadores.get(prefijo, 0) + 1  # sumo 1 al contador
        self._id = f"{prefijo}-{Entidad._contadores[prefijo]:03d}"  # queda tipo CLI-001
        self._fecha_creacion = datetime.now()

    @property
    def id(self):  # solo lectura
        return self._id

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    @abstractmethod
    def describir(self):  # cada clase hija lo tiene que hacer
        pass

    @abstractmethod
    def validar(self):  # igual, cada hija valida sus datos
        pass

    def __str__(self):
        return self.describir()
