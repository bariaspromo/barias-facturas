# 📋 PROMPT ORIGINAL COMPLETO - Barias ERP

## Especificación Completa del Sistema

Este documento contiene el prompt y especificaciones originales completas utilizadas para crear el sistema Barias ERP.

---

## 🏢 Descripción General del Proyecto

**Nombre del Proyecto:** Barias ERP - Sistema Integral de Gestión para Restaurantes, Bares y Licor Stores

**Objetivo:** Crear un sistema ERP completo, moderno e inteligente para la gestión integral de **restaurantes, bares y licor stores** en **República Dominicana**, cumpliendo con la normativa fiscal de la **DGII** (Dirección General de Impuestos Internos).

**Alcance:** El sistema debe cubrir:
- POS/punto de venta
- Facturación electrónica (e-CF)
- Contabilidad
- Inventario
- Pedidos
- Auto-pedido (self-ordering)
- Gestión de bebidas/licores
- Reportes y analíticas
- Inteligencia Artificial

---

## 🏗️ Arquitectura del Proyecto

### Stack Tecnológico Requerido

| Componente | Tecnología |
|-----------|-----------|
| **Backend** | Python (Django/FastAPI) con API REST |
| **Frontend** | React.js / Next.js con TypeScript |
| **Base de datos** | PostgreSQL |
| **Cache/Queue** | Redis + Celery para tareas asíncronas |
| **Mobile** | React Native o PWA (Progressive Web App) |
| **Contenedores** | Docker + Docker Compose |
| **CI/CD** | GitHub Actions |

### Estructura del Repositorio Requerida

```
barias-facturas/
├── README.md
├── LICENSE (MIT)
├── docker-compose.yml
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── backend/
│   ├── requirements.txt
│   ├── manage.py
│   ├── core/
│   │   ├── config.py                 # Configuración fiscal DGII
│   │   ├── settings.py
│   │   └── urls.py
│   ├── apps/
│   │   ├── accounts/                 # Usuarios, roles, permisos
│   │   ├── pos/                      # Punto de venta
│   │   ├── invoicing/                # Facturación electrónica (e-CF/NCF)
│   │   ├── accounting/               # Contabilidad
│   │   ├── inventory/                # Inventario y gestión de bebidas
│   │   ├── orders/                   # Pedidos y auto-pedido
│   │   ├── kitchen/                  # Pantalla de cocina (KDS)
│   │   ├── bar/                      # Gestión específica de bar/licores
│   │   ├── customers/                # Clientes y fidelización
│   │   ├── suppliers/                # Proveedores
│   │   ├── reports/                  # Reportes y analíticas
│   │   ├── dgii/                     # Integración DGII (606, 607, 608, e-CF)
│   │   └── ai/                       # Módulo de inteligencia artificial
│   └── utils/
│       ├── ncf_validator.py          # Validación NCF/e-NCF
│       ├── rnc_validator.py          # Validación RNC/Cédula
│       └── dgii_api.py              # API DGII
├── frontend/
│   ├── package.json
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── stores/
│   └── public/
├── mobile/                           # App móvil / PWA
│   └── self-ordering/                # Auto-pedido para clientes
├── docs/
│   ├── API.md
│   ├── INSTALACION.md
│   ├── DGII_GUIA.md
│   └── MANUAL_USUARIO.md
└── tests/
    ├── backend/
    └── frontend/
```

---

## 📦 MÓDULOS DEL SISTEMA - ESPECIFICACIONES DETALLADAS

### 1. 🔐 Módulo de Usuarios y Permisos (`apps/accounts/`)

**Funcionalidades Requeridas:**
- Autenticación JWT con refresh tokens
- Sistema de roles:
  - Administrador
  - Gerente
  - Cajero
  - Mesero
  - Bartender
  - Cocina
  - Contador
- Permisos granulares por módulo y acción
- Registro de actividad (audit log)
- Login con PIN rápido para POS (similar a Toast POS y Square)
- Multi-sucursal / multi-empresa

**Referencias:** Toast POS, Square for Restaurants

---

### 2. 🛒 Módulo POS / Punto de Venta (`apps/pos/`)

**Referencias:** Toast POS, Square for Restaurants, Clover POS, TouchBistro

