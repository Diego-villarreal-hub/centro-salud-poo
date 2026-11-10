from persona import Persona

TIPOS_MEDICO = ("Titular", "Interino", "Sustituto")


class Medico(Persona):
    def __init__(self, identificacion, nombres, annio_nac, mes_nac, dia_nac,
                 genero, direccion, codigo_postal, tipoMedico, especialidad, sueldo):
        super().__init__(identificacion, nombres, annio_nac, mes_nac, dia_nac,
                         genero, direccion, codigo_postal)
        self.tipoMedico = tipoMedico
        self.especialidad = especialidad
        self.sueldo = float(sueldo)

    def validar(self):
        super().validar()
        if self.tipoMedico not in TIPOS_MEDICO:
            raise ValueError(f"El tipo de médico debe ser uno de {TIPOS_MEDICO}")
        if not self.especialidad.strip():
            raise ValueError("La especialidad es obligatoria")
        if self.sueldo <= 0:
            raise ValueError("El sueldo debe ser mayor que cero")

    @property
    def citas(self):
        from cita import Cita
        return [c for c in Cita.listar() if c.medico_id == self.identificacion]

    def CalcularSueldoAnnio(self):
        return self.sueldo * 12

    def cantidadCitas(self):
        return len(self.citas)

    def verificarDisponibilidad(self, dia, hora):
        """Horarios libres del médico ese día, desde la hora indicada en adelante."""
        from horario import Horario
        libres = [h for h in Horario.listar()
                  if h.medico_id == self.identificacion and h.dia == dia
                  and h.hora >= hora and h.disponibilidad]
        return sorted(libres, key=lambda h: h.hora)

    def a_registro(self):
        return super().a_registro() + [self.tipoMedico, self.especialidad, self.sueldo]

    @classmethod
    def desde_registro(cls, c):
        return cls(c[0], c[1], int(c[2]), int(c[3]), int(c[4]), c[5], c[6], int(c[7]),
                   c[8], c[9], float(c[10]))
