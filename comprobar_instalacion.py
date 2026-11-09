#!/usr/bin/env python3
"""Comprueba el despliegue de NEXORA desde el anfitrión. No revela la solución."""
from urllib.request import build_opener, HTTPCookieProcessor, Request
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError
from http.cookiejar import CookieJar
import sys

BASE = "http://127.0.0.1:8081"
opener = build_opener(HTTPCookieProcessor(CookieJar()))

def check(path, values=None):
    data = urlencode(values).encode("utf-8") if values is not None else None
    req = Request(BASE+path, data=data)
    try:
        with opener.open(req, timeout=12) as r:
            return r.status, r.read().decode("utf-8", errors="replace")
    except HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")

try:
    code, body = check("/login")
    assert code == 200 and "Iniciar sesión" in body, "No carga el login"
    print("[OK] Página de acceso")
    code, body = check("/login", {"usuario":"inexistente", "password":"prueba"})
    assert code == 200 and "No hemos podido validar las credenciales" in body, "Fallo del mensaje de credenciales incorrectas"
    print("[OK] Credenciales incorrectas: aviso normal")
    code, body = check("/login", {"usuario":"'", "password":"prueba"})
    assert code == 500 and "Error SQL (1064)" in body, "Fallo del aviso de sintaxis SQL en el login"
    print("[OK] Comilla simple en login: error SQL 1064 visible")
    code, body = check("/login", {"usuario":"operador", "password":"soporte2026"})
    assert code == 200 and "Buenos días" in body, "El login no funciona"
    print("[OK] Inicio de sesión con operador")
    code, body = check("/direccion")
    assert code == 403, "La sección Dirección no está restringida"
    print("[OK] Acceso restringido a Dirección")
    code, body = check("/incidencias")
    assert code == 200, "No carga incidencias"
    assert "Recepción" in body and "conexión" in body and "Administración" in body, "Las tildes no se muestran correctamente"
    assert "RecepciÃ" not in body and "AdministraciÃ" not in body, "Persisten caracteres dañados"
    print("[OK] Tildes: Recepción, conexión y Administración")
    code, body = check("/incidencias/buscar", {"buscar":"impresora"})
    assert code == 200 and "Impresora" in body, "No funciona el buscador"
    print("[OK] Buscador de incidencias")
    print("\nLAB 03 listo para practicar.")
except (AssertionError, URLError, TimeoutError) as exc:
    print("[ERROR]", exc)
    print("Revisa: sudo docker compose logs --tail=60 portal")
    sys.exit(1)
