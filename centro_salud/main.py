"""Demostración del CRUD con archivos de texto para el Centro de Salud."""
import os
import shutil
from datetime import date, time

from persistencia import Persistente
from persona import Persona
from paciente import Paciente
from medico import Medico
from horario import Horario
from cita import Cita


def mostrar(titulo, objetos):
    print(f"\n--- {titulo} ---")
    for o in objetos:
        print(" ", o.a_registro())


if __name__ == "__main__":
    shutil.rmtree(Persistente.CARPETA, ignore_errors=True)

    Persona("900", "Laura Gomez", 1990, 5, 17, "F", "Calle 5 #4-10", 681001).guardar()
    Medico("101", "Carlos Rojas", 1980, 3, 12, "M", "Cra 27 #10-20", 680002,
           "Titular", "Cardiologia", 8500000).guardar()
    Horario("101", "Lun", 8).guardar()
    Horario("101", "Lun", 9, False).guardar()
    Horario("101", "Mar", 10).guardar()
    Paciente("1001", "Pedro Perez", 2000, 12, 20, "M", "Calle 30 #15-22", 681003,
             3, "3001234567", medico_id="101").guardar()
    Paciente("1002", "Maria Sanchez", 2004, 11, 1, "F", "Cra 10 #8-45", 681004,
             2, "3109876543").guardar()
    Cita("101", "1001", "Especialista", date(2026, 11, 10), time(8, 0), "204").guardar()
    Cita("101", "1002", "General", date(2026, 11, 12), time(9, 30)).guardar()

    for clase in (Persona, Medico, Horario, Paciente, Cita):
        mostrar(f"{clase.__name__}.txt", clase.listar())

    p = Paciente.buscar("1001")
    print("\nPaciente 1001:", p.nombres, "| edad:", p.calcularEdad(),
          "| mayor de edad:", p.esMayorEdad())
    print("Médico asignado:", p.medico.nombres, "| citas del paciente:", p.cantidadCitas())
    print("Citas por mes (2026):", p.cantidadCitasPorMes(2026))
    print("Citas por especialidad:", p.cantidadCitasPorEsp())
    m = Medico.buscar("101")
    print("Sueldo anual del médico:", m.CalcularSueldoAnnio())
    print("Disponibilidad Lun desde las 8:", [(h.dia, h.hora) for h in m.verificarDisponibilidad("Lun", 8)])

    p.telefono = "3205550000"
    p.estrato = 4
    p.actualizar()
    print("\nTeléfono actualizado:", Paciente.buscar("1001").telefono)

    print("Eliminar paciente 1002:", Paciente.eliminar("1002"))
    mostrar("Paciente.txt (después de editar y eliminar)", Paciente.listar())

    for intento in (
        lambda: Paciente("1001", "Repetido", 2000, 1, 1, "M", "x", 1, 3, "300").guardar(),
        lambda: Paciente("1003", "Estrato malo", 2000, 1, 1, "M", "x", 1, 9, "300").guardar(),
        lambda: Cita("101", "9999", "General").guardar(),
        lambda: Persona("901", "Fecha rara", 2001, 2, 30, "F", "x", 1).guardar(),
    ):
        try:
            intento()
        except (ValueError, KeyError) as e:
            print("Error controlado:", e)
