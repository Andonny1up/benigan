# BeniGan
    Software SAS Para la administracion de ganaderia.

## Requisitos

- Docker y Docker Compose

Para levantar sin docker

- Python > 3.13.5
- Node > 20
- POsgrest

## Instalación

Clonar el proyecto:

```bash
  git clone https://github.com/Andonny1up/benigan.git
```
Copiar y configurar el archivo .env

```bash
  cp .env.example .env
```
Levanta el proyecto y construye los contenedores asi:
```bash
  docker compose up --build
```
Para iniciar normalmente (después de la primera vez):
```bash
  docker compose up
```

## Comando útiles

### Docker
Para detener todo:
```bash
  docker compose down
```
Esto apaga y elimina los contenedores, pero no elimina volúmenes ni tu base de datos.

Si quieres borrarlo todo (base de datos incluida):

```bash
  docker compose down -v
```

### Django
Crear superusuario:
```bash
  docker compose exec web python manage.py createsuperuser
```
Aplicar migraciones manualmente:
```bash
  docker compose exec web python manage.py migrate
```
Entrar a un contenedor Django:
```bash
  docker compose exec web bash
```
### Node Tailwind
Ejecutar escucha (watch) de tailwind css:
```bash
  docker compose exec node npm run build:css
```
Entrar al contenedor Node:
```bash
  docker compose exec node bash
```
### Postgres

Entra al contenedor de PostgreSQL (Siempre que se haya configurado por defecto):
```bash
  docker compose exec db psql -U postgres
```