**Funcionalidades Requeridas:**
- Interfaz táctil optimizada para tablets y terminales
- Gestión de mesas con mapa visual del restaurante (drag & drop)
- División de cuentas / split billing
- Propinas configurables (%, monto fijo)
- Métodos de pago:
  - Efectivo
  - Tarjeta
  - Transferencia
  - QR
  - Mixto
- Apertura y cierre de caja (cash up)
- Impresión de recibos (térmica) y envío por email/WhatsApp
- Modo offline con sincronización automática
- Descuentos, cortesías, happy hour automático
- Turnos de cajero con cuadre

---

### 3. 📄 Módulo de Facturación Electrónica (`apps/invoicing/` + `apps/dgii/`)

**Referencias:** SistemaFacturacionDjango, Odoo DGII e-CF, dgii_reports, republica_dominicana

#### Comprobantes Fiscales (NCF/e-NCF) Requeridos:

**Tipos de NCF (Comprobantes Físicos):**
```python
TIPOS_NCF = {
    '01': 'Factura de Crédito Fiscal',
    '02': 'Factura de Consumo',
    '03': 'Nota de Débito',
    '04': 'Nota de Crédito',
    '11': 'Comprobante de Compras',
    '12': 'Registro Único de Ingresos',
    '13': 'Comprobante para Gastos Menores',
    '14': 'Comprobante de Regímenes Especiales',
    '15': 'Comprobante Gubernamental',
    '16': 'Comprobante para Exportaciones',
    '17': 'Comprobante para Pagos al Exterior',
}
```

**Tipos de e-CF (Comprobantes Electrónicos):**
```python
TIPOS_ECF = {
    '31': 'Factura de Crédito Fiscal Electrónica',
    '32': 'Factura de Consumo Electrónica',
    '33': 'Nota de Débito Electrónica',
    '34': 'Nota de Crédito Electrónica',
    '41': 'Comprobante de Compras Electrónico',
    '43': 'Gastos Menores Electrónico',
    '44': 'Regímenes Especiales Electrónico',
    '45': 'Gubernamental Electrónico',
    '46': 'Exportación Electrónico',
    '47': 'Pagos al Exterior Electrónico',
}
```

#### Impuestos Requeridos:

| Impuesto | Tasa | Aplicación |
|----------|------|------------|
| ITBIS (General) | 18% | Mayoría de productos/servicios |
| ITBIS (Reducido) | 16% | Productos específicos |
| ITBIS (Exento) | 0% | Productos exentos |
| Propina Legal | 10% | Restaurantes y bares |
| ISR Servicios | 10% | Retención en servicios |
| ITBIS Retención | 30% | Del ITBIS total |
| ISC (Cerveza) | 5% | Bebidas alcohólicas |
| ISC (Vino) | 10% | Bebidas alcohólicas |
| ISC (Licor bajo) | 15% | Hasta 20% alcohol |
| ISC (Licor alto) | 20% | Más de 20% alcohol |
| ISC (Champagne) | 25% | Bebidas alcohólicas |

#### Reportes DGII Requeridos:

**Formato 606 - Compras de Bienes y Servicios:**
- RNC/Cédula del proveedor
- Tipo de identificación
- Tipo de bienes y servicios comprados
- NCF
- NCF modificado
- Fecha de comprobante
- Fecha de pago
- Monto facturado
- ITBIS facturado
- ITBIS retenido por terceros
- ITBIS sujeto a proporcionalidad
- ITBIS llevado al costo
- ITBIS por adelantar
- ITBIS percibido en compras
- Tipo de retención en ISR
- Monto retención renta
- ISR percibido en compras
- Impuesto selectivo al consumo
- Otros impuestos/tasas
- Monto propina legal

**Formato 607 - Ventas de Bienes y Servicios:**
- RNC/Cédula del cliente
- Tipo de identificación
- NCF
- NCF modificado
- Tipo de ingreso
- Fecha de comprobante
- Fecha de retención
- Monto facturado
- ITBIS facturado
- ITBIS retenido
- ITBIS percibido
- Retención renta por terceros
- ISR percibido
- Impuesto selectivo al consumo
- Otros impuestos/tasas
- Monto propina legal
- Forma de pago

**Formato 608 - Comprobantes Anulados:**
- NCF
- Fecha de emisión
- Tipo de anulación

**Formato 609 - Pagos al Exterior:**
- Según especificaciones DGII

#### Funcionalidades de Facturación:
- Secuencias automáticas de NCF con control de vencimiento
- Firma electrónica de e-CF
- Envío automático a DGII con estados de tracking:
  - to_send (por enviar)
  - delivered_accepted (aceptado)
  - delivered_refused (rechazado)
  - contingency (modo contingencia)
