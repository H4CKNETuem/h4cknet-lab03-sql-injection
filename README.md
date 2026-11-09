# 🦊 H4CKNET · LAB 03 — SQL Injection | NEXORA

![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.4-4479A1?logo=mysql&logoColor=white)
![Python](https://img.shields.io/badge/Python-Flask-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

> **¿Serías capaz de encontrar una vulnerabilidad SQL Injection sin conocer cómo funciona la base de datos?**

**NEXORA** es una empresa ficticia con un portal interno de empleados. Tu misión es investigar su funcionamiento, identificar posibles fallos de seguridad y descubrir qué información puede quedar expuesta.

Este laboratorio forma parte del **Taller 03 de H4CKNET**, orientado a introducir la seguridad web de forma práctica y progresiva.

## 🎯 Objetivos

Al terminar el laboratorio, deberías ser capaz de:

- Entender qué es una **SQL Injection** y por qué se produce.
- Reconocer comportamientos anómalos en una aplicación web.
- Utilizar **Burp Suite** para inspeccionar y modificar peticiones HTTP.
- Comprender cómo funciona una inyección basada en `UNION SELECT`.
- Investigar la estructura de una base de datos **MySQL**.
- Distinguir entre autenticación, roles y acceso a recursos.

**No necesitas conocimientos avanzados**: basta con tener unas nociones básicas de HTTP y ganas de experimentar.

## 🧰 Requisitos

- **Docker** con el plugin **Docker Compose** (`docker compose`).
- **Python 3** para ejecutar el comprobador (recomendado).
- Un navegador web.
- **Burp Suite Community Edition** (recomendado para el taller).

El entorno está pensado para ejecutarse de forma local en **Kali Linux**, aunque también puede utilizarse en otros sistemas con Docker Compose.

## 🚀 Instalación

### 1. Descargar el laboratorio

Puedes clonar el repositorio:

```bash
git clone https://github.com/TU-USUARIO/h4cknet-lab03-sql-injection.git
cd h4cknet-lab03-sql-injection
```

> Sustituye `TU-USUARIO` por la cuenta u organización que publique el repositorio. También puedes usar **Code → Download ZIP** y descomprimirlo.

### 2. Iniciar Docker (Kali Linux)

```bash
sudo systemctl start docker
```

### 3. Levantar el laboratorio

Desde la carpeta en la que se encuentra `compose.yaml`:

```bash
sudo docker compose up --build -d
```

Comprueba que los servicios estén activos:

```bash
sudo docker compose ps
```

### 4. Verificar la instalación (opcional)

```bash
python3 comprobar_instalacion.py
```

Si todo va bien, el script mostrará:

```text
LAB 03 listo para practicar.
```

### 5. Acceder a NEXORA

Abre **http://127.0.0.1:8081** en tu navegador.

Las credenciales iniciales del empleado están disponibles en el archivo [`acceso_inicial.txt`](acceso_inicial.txt). También son:

| Campo | Valor |
|---|---|
| Usuario | `operador` |
| Contraseña | `soporte2026` |

Estas credenciales permiten explorar el portal, pero no ofrecen acceso a todas sus secciones.

> **Consejo:** puedes mantener Burp Suite en su puerto proxy habitual (`8080`). La aplicación NEXORA se abre en el `8081`.

## 🕵️ Tu misión (sin spoilers)

1. Accede al portal con las credenciales proporcionadas.
2. Explora las secciones e identifica cuáles tienen acceso restringido.
3. Investiga cómo se comportan los formularios y las búsquedas.
4. Utiliza Burp Suite para estudiar las peticiones y respuestas.
5. Trata de identificar vulnerabilidades y alcanzar los objetivos del laboratorio.

**Hay dos retos relacionados con SQL Injection.** Intenta resolverlos sin consultar el código fuente.

<details>
<summary>💡 Pista de metodología (sin soluciones)</summary>

Empieza observando cómo responde la aplicación a entradas habituales y a entradas inesperadas. Formula una hipótesis, comprueba su resultado y documenta lo que ocurre. No hace falta conocer de antemano el nombre de las tablas ni de la base de datos.

</details>

## 📁 Estructura del proyecto

```text
.
├── app/
│   ├── main.py                 # Aplicación Flask
│   ├── requirements.txt        # Dependencias de Python
│   ├── static/                 # CSS y JavaScript
│   └── templates/              # Plantillas HTML
├── db/
│   └── init/
│       └── 01_nexora.sql       # Inicialización de MySQL
├── acceso_inicial.txt          # Credenciales de acceso al laboratorio
├── comprobar_instalacion.py   # Comprobación del despliegue
├── compose.yaml               # Servicios Docker
├── Dockerfile                  # Imagen de la aplicación
├── LICENSE                    # Licencia MIT
└── README.md
```

> **Importante:** el código fuente y los datos iniciales están disponibles porque el laboratorio se distribuye para ejecutarse localmente. Si quieres practicar como si fuese una auditoría de caja negra, **no abras `app/main.py` ni `db/init/01_nexora.sql` antes de terminar los retos**.

## 🛠️ Comandos útiles

**Detener el laboratorio:**

```bash
sudo docker compose down
```

**Volver a levantarlo:**

```bash
sudo docker compose up -d
```

**Consultar los registros si algo falla:**

```bash
sudo docker compose logs --tail=60 portal
sudo docker compose logs --tail=60 db
```

**Reiniciar el laboratorio desde cero:**

```bash
sudo docker compose down -v
sudo docker compose up --build -d
```

⚠️ El comando `down -v` **elimina los volúmenes y datos almacenados por este proyecto Docker**. Úsalo únicamente si quieres reiniciar el entorno y perder su estado anterior.

## 🔒 Seguridad y alcance

Este proyecto es **deliberadamente vulnerable** y se ha creado exclusivamente para fines educativos.

- Ejecútalo **en tu propio equipo** o en un entorno de prácticas autorizado.
- **No lo publiques en Internet** ni lo utilices como aplicación real.
- La aplicación se publica en `127.0.0.1:8081` para limitar el acceso al equipo local.
- El servidor MySQL no expone directamente su puerto al anfitrión.
- El laboratorio contiene únicamente datos ficticios.

Las técnicas aprendidas deben practicarse exclusivamente en sistemas propios o con autorización expresa.

## 🦊 Sobre H4CKNET

**H4CKNET** es una iniciativa de aprendizaje práctico de ciberseguridad, enfocada en pentesting y seguridad ofensiva. Nuestros laboratorios están diseñados para aprender haciendo, empezando por los fundamentos y avanzando progresivamente.

**Taller 03 · SQL Injection — NEXORA**

## 📄 Licencia

Distribuido bajo la licencia [MIT](LICENSE). © 2026 H4CKNET.
