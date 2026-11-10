"""NEXORA — LAB03 SQL Injection sobre MySQL 8.4.

Aplicación deliberadamente vulnerable. Uso educativo SOLO en localhost.
Las dos consultas inseguras están señaladas como parte del laboratorio.
"""
import hashlib
import os
from functools import wraps

import pymysql
from pymysql.cursors import DictCursor
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.getenv("LAB_SESSION_SECRET", "solo-ejercicio-local"),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)
FLAG_ADMIN = "H4CKNET{SQLI_ADMIN_NEXORA}"


def digest(password: str) -> str:
    # SHA-256 aquí sirve para mantener simple el ejercicio. NO usar para contraseñas reales.
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def clean_text(value):
    """Repara datos de un volumen antiguo importado con el charset equivocado.

    Una base de datos nueva se inicializa con UTF-8 real mediante CONVERT.
    """
    if not isinstance(value, str) or not any(t in value for t in ("Ã", "Â")):
        return value
    try:
        return value.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return value


def clean_row(row):
    if row is None:
        return None
    return {key: clean_text(value) for key, value in row.items()}


def db():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("DB_NAME", "nexora"),
        user=os.getenv("DB_USER", "nexora_app"),
        password=os.getenv("DB_PASSWORD", ""),
        charset="utf8mb4",
        cursorclass=DictCursor,
        connect_timeout=5,
        read_timeout=5,
        autocommit=True,
    )


@app.after_request
def headers(response):
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response


def login_required(handler):
    @wraps(handler)
    def guarded(*args, **kwargs):
        if not session.get("usuario"):
            return redirect(url_for("login"))
        return handler(*args, **kwargs)
    return guarded


@app.route("/")
def index():
    return redirect(url_for("inicio") if session.get("usuario") else url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        usuario = request.form.get("usuario", "")[:150]
        password = request.form.get("password", "")[:150]
        password_hash = digest(password)
        try:
            with db() as connection:
                with connection.cursor() as cursor:
                    # SQLi INTENCIONAL: concatenación insegura. Solo para el laboratorio.
                    query = (
                        f"SELECT id, usuario, nombre, rol FROM empleados "
                        f"WHERE usuario = '{usuario}' AND password_hash = '{password_hash}'"
                    )
                    cursor.execute(query)
                    row = clean_row(cursor.fetchone())
        except pymysql.MySQLError as exc:
            # Laboratorio: mostramos una pista cuando la entrada rompe la sintaxis SQL.
            # 1064 es el código de MySQL para errores de sintaxis.
            if exc.args and exc.args[0] == 1064:
                return render_template(
                    "login.html",
                    error="Error SQL (1064): la consulta tiene un error de sintaxis.",
                    title="Acceso de empleados",
                ), 500
            app.logger.exception("Error de base de datos durante el inicio de sesión")
            return render_template(
                "login.html",
                error="No se ha podido procesar la solicitud.",
                title="Acceso de empleados",
            ), 500

        if row:
            session.clear()
            session.update(id=row["id"], usuario=row["usuario"], nombre=row["nombre"], rol=row["rol"])
            return redirect(url_for("inicio"))
        error = "No hemos podido validar las credenciales."
    return render_template("login.html", error=error, title="Acceso de empleados")


@app.route("/salir")
def salir():
    session.clear()
    return redirect(url_for("login"))


@app.route("/inicio")
@login_required
def inicio():
    with db() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS n FROM incidencias")
            count = cursor.fetchone()["n"]
            cursor.execute("SELECT COUNT(*) AS n FROM incidencias WHERE estado = %s", ("Abierta",))
            open_count = cursor.fetchone()["n"]
    return render_template("inicio.html", title="Panel de trabajo", total=count, abiertas=open_count)


@app.route("/incidencias")
@login_required
def incidencias():
    with db() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, asunto, area, estado FROM incidencias ORDER BY id DESC LIMIT 8")
            rows = [clean_row(r) for r in cursor.fetchall()]
    return render_template("incidencias.html", title="Incidencias", rows=rows)


@app.route("/incidencias/buscar", methods=["POST"])
@login_required
def buscar_incidencias():
    termino = request.form.get("buscar", "")[:250]
    try:
        with db() as connection:
            with connection.cursor() as cursor:
                # SQLi INTENCIONAL: no parametrizar este WHERE en el laboratorio.
                query = (
                    "SELECT id, asunto, area, estado FROM incidencias "
                    f"WHERE asunto LIKE '%{termino}%' ORDER BY id DESC LIMIT 30"
                )
                cursor.execute(query)
                rows = [clean_row(r) for r in cursor.fetchall()]
        return render_template("partials/resultados.html", rows=rows)
    except pymysql.MySQLError:
        return '<p class="notice error">No se pudo completar la búsqueda.</p>', 500


@app.route("/documentacion")
@login_required
def documentacion():
    return render_template("documentacion.html", title="Documentación")


@app.route("/equipo")
@login_required
def equipo():
    return render_template("equipo.html", title="Equipo")


@app.route("/direccion")
@login_required
def direccion():
    if session.get("rol") != "direccion":
        return render_template("prohibido.html", title="Acceso restringido"), 403
    return render_template("direccion.html", title="Dirección", flag=FLAG_ADMIN)
