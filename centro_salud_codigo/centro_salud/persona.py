from datetime import date
from persistencia import Persistente


class Persona(Persistente):
    def __init__(self, identificacion, nombres, annio_nac, mes_nac, dia_nac,
                 genero, direccion, codigo_postal):
        self.identificacion = str(identificacion)
        self.nombres = nombres
        self.annio_nac = annio_nac
        self.mes_nac = mes_nac
        self.dia_nac = dia_nac
        self.genero = genero                  # "M" o "F"
        self.direccion = direccion
        self.codigo_postal = codigo_postal

    def validar(self):
        if not self.identificacion.strip():
            raise ValueError("La identificación es obligatoria")
        if not self.nombres.strip():
            raise ValueError("Los nombres son obligatorios")
        if self.genero not in ("M", "F"):
            raise ValueError("El género debe ser 'M' o 'F'")
        date(self.annio_nac, self.mes_nac, self.dia_nac)   # lanza ValueError si la fecha no existe
        if not isinstance(self.codigo_postal, int):
            raise ValueError("El código postal debe ser un entero")

    def calcularEdad(self):
        hoy = date.today()
        edad = hoy.year - self.annio_nac
        if (hoy.month, hoy.day) < (self.mes_nac, self.dia_nac):
            edad -= 1
        return edad

    def cantidadCitas(self):
        return 0                              # las subclases lo sobrescriben

    def esMayorEdad(self):
        return self.calcularEdad() >= 18

    # ---- persistencia ----
    def clave(self):
        return self.identificacion

    def a_registro(self):
        return [self.identificacion, self.nombres, self.annio_nac, self.mes_nac,
                self.dia_nac, self.genero, self.direccion, self.codigo_postal]

    @classmethod
    def desde_registro(cls, c):
        return cls(c[0], c[1], int(c[2]), int(c[3]), int(c[4]), c[5], c[6], int(c[7]))
