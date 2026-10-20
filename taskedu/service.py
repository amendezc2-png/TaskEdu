"""Lógica de negocio de TaskEdu: registrar, consultar, cambiar estado y filtrar tareas."""
import json
from dataclasses import dataclass, asdict
from datetime import date
from pathlib import Path

PENDIENTE = "Pendiente"
TERMINADA = "Terminada"

FILTROS = {
    "Todas": None,
    "Pendientes": PENDIENTE,
    "Terminadas": TERMINADA,
}


class ErrorValidacion(ValueError):
    """Se lanza cuando los datos de una tarea no cumplen los criterios de aceptación."""


@dataclass
class Tarea:
    id: int
    titulo: str
    asignatura: str
    fecha: str  # formato AAAA-MM-DD
    estado: str = PENDIENTE


def _validar_campo(valor, nombre):
    """Devuelve el texto sin espacios sobrantes o lanza error si queda vacío."""
    limpio = (valor or "").strip()
    if not limpio:
        raise ErrorValidacion(f"El campo {nombre} no puede estar vacío.")
    return limpio


def _validar_fecha(valor):
    texto = _validar_campo(valor, "fecha")
    try:
        date.fromisoformat(texto)
    except ValueError:
        raise ErrorValidacion("La fecha debe tener el formato AAAA-MM-DD.")
    return texto


class TaskService:
    """Gestiona las tareas y las guarda en un archivo JSON para que el estado se conserve."""

    def __init__(self, archivo):
        self.archivo = Path(archivo)
        self._tareas = self._cargar()

    # ---------- persistencia ----------
    def _cargar(self):
        if not self.archivo.exists():
            return []
        with self.archivo.open(encoding="utf-8") as f:
            return [Tarea(**datos) for datos in json.load(f)]

    def _guardar(self):
        self.archivo.parent.mkdir(parents=True, exist_ok=True)
        with self.archivo.open("w", encoding="utf-8") as f:
            json.dump([asdict(t) for t in self._tareas], f, ensure_ascii=False, indent=2)

    # ---------- HU-01: registrar ----------
    def registrar(self, titulo, asignatura, fecha):
        tarea = Tarea(
            id=max((t.id for t in self._tareas), default=0) + 1,
            titulo=_validar_campo(titulo, "título"),
            asignatura=_validar_campo(asignatura, "asignatura"),
            fecha=_validar_fecha(fecha),
        )
        self._tareas.append(tarea)
        self._guardar()
        return tarea

    # ---------- HU-02 y HU-04: consultar y filtrar ----------
    def listar(self, filtro="Todas"):
        if filtro not in FILTROS:
            raise ErrorValidacion("Filtro no válido. Usa Todas, Pendientes o Terminadas.")
        estado = FILTROS[filtro]
        tareas = [t for t in self._tareas if estado is None or t.estado == estado]
        return sorted(tareas, key=lambda t: (t.fecha, t.id))

    # ---------- HU-03: cambiar estado ----------
    def _buscar(self, id_tarea):
        for tarea in self._tareas:
            if tarea.id == id_tarea:
                return tarea
        raise KeyError(f"No existe la tarea {id_tarea}.")

    def terminar(self, id_tarea):
        tarea = self._buscar(id_tarea)
        tarea.estado = TERMINADA
        self._guardar()
        return tarea
