"""Prueba de integración: interfaz web + servicio + archivo JSON."""
from taskedu.app import create_app
from taskedu.service import TaskService


def test_registrar_y_terminar_se_guarda_en_disco(tmp_path):
    archivo = tmp_path / "tareas.json"
    cliente = create_app(archivo).test_client()

    cliente.post("/tareas", data={"titulo": "Parcial", "asignatura": "Física", "fecha": "2026-11-05"})
    cliente.post("/tareas/1/terminar")

    # Se reconstruye el servicio desde cero para comprobar que el estado se conservó
    recargado = TaskService(archivo)
    tareas = recargado.listar()
    assert len(tareas) == 1
    assert tareas[0].estado == "Terminada"
