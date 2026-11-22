# excepciones.py
# Aqui van las excepciones propias del sistema Software FJ.
# Todas heredan de SoftwareFJError para poder atraparlas todas juntas si hace falta.


class SoftwareFJError(Exception):  # excepcion general del sistema
    def __init__(self, mensaje, codigo="ERR-GENERAL"):
        super().__init__(mensaje)  # le paso el mensaje a Exception
        self.codigo = codigo  # codigo para saber que tipo de error es

    def __str__(self):
        return f"[{self.codigo}] {self.args[0]}"  # asi se ve el error cuando se imprime


class DatoInvalidoError(SoftwareFJError):  # cuando un dato esta mal (correo, horas, etc.)
    def __init__(self, campo, valor, detalle=""):
        mensaje = f"Dato inválido en '{campo}': {valor!r}. {detalle}".strip()  # armo el mensaje
        super().__init__(mensaje, "ERR-DATO")
        self.campo = campo  # guardo cual campo fallo


class ParametroFaltanteError(SoftwareFJError):  # cuando no mandan un dato obligatorio
    def __init__(self, parametro):
        super().__init__(f"Falta el parámetro obligatorio '{parametro}'.", "ERR-PARAM")
        self.parametro = parametro


class ServicioNoDisponibleError(SoftwareFJError):  # servicio inactivo o que no existe
    def __init__(self, nombre_servicio):
        super().__init__(f"El servicio '{nombre_servicio}' no está disponible.", "ERR-SERV")


class ReservaInvalidaError(SoftwareFJError):  # problemas con una reserva
    def __init__(self, mensaje):
        super().__init__(mensaje, "ERR-RESERVA")


class OperacionNoPermitidaError(SoftwareFJError):  # ej: cancelar algo que ya estaba cancelado
    def __init__(self, mensaje):
        super().__init__(mensaje, "ERR-OPERACION")


class CalculoInconsistenteError(SoftwareFJError):  # cuando un calculo da algo raro (descuento > 100%)
    def __init__(self, mensaje):
        super().__init__(mensaje, "ERR-CALCULO")


class ClienteDuplicadoError(SoftwareFJError):  # cliente con documento repetido
    def __init__(self, documento):
        super().__init__(f"Ya existe un cliente con documento {documento}.", "ERR-DUPLICADO")
