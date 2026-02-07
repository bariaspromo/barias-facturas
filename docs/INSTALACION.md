# 📘 Guía de Instalación - Barias ERP

Esta guía detalla los pasos necesarios para instalar y configurar el sistema Barias ERP en diferentes entornos.

---

## 📋 Requisitos del Sistema

### Requisitos Mínimos

- **Sistema Operativo:** Linux (Ubuntu 20.04+), macOS, o Windows con WSL2
- **RAM:** 4 GB mínimo (8 GB recomendado)
- **Disco:** 20 GB de espacio libre
- **Procesador:** 2 núcleos (4 núcleos recomendado)

### Software Requerido

- **Docker:** 20.10 o superior
- **Docker Compose:** 2.0 o superior
- **Git:** 2.30 o superior

### Requisitos Opcionales (Desarrollo)

- **Python:** 3.11+
- **Node.js:** 20+
- **PostgreSQL:** 16+ (si no usa Docker)

---

## 🚀 Instalación con Docker (Recomendado)

### 1. Clonar el Repositorio

```bash
git clone https://github.com/bariaspromo/barias-facturas.git
cd barias-facturas
```

### 2. Configurar Variables de Entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar el archivo .env con tus configuraciones
nano .env
```

**Variables importantes a configurar:**

```env
# Base de datos
DB_PASSWORD=tu_contraseña_segura

# Django
SECRET_KEY=tu_clave_secreta_django
DEBUG=False  # True solo en desarrollo

# DGII
DGII_ENV=test  # o 'production' en producción
DGII_RNC=tu_rnc_de_empresa
DGII_CERT_PATH=/certs/tu_certificado.p12
DGII_CERT_PASSWORD=contraseña_del_certificado
```

### 3. Iniciar los Servicios

```bash
# Construir e iniciar todos los contenedores
docker-compose up -d

# Ver los logs
docker-compose logs -f
```

### 4. Ejecutar Migraciones

```bash
# Ejecutar migraciones de base de datos
docker-compose exec backend python manage.py migrate

# Crear datos iniciales (opcional)
docker-compose exec backend python manage.py loaddata initial_data
```

### 5. Crear Superusuario

```bash
docker-compose exec backend python manage.py createsuperuser
```

Sigue las instrucciones en pantalla para crear el usuario administrador.

### 6. Acceder a la Aplicación

- **Frontend:** http://localhost:3000
- **Admin Django:** http://localhost:8000/admin
- **API:** http://localhost:8000/api
- **API Docs:** http://localhost:8000/api/docs

---

## 💻 Instalación Manual (Sin Docker)

### 1. Instalar PostgreSQL

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# macOS con Homebrew
brew install postgresql@16
```

### 2. Crear Base de Datos

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE barias_erp;
CREATE USER barias WITH PASSWORD 'tu_contraseña';
ALTER ROLE barias SET client_encoding TO 'utf8';
ALTER ROLE barias SET default_transaction_isolation TO 'read committed';
ALTER ROLE barias SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE barias_erp TO barias;
\q
```

### 3. Instalar Redis

```bash
# Ubuntu/Debian
sudo apt install redis-server

# macOS con Homebrew
brew install redis

# Iniciar Redis
sudo systemctl start redis  # Linux
brew services start redis   # macOS
```

### 4. Configurar Backend (Python/Django)

```bash
cd backend

# Crear entorno virtual
python3.11 -m venv venv
source venv/bin/activate  # Linux/macOS
# o
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Copiar y configurar .env
cp ../.env.example ../.env
# Editar .env con tus configuraciones

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Iniciar servidor de desarrollo
python manage.py runserver
```

### 5. Configurar Frontend (React/Next.js)

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

### 6. Iniciar Celery (Tareas Asíncronas)

```bash
cd backend

# Worker
celery -A core worker -l info

# Beat (en otra terminal)
celery -A core beat -l info
```

---

## 🔧 Configuración Adicional

### Certificado Digital DGII

Para facturación electrónica, necesitas un certificado digital:

1. Solicita tu certificado en la DGII
2. Descarga el archivo `.p12`
3. Colócalo en la carpeta `certs/` (crear si no existe)
4. Configura la ruta en `.env`:

```env
DGII_CERT_PATH=/ruta/a/tu/certificado.p12
DGII_CERT_PASSWORD=tu_contraseña
```

### Configuración de Email

Para enviar facturas por email:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_contraseña_o_app_password
```

### WhatsApp (Opcional)

Para notificaciones por WhatsApp:

```env
WHATSAPP_API_KEY=tu_api_key
WHATSAPP_PHONE_NUMBER=tu_numero
```

---

## 🧪 Verificar Instalación

### Verificar Backend

```bash
# Con Docker
docker-compose exec backend python manage.py check

# Sin Docker
python manage.py check
```

### Ejecutar Tests

```bash
# Backend
docker-compose exec backend pytest

# Frontend
docker-compose exec frontend npm test
```

---

## 🔄 Actualizar el Sistema

```bash
# Detener servicios
docker-compose down

# Actualizar código
git pull origin main

# Reconstruir contenedores
docker-compose build

# Iniciar servicios
docker-compose up -d

# Ejecutar nuevas migraciones
docker-compose exec backend python manage.py migrate

# Limpiar archivos estáticos (si es necesario)
docker-compose exec backend python manage.py collectstatic --noinput
```

---

## 🛠️ Solución de Problemas

### El backend no inicia

```bash
# Ver logs
docker-compose logs backend

# Verificar conexión a base de datos
docker-compose exec backend python manage.py dbshell
```

### Error de permisos en archivos

```bash
# Dar permisos al directorio
sudo chown -R $USER:$USER .
```

### Puerto ya en uso

```bash
# Cambiar puertos en docker-compose.yml
# Ejemplo: "3001:3000" en lugar de "3000:3000"
```

### Base de datos no conecta

```bash
# Verificar que PostgreSQL esté corriendo
docker-compose ps
docker-compose logs db
```

---

## 📞 Soporte

Si encuentras problemas durante la instalación:

- 🐛 [Reportar un issue](https://github.com/bariaspromo/barias-facturas/issues)
- 📖 [Ver la documentación completa](https://github.com/bariaspromo/barias-facturas/wiki)
- 📧 Email: support@bariaserp.com

---

**¡Felicidades! Tu instalación de Barias ERP está lista. 🎉**