- Almacenamiento de XML firmados
- Notas de crédito y débito vinculadas
- Validación de RNC ante DGII API
- Generación automática de reportes en formato TXT/CSV

---

### 4. 📊 Módulo de Contabilidad (`apps/accounting/`)

**Referencias:** Odoo Accounting, ERPNext, FacturaScripts

**Funcionalidades Requeridas:**
- Plan de cuentas configurable (adaptado a República Dominicana)
- Asientos contables automáticos desde:
  - Ventas
  - Compras
  - Gastos
- Libro diario
- Libro mayor
- Balance general
- Estado de resultados
- Conciliación bancaria
- Cuentas por cobrar
- Cuentas por pagar
- Gestión de gastos operativos del restaurante/bar
- Cierre contable mensual y anual
- Multi-moneda (DOP, USD) con tasa de cambio automática del Banco Central RD

---

### 5. 📦 Módulo de Inventario (`apps/inventory/` + `apps/bar/`)

**Referencias:** BevSpot, Bar-i, Partender, mPower Beverage, Bottle POS, KORONA POS

#### Inventario General:
- Gestión de productos con categorías:
  - Alimentos
  - Bebidas
  - Licores
  - Insumos
- Código de barras / QR para productos
- Unidades de medida múltiples:
  - Unidad
  - Botella
  - Caja
  - Onza
  - Litro
- Stock mínimo con alertas automáticas
- Entradas y salidas de inventario
- Transferencias entre sucursales/almacenes
- Tomas de inventario físico con comparación
- Costo promedio ponderado y FIFO
- Mermas y desperdicios con registro

#### Gestión Específica de Bebidas y Licores (Bar Module):
- **Control por botella:** Tracking de botellas abiertas vs. cerradas
- **Nivel de botella:** Registro de nivel (%, onzas restantes) — similar a Partender/Bar-i
- **Recetas de cócteles:** Ingredientes con cantidades exactas, costo automático
- **Pour cost:** Cálculo automático del costo de servir cada bebida
- **Varianza de licor:** Comparación entre lo vendido vs. consumido (pérdida/derrame)
- **Alertas de reorden:** Basado en velocidad de consumo y días de inventario
- **Integración con proveedores:** Auto-pedido cuando el stock llega al mínimo
- **Lotes y vencimiento:** Control de fechas para productos perecederos
- **ISC automático:** Cálculo del Impuesto Selectivo al Consumo para bebidas alcohólicas

---

### 6. 🍽️ Módulo de Pedidos (`apps/orders/`)

**Referencias:** Toast POS, Arryved, TouchBistro, Lightspeed Restaurant

#### Pedidos Internos (Meseros):
- Toma de pedidos desde tablet/móvil
- Asignación a:
  - Mesa
  - Barra
  - Delivery
  - Para llevar
- Modificadores de platillos:
  - "Sin cebolla"
  - "Extra queso"
  - "Término de carne"
  - Etc.
- Envío directo a cocina (KDS) y/o barra
- Priorización de pedidos (rush order)
- Notas especiales por ítem
- Transferencia de mesa
- Unión/separación de mesas

#### Auto-pedido / Self-ordering (Para Clientes):
- **QR en mesa:** Cliente escanea QR y ve el menú digital
- **PWA:** No requiere descarga de app
- **Menú visual:** Fotos, descripciones, precios con ITBIS incluido
- **Personalización:** Modificadores, alergenos, recomendaciones
- **Carrito y pago:** 
  - Pago directo desde el celular (tarjeta, QR)
  - O solicitar cuenta al mesero
- **Estado del pedido:** El cliente ve el progreso en tiempo real
- **Llamar al mesero:** Botón para solicitar atención
- **Multi-idioma:** Español, inglés (para zonas turísticas)
- **Menú dinámico:** Ocultar items agotados automáticamente según inventario

---

### 7. 👨‍🍳 Pantalla de Cocina / KDS (`apps/kitchen/`)

**Referencias:** Toast KDS, Lightspeed KDS

**Funcionalidades Requeridas:**
- Pantalla de pedidos en tiempo real
- Organización por estación:
  - Cocina caliente
  - Cocina fría
  - Barra
  - Postres
