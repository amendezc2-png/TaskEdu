# TaskEdu

Gestor de tareas académicas (producto mínimo viable) hecho con Python y Flask.

## Cómo ejecutarlo

```bash
python -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m taskedu.app
```

Abre http://127.0.0.1:5000 en el navegador.

## Pruebas

```bash
python -m pytest -v
```

- `tests/test_unitarias.py`: pruebas unitarias del servicio.
- `tests/test_integracion.py`: interfaz web + servicio + archivo JSON.
- `tests/test_aceptacion.py`: recorre los criterios de aceptación de HU-01 a HU-04.

## Historias implementadas

| Historia | Qué hace |
|----------|----------|
| HU-01 | Registrar tarea (título, asignatura y fecha; rechaza título vacío; muestra confirmación) |
| HU-02 | Consultar tareas (asignatura, fecha y estado; mensaje si no hay tareas) |
| HU-03 | Marcar como terminada (se guarda en `data/tareas.json`) |
| HU-04 | Filtrar por Todas, Pendientes o Terminadas |

## Flujo de ramas sugerido

`main` protegida y una rama por historia: `feature/HU-01`, `feature/HU-02`, `feature/HU-03`, `feature/HU-04`. Cada una se integra con pull request revisado por otro integrante.

## Integración continua

El workflow `.github/workflows/ci.yml` descarga el código, instala dependencias y ejecuta las pruebas en cada push y pull request a `main`.
