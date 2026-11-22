# servicios.py
# Clase abstracta Servicio y los 3 servicios que pide el ejercicio:
# ReservaSala, AlquilerEquipo y Asesoria.

from abc import abstractmethod
from entidad import Entidad
from excepciones import (DatoInvalidoError, ParametroFaltanteError,
                         CalculoInconsistenteError, ServicioNoDisponibleError)


class Servicio(Entidad):
    IVA = 0.19  # 19%

    def __init__(self, nombre, tarifa_hora):
        super().__init__("SRV")
        if not nombre or not str(nombre).strip():
            raise ParametroFaltanteError("nombre del servicio")
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:  # la tarifa tiene que ser positiva
            raise DatoInvalidoError("tarifa_hora", tarifa_hora, "Debe ser un número mayor que cero.")
        self._nombre = str(nombre).strip()
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = True  # por defecto el servicio esta disponible

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_hora(self):
        return self._tarifa_hora

    @property
    def disponible(self):
        return self._disponible

    def desactivar(self):
        self._disponible = False

    def activar(self):
        self._disponible = True

    def verificar_disponibilidad(self):
        if not self._disponible:
            raise ServicioNoDisponibleError(self._nombre)

    # estos dos los tiene que hacer cada servicio (polimorfismo)
    @abstractmethod
    def costo_base(self, horas, **extras):
        pass

    @abstractmethod
    def validar_parametros(self, horas, **extras):
        pass

    def calcular_costo(self, horas, impuesto=None, descuento=0.0, **extras):
        # "sobrecarga" con parametros opcionales, se puede llamar de varias formas:
        #   calcular_costo(3)                -> con IVA
        #   calcular_costo(3, impuesto=0)    -> sin IVA
        #   calcular_costo(3, descuento=0.1) -> con 10% de descuento
        self.validar_parametros(horas, **extras)
        if impuesto is None:  # si no mandan impuesto uso el IVA
            impuesto = self.IVA
        if not 0 <= descuento < 1:
            raise CalculoInconsistenteError(f"Descuento inválido: {descuento}. Debe estar entre 0 y 0.99.")
        if impuesto < 0:
            raise CalculoInconsistenteError(f"Impuesto negativo: {impuesto}.")
        base = self.costo_base(horas, **extras)  # cada servicio lo calcula diferente
        total = base * (1 - descuento) * (1 + impuesto)
        if total <= 0:
            raise CalculoInconsistenteError(f"El costo calculado no es válido: {total}.")
        return round(total, 2)

    def cotizar(self, datos):
        # Python no tiene sobrecarga como Java, entonces reviso el tipo de dato
        # que llega y segun eso calculo de una forma u otra
        if isinstance(datos, (int, float)):  # solo las horas
            return self.calcular_costo(datos)
        elif isinstance(datos, tuple):  # (horas, impuesto, descuento)
            horas, impuesto, descuento = (list(datos) + [None, 0.0])[:3]  # relleno si faltan valores
            return self.calcular_costo(horas, impuesto=impuesto, descuento=descuento or 0.0)
        elif isinstance(datos, dict):  # {"horas": 4, "cantidad": 3, ...}
            if "horas" not in datos:
                raise ParametroFaltanteError("horas")
            copia = dict(datos)
            horas = copia.pop("horas")
            return self.calcular_costo(horas, **copia)
        else:
            raise DatoInvalidoError("cotizar", datos, "Tipo de argumento no soportado.")

    @staticmethod
    def _validar_horas(horas, minimo, maximo):  # la uso en los 3 servicios
        if horas is None:
            raise ParametroFaltanteError("horas")
        if not isinstance(horas, (int, float)) or isinstance(horas, bool):
            raise DatoInvalidoError("horas", horas, "Debe ser numérico.")
        if not minimo <= horas <= maximo:
            raise DatoInvalidoError("horas", horas, f"Debe estar entre {minimo} y {maximo}.")

    def validar(self):
        if self._tarifa_hora <= 0:
            raise DatoInvalidoError("tarifa_hora", self._tarifa_hora)
        return True


class ReservaSala(Servicio):  # servicio 1
    def __init__(self, nombre, tarifa_hora, capacidad):
        super().__init__(nombre, tarifa_hora)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatoInvalidoError("capacidad", capacidad, "Debe ser un entero positivo.")
        self._capacidad = capacidad

    def validar_parametros(self, horas, personas=1, **extras):
        self._validar_horas(horas, 1, 12)  # una sala se reserva de 1 a 12 horas
        if personas > self._capacidad:  # no caben mas personas
            raise DatoInvalidoError("personas", personas, f"La sala admite máximo {self._capacidad}.")

    def costo_base(self, horas, personas=1, **extras):
        return self._tarifa_hora * horas

    def describir(self):
        return f"Sala '{self.nombre}' ({self.id}) - capacidad {self._capacidad} - ${self.tarifa_hora:,.0f}/h"


class AlquilerEquipo(Servicio):  # servicio 2
    SEGURO = 20000  # seguro fijo por cada alquiler

    def __init__(self, nombre, tarifa_hora, tipo_equipo, unidades):
        super().__init__(nombre, tarifa_hora)
        if not tipo_equipo:
            raise ParametroFaltanteError("tipo_equipo")
        if not isinstance(unidades, int) or unidades < 0:
            raise DatoInvalidoError("unidades", unidades, "Debe ser un entero mayor o igual a 0.")
        self._tipo_equipo = tipo_equipo
        self._unidades = unidades
        if unidades == 0:  # si no hay equipos lo dejo no disponible
            self.desactivar()

    def validar_parametros(self, horas, cantidad=1, **extras):
        self._validar_horas(horas, 1, 72)  # maximo 3 dias
        if not isinstance(cantidad, int) or cantidad < 1:
            raise DatoInvalidoError("cantidad", cantidad, "Debe ser un entero mayor que 0.")
        if cantidad > self._unidades:
            raise DatoInvalidoError("cantidad", cantidad, f"Solo hay {self._unidades} unidades.")

    def costo_base(self, horas, cantidad=1, **extras):
        return self._tarifa_hora * horas * cantidad + self.SEGURO  # tarifa x horas x cantidad + seguro

    def describir(self):
        return (f"Equipo '{self.nombre}' ({self.id}) - {self._tipo_equipo} - "
                f"{self._unidades} und. - ${self.tarifa_hora:,.0f}/h")


class Asesoria(Servicio):  # servicio 3
    MULTIPLICADORES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}  # el precio sube segun el nivel

    def __init__(self, nombre, tarifa_hora, especialidad, nivel="junior"):
        super().__init__(nombre, tarifa_hora)
        if not especialidad:
            raise ParametroFaltanteError("especialidad")
        if nivel not in self.MULTIPLICADORES:
            raise DatoInvalidoError("nivel", nivel, f"Use uno de: {list(self.MULTIPLICADORES)}.")
        self._especialidad = especialidad
        self._nivel = nivel

    def validar_parametros(self, horas, **extras):
        self._validar_horas(horas, 1, 8)  # una asesoria dura maximo 8 horas

    def costo_base(self, horas, **extras):
        return self._tarifa_hora * horas * self.MULTIPLICADORES[self._nivel]

    def describir(self):
        return (f"Asesoría '{self.nombre}' ({self.id}) - {self._especialidad} - "
                f"nivel {self._nivel} - ${self.tarifa_hora:,.0f}/h")
