# Software FJ

Fase 4 - Componente práctico - Programación (213023) - UNAD

Sistema de gestión de clientes, servicios y reservas para la empresa Software FJ.
Está hecho en Python con programación orientada a objetos y manejo de excepciones. No usa base de datos:
todo se guarda en listas y los errores se guardan en `logs/software_fj.log`.

## Cómo ejecutarlo

```
python main.py
```

No necesita instalar nada, solo Python 3.

## Archivos

- `excepciones.py` - excepciones propias del sistema
- `registro_logs.py` - configuración del log
- `entidad.py` - clase abstracta Entidad
- `cliente.py` - clase Cliente con validaciones
- `servicios.py` - clase abstracta Servicio + ReservaSala, AlquilerEquipo y Asesoria
- `reserva.py` - clase Reserva (confirmar, cancelar, procesar)
- `sistema.py` - gestor con las listas de clientes, servicios y reservas
- `main.py` - prueba de 25 operaciones, válidas e inválidas

## Lo que se usó

- Clases abstractas, herencia, polimorfismo y encapsulación
- "Sobrecarga" con parámetros opcionales (`calcular_costo`) y revisando el tipo de dato (`cotizar`)
- try/except, try/except/else, try/except/finally y raise ... from ...
- Archivo de logs con el módulo logging
