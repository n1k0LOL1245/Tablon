# Tablón — mini Pinterest en Django

## Puesta en marcha
```bash
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations pins
python manage.py migrate
python manage.py createsuperuser   # opcional (para /admin/)
python manage.py runserver
```
Abre http://127.0.0.1:8000/

## Qué incluye
- Registro, login y logout (auth de Django).
- Subida de imágenes y videos (hasta 50 MB), con validación de extensión.
- Muro en columnas tipo Pinterest, búsqueda por título, orden por "Mejor puntuados".
- Puntuación de 1 a 5 estrellas: una por usuario y publicación (se puede cambiar);
  no puedes puntuar tus propias publicaciones.
- Perfil de usuario y eliminación de tus publicaciones.