- Temporizador por pedido con alertas de demora
- Marcado de items completados
- Priorización visual (colores por tiempo de espera)
- Historial de tiempos de preparación
- Compatible con pantallas táctiles grandes

---

### 8. 👥 Módulo de Clientes y Fidelización (`apps/customers/`)

**Referencias:** Upserve, Square Loyalty

**Funcionalidades Requeridas:**
- Base de datos de clientes con historial de compras
- Validación de RNC/Cédula para facturación fiscal
- Programa de puntos/recompensas
- Tarjetas de regalo (gift cards)
- Descuentos por cliente VIP
- Envío de promociones por WhatsApp/SMS/Email
- Análisis de preferencias y frecuencia de visita

---

### 9. 🚚 Módulo de Proveedores y Compras (`apps/suppliers/`)

**Referencias:** Revel Systems, Lavu POS

**Funcionalidades Requeridas:**
- Catálogo de proveedores con RNC
- Órdenes de compra con aprobación
- Recepción de mercancía con verificación
- Cuentas por pagar con vencimientos
- Historial de precios por proveedor
- Comparación de precios entre proveedores
- Auto-pedido inteligente basado en consumo histórico

---

### 10. 📈 Módulo de Reportes e Inteligencia (`apps/reports/` + `apps/ai/`)

**Referencias:** Upserve Analytics, Toast Analytics, BevSpot Analytics

#### Reportes Operativos:
- Ventas por hora, día, semana, mes
- Ventas por producto, categoría, mesero
- Ticket promedio
- Productos más/menos vendidos
- Rentabilidad por platillo/bebida
- Ocupación de mesas y rotación
- Tiempos de servicio (cocina y barra)
- Reporte de propinas por empleado
- Dashboard en tiempo real

#### Reportes Financieros:
- Estado de resultados
- Flujo de caja
- Cuentas por cobrar/pagar aging
- Análisis de costos:
  - Food cost
  - Pour cost
  - Labor cost

#### Inteligencia Artificial 🤖:
- **Predicción de demanda:** Estimación de ventas por día/hora usando datos históricos
- **Sugerencia de inventario:** Cantidades óptimas de compra basadas en tendencias
- **Detección de anomalías:** Alertas de consumo inusual (posible robo/desperdicio)
- **Precios dinámicos:** Sugerencias de happy hour basadas en inventario y demanda
- **Menú inteligente:** Recomendaciones de platillos para clientes basadas en historial
- **Análisis de sentimiento:** Integración con reseñas de Google/TripAdvisor
- **Forecast financiero:** Proyección de ingresos y gastos

---

## 🔧 Configuración Fiscal DGII (República Dominicana)

### Archivo `backend/core/config.py` - Contenido Requerido:

```python
"""
Configuración Fiscal DGII - República Dominicana
Barias ERP - Sistema de Gestión para Restaurantes, Bares y Licor Stores
"""

DGII_CONFIG = {
    'TIPOS_NCF': {
        '01': 'Factura de Crédito Fiscal',
        '02': 'Factura de Consumo',
        '03': 'Nota de Débito',
        '04': 'Nota de Crédito',
        '11': 'Comprobante de Compras',
        '12': 'Registro Único de Ingresos',
        '13': 'Comprobante para Gastos Menores',
        '14': 'Comprobante de Regímenes Especiales',
        '15': 'Comprobante Gubernamental',
        '16': 'Comprobante para Exportaciones',
        '17': 'Comprobante para Pagos al Exterior',
    },
    'TIPOS_ANULACION': {
        '01': 'Deterioro de Factura Pre-impresa',
        '02': 'Errores de Impresión',
        '03': 'Impresión Defectuosa',
        '04': 'Corrección de la Información',
        '05': 'Cambio de Productos',
        '06': 'Devolución de Productos',
        '07': 'Omisión de Productos',
        '08': 'Errores en Secuencia de NCF',
        '09': 'Por Cese de Operaciones',
        '10': 'Pérdida o Hurto de Talonarios',
    },
    'ITBIS_TASA': 0.18,
    'ITBIS_TASA_REDUCIDA': 0.16,
    'PROPINA_LEGAL': 0.10,
    'RETENCION_ISR_SERVICIOS': 0.10,
    'RETENCION_ITBIS': 0.30,
}
```

---

## 📄 ARCHIVOS INICIALES A CREAR (14 Entregables)

