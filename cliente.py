# cliente.py
# Clase Cliente. Los datos son privados y se validan en los setters.

import re
from entidad import Entidad
from excepciones import DatoInvalidoError, ParametroFaltanteError


class Cliente(Entidad):
    PATRON_CORREO = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$")  # algo@algo.com
    PATRON_TELEFONO = re.compile(r"^\d{7,10}$")  # entre 7 y 10 numeros

    def __init__(self, nombre, documento, correo, telefono):
        super().__init__("CLI")
        # al asignar asi se llaman los setters de abajo y ahi se valida
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self.__nombre  # con doble guion bajo queda privado

    @nombre.setter
    def nombre(self, valor):
        if valor is None or str(valor).strip() == "":  # no puede venir vacio
            raise ParametroFaltanteError("nombre")
        valor = str(valor).strip()
        # minimo 3 letras y que no tenga numeros
        if len(valor) < 3 or not all(c.isalpha() or c.isspace() for c in valor):
            raise DatoInvalidoError("nombre", valor, "Debe tener al menos 3 letras y no contener números.")
        self.__nombre = valor.title()  # primera letra en mayuscula

    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("documento")
        valor = str(valor).strip()
        if not valor.isdigit() or not 6 <= len(valor) <= 10:  # solo numeros, de 6 a 10
            raise DatoInvalidoError("documento", valor, "Debe tener entre 6 y 10 dígitos.")
        self.__documento = valor

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not valor:
            raise ParametroFaltanteError("correo")
        if not self.PATRON_CORREO.match(str(valor)):  # reviso el formato con la expresion regular
            raise DatoInvalidoError("correo", valor, "Formato de correo incorrecto.")
        self.__correo = str(valor).lower()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if not valor:
            raise ParametroFaltanteError("telefono")
        if not self.PATRON_TELEFONO.match(str(valor)):
            raise DatoInvalidoError("telefono", valor, "Debe tener entre 7 y 10 dígitos.")
        self.__telefono = str(valor)

    def validar(self):
        # vuelvo a pasar todo por los setters por si algo cambio
        self.nombre = self.nombre
        self.documento = self.documento
        self.correo = self.correo
        self.telefono = self.telefono
        return True

    def describir(self):
        doc_oculto = "*" * (len(self.documento) - 4) + self.documento[-4:]  # solo muestro los ultimos 4 numeros
        return f"Cliente {self.id}: {self.nombre} | Doc: {doc_oculto} | {self.correo}"
