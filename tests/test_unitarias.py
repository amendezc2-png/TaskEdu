"""Pruebas unitarias del servicio (HU-01, HU-02, HU-03, HU-04)."""
import pytest

from taskedu.service import ErrorValidacion, PENDIENTE, TERMINADA, TaskService


@pytest.fixture
def servicio(tmp_path):
    return TaskService(tmp_path / "tareas.json")


def test_registrar_tarea_valida(servicio):
    tarea = servicio.registrar("Taller de SQL", "Bases de Datos I", "2026-11-03")
    assert tarea.id == 1
    assert tarea.estado == PENDIENTE


@pytest.mark.parametrize("titulo", ["", "   ", None])
def test_no_acepta_titulo_vacio(servicio, titulo):
    with pytest.raises(ErrorValidacion):
        servicio.registrar(titulo, "Cálculo", "2026-11-03")
    assert servicio.listar() == []


def test_terminar_cambia_el_estado(servicio):
    tarea = servicio.registrar("Informe", "Requisitos", "2026-11-10")
    servicio.terminar(tarea.id)
    assert servicio.listar()[0].estado == TERMINADA


def test_filtrar_por_estado(servicio):
    a = servicio.registrar("A", "Física", "2026-11-01")
    servicio.registrar("B", "Física", "2026-11-02")
    servicio.terminar(a.id)
    assert [t.titulo for t in servicio.listar("Pendientes")] == ["B"]
    assert [t.titulo for t in servicio.listar("Terminadas")] == ["A"]
    assert len(servicio.listar("Todas")) == 2


def test_fecha_invalida_se_rechaza(servicio):
    with pytest.raises(ErrorValidacion):
        servicio.registrar("Tarea", "POO", "03/11/2026")
