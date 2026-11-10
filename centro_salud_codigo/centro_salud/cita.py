from datetime import date, datetime
from persistencia import Persistente

TIPOS_CITA = ("General", "Odontología", "Especialista")


class Cita(Persistente):
    def __init__(self, medico_id, paciente_id, tipo="General", fecha=None,
                 hora=None, numConsultorio="NA"):
        self.medico_id = str(medico_id)
        self.paciente_id = str(paciente_id)
        self.tipo = tipo
        self.fecha = fecha or date.today()                                  # por defecto: hoy
        self.hora = hora or datetime.now().time().replace(second=0, microsecond=0)  # por defecto: ahora
        self.numConsultorio = str(numConsultorio)

    def validar(self):
        from medico import Medico
        from paciente import Paciente
        if self.tipo not in TIPOS_CITA:
            raise ValueError(f"El tipo de cita debe ser uno de {TIPOS_CITA}")
        if Medico.buscar(self.medico_id) is None:
            raise ValueError(f"No existe el médico '{self.medico_id}' en Medico.txt")
        if Paciente.buscar(self.paciente_id) is None:
            raise ValueError(f"No existe el paciente '{self.paciente_id}' en Paciente.txt")

    def consultarMedico(self):
        from medico import Medico
        return Medico.buscar(self.medico_id)

    def consultarPaciente(self):
        from paciente import Paciente
        return Paciente.buscar(self.paciente_id)

    @property
    def medico(self):
        return self.consultarMedico()

    @property
    def paciente(self):
        return self.consultarPaciente()

    # ---- persistencia ----
    def clave(self):
        # Un médico no puede tener dos citas el mismo día a la misma hora
        return f"{self.medico_id}-{self.fecha.isoformat()}-{self.hora.strftime('%H:%M')}"

    def a_registro(self):
        return [self.medico_id, self.paciente_id, self.tipo,
                self.fecha.isoformat(), self.hora.strftime("%H:%M"), self.numConsultorio]

    @classmethod
    def desde_registro(cls, c):
        return cls(c[0], c[1], c[2], date.fromisoformat(c[3]),
                   datetime.strptime(c[4], "%H:%M").time(), c[5])
