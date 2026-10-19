"""Prueba de aceptación: recorre los criterios de HU-01 a HU-04 como lo haría un estudiante."""
from taskedu.app import create_app


def test_flujo_completo_del_estudiante(tmp_path):
    cliente = create_app(tmp_path / "tareas.json").test_client()

    # HU-02: sin tareas, mensaje informativo
    pagina = cliente.get("/").get_data(as_text=True)
    assert "No hay tareas para mostrar" in pagina

    # HU-01: título vacío no se acepta
    respuesta = cliente.post(
        "/tareas",
        data={"titulo": "", "asignatura": "Cálculo", "fecha": "2026-11-04"},
        follow_redirects=True,
    ).get_data(as_text=True)
    assert "no puede estar vacío" in respuesta

    # HU-01: registro válido muestra confirmación
    respuesta = cliente.post(
        "/tareas",
        data={"titulo": "Taller de límites", "asignatura": "Cálculo", "fecha": "2026-11-04"},
        follow_redirects=True,
    ).get_data(as_text=True)
    assert "registrada correctamente" in respuesta

    cliente.post("/tareas", data={"titulo": "Quiz POO", "asignatura": "POO", "fecha": "2026-11-06"})

    # HU-02: cada tarea muestra asignatura, fecha y estado
    pagina = cliente.get("/").get_data(as_text=True)
    assert "Cálculo" in pagina and "2026-11-04" in pagina and "Estado: Pendiente" in pagina

    # HU-03: marcar como terminada y verlo de inmediato
    respuesta = cliente.post("/tareas/1/terminar", follow_redirects=True).get_data(as_text=True)
    assert "Estado: Terminada" in respuesta

    # HU-04: el filtro devuelve solo lo que corresponde
    pendientes = cliente.get("/?estado=Pendientes").get_data(as_text=True)
    assert "Quiz POO" in pendientes and "Taller de límites" not in pendientes
    terminadas = cliente.get("/?estado=Terminadas").get_data(as_text=True)
    assert "Taller de límites" in terminadas and "Quiz POO" not in terminadas
