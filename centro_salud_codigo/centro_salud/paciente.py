from datetime import date
from persona import Persona


class Paciente(Persona):
    def __init__(self, identificacion, nombres, annio_nac, mes_nac, dia_nac,
                 genero, direccion, codigo_postal, estrato, telefono,
                 ciudad="Giron", medico_id=""):
        super().__init__(identificacion, nombres, annio_nac, mes_nac, dia_nac,
                         genero, direccion, codigo_postal)
        self.estrato = estrato
        self.ciudad = ciudad
        self.telefono = telefono
        self.medico_id = str(medico_id)       # identificación del médico asignado

    def validar(self):
        super().validar()
        if not isinstance(self.estrato, int) or not 1 <= self.estrato <= 6:
            raise ValueError("El estrato debe ser un entero entre 1 y 6")
        if not self.ciudad.strip():
            raise ValueError("La ciudad es obligatoria")
        if not self.telefono.isdigit():
            raise ValueError("El teléfono debe contener solo dígitos")
        if self.medico_id:
            from medico import Medico
            if Medico.buscar(self.medico_id) is None:
                raise ValueError(f"No existe el médico '{self.medico_id}' en Medico.txt")

    # ---- relaciones (se resuelven leyendo los otros archivos) ----
    @property
    def medico(self):
        from medico import Medico
        return Medico.buscar(self.medico_id) if self.medico_id else None

    @property
    def citas(self):
        from cita import Cita
        return [c for c in Cita.listar() if c.paciente_id == self.identificacion]

    def cantidadCitas(self):
        return len(self.citas)

    def cantidadCitasPorMes(self, anio=None):
        """Lista de 12 posiciones (enero=0 ... diciembre=11) con las citas del año."""
        anio = anio or date.today().year
        conteo = [0] * 12
        for c in self.citas:
            if c.fecha.year == anio:
                conteo[c.fecha.month - 1] += 1
        return conteo

    def cantidadCitasPorEsp(self):
        """Lista de tuplas (especialidad, cantidad)."""
        conteo = {}
        for c in self.citas:
            medico = c.medico
            esp = medico.especialidad if medico else "Sin especialidad"
            conteo[esp] = conteo.get(esp, 0) + 1
        return sorted(conteo.items())

    # ---- persistencia ----
    def a_registro(self):
        return super().a_registro() + [self.estrato, self.telefono, self.ciudad, self.medico_id]

    @classmethod
    def desde_registro(cls, c):
        return cls(c[0], c[1], int(c[2]), int(c[3]), int(c[4]), c[5], c[6], int(c[7]),
                   int(c[8]), c[9], c[10], c[11])