### 1. README.md
**Contenido Requerido:**
- Logo/nombre del proyecto: **Barias ERP**
- Descripción del sistema
- Features principales
- Screenshots/mockups placeholders
- Guía de instalación (Docker)
- Stack tecnológico
- Guía de contribución
- Licencia MIT
- Badges (build, license, version)
- Todo en español

### 2. docker-compose.yml
**Servicios Requeridos:**
```yaml
version: '3.8'
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: barias_erp
      POSTGRES_USER: barias
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgresql://barias:${DB_PASSWORD}@db:5432/barias_erp
      - REDIS_URL=redis://redis:6379/0

  frontend:
    build: ./frontend
    volumes:
      - ./frontend:/app
    ports:
      - "3000:3000"
    depends_on:
      - backend

  celery:
    build: ./backend
    command: celery -A core worker -l info
    volumes:
      - ./backend:/app
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
```

### 3. GitHub Actions CI (.github/workflows/ci.yml)
**Pipelines Requeridos:**
- Lint (flake8/black para Python, ESLint para JS)
- Tests (pytest, jest)
- Build Docker images
- Security scan

### 4. .env.example
**Variables Requeridas:**
```
DB_PASSWORD=your_secure_password
SECRET_KEY=your_django_secret_key
DGII_ENV=test  # test | production
DGII_RNC=your_company_rnc
DGII_CERT_PATH=/certs/dgii_cert.p12
DGII_CERT_PASSWORD=your_cert_password
```

### 5. backend/core/config.py
- Configuración fiscal DGII completa
- Todos los tipos de NCF y e-CF
- Todas las tasas de impuestos
- Tipos de anulación
- Formas de pago

### 6. backend/utils/ncf_validator.py
- Validador de formato NCF
- Validador de secuencias
- Validador de vencimiento
- Generador de NCF
- Extractor de componentes

### 7. backend/utils/rnc_validator.py
- Validador de RNC (9 dígitos)
- Validador de Cédula (11 dígitos con algoritmo Luhn)
- Auto-detección de tipo
- Formateadores

### 8. backend/requirements.txt
**Dependencias Principales:**
- Django>=5.0.0
- djangorestframework
- psycopg2-binary
- celery
- redis
- django-redis
- djangorestframework-simplejwt
- cryptography
- lxml (para e-CF)
- reportlab (para PDF)
- qrcode
- requests
- pytest

### 9. frontend/package.json
**Dependencias Principales:**
- next (>=14.1.0)
- react (>=18.2.0)
- typescript
- @tanstack/react-query
- axios
- zustand
- react-hook-form
- zod
- recharts
- socket.io-client

### 10. docs/INSTALACION.md
**Contenido Requerido:**
- Requisitos del sistema
- Instalación con Docker (paso a paso)
- Instalación manual (sin Docker)
- Configuración de variables de entorno
- Configuración de certificado DGII
- Verificación de instalación
- Solución de problemas comunes

### 11. docs/DGII_GUIA.md
**Contenido Requerido:**
- Explicación de NCF y e-CF
- Tabla completa de tipos de comprobantes
- Ejemplos de cálculo de impuestos
- Proceso de facturación electrónica
- Configuración de secuencias NCF
- Modo contingencia
- Generación de reportes 606, 607, 608
- Links a recursos DGII

### 12. docs/API.md
**Contenido Requerido:**
- Autenticación JWT
- Endpoints principales
- Ejemplos de requests/responses
- Códigos de error
- Paginación
- WebSocket para tiempo real

### 13. docs/MANUAL_USUARIO.md
**Contenido Requerido:**
- Guía de uso del POS
- Guía de meseros
- Guía de cocina
- Gestión de inventario
- Facturación
- Reportes
- Preguntas frecuentes

### 14. LICENSE
- MIT License

---

## 🔗 REFERENCIAS DE CÓDIGO ABIERTO

Proyectos que sirvieron de inspiración y referencia:

### Proyectos DGII (República Dominicana):
| Proyecto | GitHub | Uso |
|----------|--------|-----|
| henry365/SistemaFacturacionDjango | GitHub | Configuración fiscal DGII, NCF, reportes 606/607/608 |
| ithesk/odoo_dgii_ecf | GitHub | Facturación electrónica e-CF |
| jeffryjdelarosa/dgii_reports | GitHub | Validación NCF/RNC |
| joenilson/republica_dominicana | GitHub | NCF + reportes fiscales para FacturaScripts |
| joseernestomendez/external-service-addons | GitHub | Envío e-CF a DGII |

