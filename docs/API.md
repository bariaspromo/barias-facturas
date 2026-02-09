# 🔌 API Documentation - Barias ERP

Documentación de la API REST de Barias ERP.

---

## 📋 Información General

- **Base URL:** `http://localhost:8000/api`
- **Formato:** JSON
- **Autenticación:** JWT (JSON Web Tokens)
- **Versionado:** `/api/v1/`

---

## 🔐 Autenticación

### Obtener Token

```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "password123"
}
```

**Respuesta:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@bariaserp.com",
    "role": "admin"
  }
}
```

### Usar Token

```http
GET /api/v1/invoices
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### Refrescar Token

```http
POST /api/auth/refresh
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## 📄 Endpoints - Facturación

### Listar Facturas

```http
GET /api/v1/invoices?page=1&limit=20
```

**Parámetros de consulta:**
- `page`: Número de página (default: 1)
- `limit`: Resultados por página (default: 20)
- `status`: Filtrar por estado (draft, sent, paid, cancelled)
- `customer`: ID del cliente
- `date_from`: Fecha desde (YYYY-MM-DD)
- `date_to`: Fecha hasta (YYYY-MM-DD)

### Crear Factura

```http
POST /api/v1/invoices
Content-Type: application/json

{
  "customer_id": 1,
  "ncf_type": "02",
  "items": [
    {
      "product_id": 10,
      "quantity": 2,
      "price": 500.00
    }
  ],
  "payment_method": "cash",
  "notes": "Factura de prueba"
}
```

### Obtener Factura

```http
GET /api/v1/invoices/{id}
```

### Anular Factura

```http
POST /api/v1/invoices/{id}/cancel
Content-Type: application/json

{
  "reason": "04",
  "notes": "Cliente devolvió productos"
}
```

---

## 🛒 Endpoints - POS

### Crear Orden

```http
POST /api/v1/pos/orders
Content-Type: application/json

{
  "table_id": 5,
  "waiter_id": 2,
  "items": [
    {
      "product_id": 15,
      "quantity": 1,
      "modifiers": ["sin cebolla", "extra queso"]
    }
  ]
}
```

### Dividir Cuenta

```http
POST /api/v1/pos/orders/{id}/split
Content-Type: application/json

{
  "splits": [
    {
      "items": [1, 2],
      "customer_name": "Cliente 1"
    },
    {
      "items": [3, 4],
      "customer_name": "Cliente 2"
    }
  ]
}
```

---

## 📦 Endpoints - Inventario

### Listar Productos

```http
GET /api/v1/inventory/products
```

### Actualizar Stock

```http
PATCH /api/v1/inventory/products/{id}/stock
Content-Type: application/json

{
  "quantity": 50,
  "reason": "restock",
  "notes": "Compra a proveedor"
}
```

### Alerta de Stock Bajo

```http
GET /api/v1/inventory/low-stock
```

---

## 👥 Endpoints - Clientes

### Crear Cliente

```http
POST /api/v1/customers
Content-Type: application/json

{
  "name": "Juan Pérez",
  "rnc": "123456789",
  "email": "juan@example.com",
  "phone": "809-555-1234",
  "address": "Av. Principal #123"
}
```

### Validar RNC

```http
GET /api/v1/customers/validate-rnc/{rnc}
```

---

## 📊 Endpoints - Reportes

### Ventas por Período

```http
GET /api/v1/reports/sales?start=2024-01-01&end=2024-01-31
```

### Productos Más Vendidos

```http
GET /api/v1/reports/top-products?limit=10
```

### Reporte DGII 607

```http
GET /api/v1/reports/dgii/607?month=1&year=2024
```

---

## 📱 WebSocket - Tiempo Real

### Conectar

```javascript
const socket = io('http://localhost:8000', {
  auth: {
    token: 'Bearer eyJ0eXAiOiJKV1QiLCJhbGc...'
  }
});

// Escuchar nuevos pedidos (Cocina)
socket.on('new_order', (data) => {
  console.log('Nueva orden:', data);
});

// Actualización de mesa
socket.on('table_update', (data) => {
  console.log('Mesa actualizada:', data);
});
```

---

## 🧪 Testing

### Ambiente de Pruebas

- **Base URL:** `https://test-api.bariaserp.com`
- **Credenciales de prueba:**
  - Usuario: `test@bariaserp.com`
  - Password: `Test123!`

---

## 📝 Códigos de Estado

| Código | Significado |
|--------|-------------|
| 200 | OK |
| 201 | Creado |
| 400 | Solicitud inválida |
| 401 | No autenticado |
| 403 | Sin permisos |
| 404 | No encontrado |
| 500 | Error del servidor |

---

## 🔗 Documentación Interactiva

Accede a la documentación interactiva Swagger UI:

```
http://localhost:8000/api/docs
```

O ReDoc:

```
http://localhost:8000/api/redoc
```

---

**Documentación completa en desarrollo...**
