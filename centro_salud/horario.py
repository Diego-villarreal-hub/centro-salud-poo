from persistencia import Persistente

DIAS = ("Lun", "Mar", "Mie", "Jue", "Vie", "Sab")


class Horario(Persistente):
    def __init__(self, medico_id, dia, hora, disponibilidad=True):
        self.medico_id = str(medico_id)
        self.dia = dia
        self.hora = hora
        self.disponibilidad = disponibilidad

    def validar(self):
        from medico import Medico
        if self.dia not in DIAS:
            raise ValueError(f"El día debe ser uno de {DIAS}")
        if not isinstance(self.hora, int) or not 6 <= self.hora <= 18:
            raise ValueError("La hora debe ser un entero entre 6 y 18")
        if Medico.buscar(self.medico_id) is None:
            raise ValueError(f"No existe el médico '{self.medico_id}' en Medico.txt")

    @property
    def medico(self):
        from medico import Medico
        return Medico.buscar(self.medico_id)

    def clave(self):
        return f"{self.medico_id}-{self.dia}-{self.hora}"

    def a_registro(self):
        return [self.medico_id, self.dia, self.hora, self.disponibilidad]

    @classmethod
    def desde_registro(cls, c):
        return cls(c[0], c[1], int(c[2]), c[3] == "True")
