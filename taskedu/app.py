"""Interfaz web de TaskEdu con Flask."""
from pathlib import Path

from flask import Flask, abort, flash, redirect, render_template, request, url_for

from .service import FILTROS, ErrorValidacion, TaskService


def create_app(archivo_datos=None):
    app = Flask(__name__)
    app.secret_key = "taskedu-dev"  # solo para los mensajes flash del MVP
    datos = archivo_datos or Path(__file__).resolve().parent.parent / "data" / "tareas.json"
    servicio = TaskService(datos)

    @app.get("/")
    def index():
        filtro = request.args.get("estado", "Todas")
        if filtro not in FILTROS:
            filtro = "Todas"
        return render_template(
            "index.html",
            tareas=servicio.listar(filtro),
            filtros=list(FILTROS),
            filtro_actual=filtro,
        )

    @app.post("/tareas")
    def registrar():
        try:
            tarea = servicio.registrar(
                request.form.get("titulo"),
                request.form.get("asignatura"),
                request.form.get("fecha"),
            )
            flash(f"Tarea «{tarea.titulo}» registrada correctamente.", "ok")
        except ErrorValidacion as error:
            flash(str(error), "error")
        return redirect(url_for("index"))

    @app.post("/tareas/<int:id_tarea>/terminar")
    def terminar(id_tarea):
        try:
            servicio.terminar(id_tarea)
        except KeyError:
            abort(404)
        return redirect(url_for("index", estado=request.form.get("estado", "Todas")))

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
