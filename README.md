# Prueba Técnica – Backend Developer en Area101

Este proyecto es una API RESTful desarrollada para gestionar sesiones presenciales de eventos o talleres, permitiendo a los usuarios consultar, reservar y cancelar su asistencia. Está construida con una arquitectura modular y escalable, siguiendo buenas prácticas de desarrollo backend y ofreciendo documentación interactiva para facilitar su consumo.


## 🚀 Tecnologías utilizadas

- **Python 3.10+** – Lenguaje de programación principal.
- **Django 5.2** – Framework web robusto para desarrollo backend.
- **Django REST Framework** – Construcción de APIs RESTful.
- **drf-spectacular** – Generación automática de documentación (OpenAPI).
- **PostgreSQL** – Base de datos relacional para persistencia de datos.
- **Gunicorn** – Servidor WSGI usado en el despliegue.
- **django-environ** – Gestión de variables de entorno desde `.env`.
- **psycopg2-binary** – Driver PostgreSQL para Python.
- **Git & GitHub** – Control de versiones.

## ⚙️ Instalación
Puedes acceder a la API a través de este enlace:

- https://area101-prueba-backend.onrender.com/

O si prefieres ejecutarlo en local, sigue estos pasos:

1. Clona el repositorio en la carpeta que desees:
```
git clone https://github.com/SergioLM7/back-django-area101/
```
2. Navega al directorio del proyecto:
```
cd area101_prueba_backend
```
3. Asegúrate de tener instalado Python 3.8 o superior.  

4. Crea un entorno virtual y actívalo:
```
python -m venv env
source env/Scripts/activate   # En Windows Git Bash
env/Scripts/activate          # En Windows PowerShell / CMD
source env/bin/activate       # En MacOS y Linux

```
5. Instala las dependencias:
```
pip install -r requirements.txt
```
6. Crea el archivo `.env` con las variables necesarias.
```
DEBUG=
SECRET_KEY=

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_SSLMODE=
```
7. Aplica las migraciones a la base de datos:
```
python manage.py migrate
```
8. Ejecuta el servidor:

```
python manage.py runserver
```

## 🔧 Funcionalidades principales

### - Listar sesiones activas
`GET /api/sessions/` / `GET /api/sessions/?page=1`    
Devuelve únicamente las sesiones con plazas disponibles, con paginación por parámetro page en la URL.

La respuesta incluye los campos count, next, previous y results con las sesiones de la página actual.

### - Ver detalle de una sesión
`GET /api/sessions/<id>/`  
Muestra la información completa de la sesión, incluyendo reservas.

### - Reservar una plaza
`POST /api/sessions/<id>/reserve/`  
Permite reservar una plaza si hay disponibilidad.  
Evita duplicados por email y controla el overbooking.

### - Cancelar una reserva
`POST /api/sessions/<id>/cancel/`  
Cancela una reserva existente mediante el correo electrónico.

## 🗃️ Estructura de datos

### Modelo `Session`
- `title`: título de la sesión.
- `description`: descripción general.
- `start_time`, `end_time`: fechas de inicio y fin.
- `capacity`: número máximo de plazas.
- `available_slots`: propiedad calculada y cacheada (20s) para rendimiento.

### Modelo `Reservation`
- `session`: relación con una sesión.
- `name`, `email`: información del usuario.
- `created_at`: fecha de creación.
- Restricción de unicidad por `session + email` para evitar duplicados.

## 🧠 Lógica y rendimiento

- Uso de **anotaciones y `prefetch_related`** para optimizar consultas.
- Uso de **caché en memoria (`LocMemCache`)** para reducir accesos a base de datos en:
  - Conteo de plazas disponibles.
  - Detalles de sesión.
- La caché se invalida automáticamente al crear o cancelar reservas.

## ✅ Testing

El proyecto cuenta con una batería de pruebas automatizadas utilizando `APITestCase`, proporcionado por **Django REST Framework**, que extiende las capacidades de testing de Django para facilitar pruebas sobre endpoints RESTful.

Las pruebas cubren los principales flujos de negocio:

- ✅ Reserva exitosa (flujo principal).
- 🚫 Prevención de reservas duplicadas por email.
- 🚫 Control de overbooking (cuando se superan las plazas disponibles).
- 🚫 Validación de datos obligatorios.
- ✅ Cancelación de reservas correctamente procesada.

Estas pruebas aseguran la consistencia de la lógica de negocio, la gestión de plazas y los mensajes de error.

**Ubicación del archivo de pruebas:**  
area101_prueba_backend/community_sessions/tests.py

**Para probar los tests:**
```
python manage.py test
```

## 📫 Recursos adicionales

- [Colección de Postman para pruebas de API](./readme/Area101.postman_collection.json)


## 📂 Estructura general del código

- `models.py`: definición de `Session` y `Reservation`.
- `views.py`: lógica de negocio, caché, validaciones y acciones personalizadas.
- `serializers.py`: validación y transformación de datos.
- `urls.py`: enrutamiento de endpoints API.