### Sistemas POS Open Source:
| Proyecto | GitHub | Uso |
|----------|--------|-----|
| opensourcepos/opensourcepos | GitHub | POS web con inventario y facturación |
| floreantpos/floreantpos | GitHub | POS para restaurantes con KDS |

### Sistemas Comerciales de Referencia (UX/funcionalidades):
- **POS General:** Toast POS, Square for Restaurants, Lightspeed Restaurant, TouchBistro, Clover POS, Revel Systems, Lavu POS
- **Gestión de Bar:** BevSpot, Bar-i, Partender, Bottle POS, KORONA POS, mPower Beverage
- **Analíticas:** Upserve, Toast Analytics
- **KDS:** Toast KDS, Lightspeed KDS
- **Loyalty:** Square Loyalty
- **Contabilidad:** Odoo Accounting, ERPNext, FacturaScripts

---

## ✅ CRITERIOS DE ÉXITO

El sistema debe cumplir con:

1. **Cumplimiento DGII 100%:**
   - Todos los tipos de NCF y e-CF implementados
   - Cálculo correcto de todos los impuestos
   - Generación de reportes 606, 607, 608, 609
   - Validación de RNC/Cédula
   - Envío de e-CF a DGII

2. **POS Funcional:**
   - Interfaz táctil optimizada
   - División de cuentas
   - Modo offline
   - Múltiples métodos de pago

3. **Inventario Inteligente:**
   - Control de bebidas por botella
   - Cálculo de pour cost
   - Alertas de reorden

4. **Arquitectura Escalable:**
   - Modular con apps independientes
   - API REST documentada
   - Docker para deployment
   - CI/CD automatizado

5. **Documentación Completa:**
   - Todo en español
   - Guías de instalación y uso
   - Documentación técnica
   - Ejemplos de código

---

## 📊 MÉTRICAS DE CALIDAD

- ✅ Cobertura de tests: >80%
- ✅ Validación de datos: 100% en inputs fiscales
- ✅ Tiempo de respuesta API: <200ms
- ✅ Disponibilidad: 99.9%
- ✅ Compatibilidad mobile: 100%

---

## 🚀 FASES DE IMPLEMENTACIÓN

### Fase 0 - Inicial (COMPLETADA) ✅
- [x] Estructura del proyecto
- [x] Configuración DGII
- [x] Validadores NCF/RNC
- [x] Docker setup
- [x] CI/CD
- [x] Documentación base

### Fase 1 - Core (Próxima)
- [ ] Modelos Django completos
- [ ] API REST endpoints
- [ ] Autenticación JWT
- [ ] POS básico
- [ ] Facturación con NCF

### Fase 2 - Avanzado
- [ ] Facturación electrónica (e-CF)
- [ ] Integración DGII
- [ ] Reportes automatizados
- [ ] Pantalla de cocina (KDS)
- [ ] Auto-pedido con QR

### Fase 3 - Inteligencia
- [ ] Módulo de IA
- [ ] Predicción de demanda
- [ ] Análisis avanzados
- [ ] Optimización automática

---

## 📞 SOPORTE Y RECURSOS

- **Portal DGII:** https://dgii.gov.do
- **Oficina Virtual DGII:** https://oficinavirtual.dgii.gov.do
- **Documentación Django:** https://docs.djangoproject.com
- **Documentación Next.js:** https://nextjs.org/docs
- **GitHub Repo:** https://github.com/bariaspromo/barias-facturas

---

**Última actualización:** Febrero 2026

**Versión del Prompt:** 1.0

**Estado:** ✅ Fase 0 Completada - Ready for Fase 1

---

## 🎯 NOTAS FINALES

Este documento representa la especificación completa y original del sistema Barias ERP. Todas las funcionalidades, módulos y requerimientos listados aquí deben ser implementados siguiendo estas especificaciones para asegurar:

1. **Cumplimiento fiscal** total con la DGII de República Dominicana
2. **Experiencia de usuario** óptima basada en mejores prácticas de sistemas comerciales
3. **Arquitectura técnica** escalable y mantenible
4. **Documentación** completa en español

El sistema está diseñado para ser la solución más completa del mercado dominicano para restaurantes, bares y licor stores, combinando cumplimiento fiscal, operaciones eficientes y analíticas inteligentes.

---

**🇩🇴 Hecho para República Dominicana con ❤️**
