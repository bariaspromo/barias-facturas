# 📄 Guía de Integración DGII - Barias ERP

Esta guía detalla cómo funciona la integración con la Dirección General de Impuestos Internos (DGII) de República Dominicana.

---

## 📋 Descripción General

El sistema Barias ERP cumple con todos los requisitos fiscales de la DGII para:

- ✅ Emisión de Comprobantes Fiscales (NCF)
- ✅ Facturación Electrónica (e-CF)
- ✅ Generación de Reportes (606, 607, 608, 609)
- ✅ Validación de RNC y Cédulas
- ✅ Cálculo automático de impuestos

---

## 🔢 Comprobantes Fiscales (NCF)

### Tipos de NCF Soportados

El sistema soporta todos los tipos de comprobantes según la normativa DGII:

#### Comprobantes Físicos

| Código | Tipo | Uso |
|--------|------|-----|
| 01 | Factura de Crédito Fiscal | Ventas a contribuyentes con derecho a crédito |
| 02 | Factura de Consumo | Ventas finales a consumidores |
| 03 | Nota de Débito | Aumentos posteriores al monto facturado |
| 04 | Nota de Crédito | Devoluciones o descuentos posteriores |
| 11 | Comprobante de Compras | Registro de compras |
| 12 | Registro Único de Ingresos | Pequeños contribuyentes |
| 13 | Gastos Menores | Compras menores a RD$ 50,000 |
| 14 | Regímenes Especiales | Contribuyentes con regímenes especiales |
| 15 | Gubernamental | Ventas al Estado |
| 16 | Exportaciones | Ventas al exterior |
| 17 | Pagos al Exterior | Servicios del exterior |

#### Comprobantes Electrónicos (e-CF)

| Código | Tipo |
|--------|------|
| 31 | Factura de Crédito Fiscal Electrónica |
| 32 | Factura de Consumo Electrónica |
| 33 | Nota de Débito Electrónica |
| 34 | Nota de Crédito Electrónica |
| 41 | Comprobante de Compras Electrónico |
| 43 | Gastos Menores Electrónico |
| 44 | Regímenes Especiales Electrónico |
| 45 | Gubernamental Electrónico |
| 46 | Exportación Electrónico |
| 47 | Pagos al Exterior Electrónico |

### Formato de NCF

Un NCF tiene el siguiente formato:

```
A01 + RNC (9 dígitos) + Tipo (2 dígitos) + Secuencia (8 dígitos)
```

**Ejemplo:** `A01123456789021234567890`

- `A01`: Serie
- `123456789`: RNC del emisor
- `02`: Tipo (Factura de Consumo)
- `12345678`: Número de secuencia

---

## 💰 Impuestos

### ITBIS (Impuesto a las Transferencias de Bienes y Servicios)

| Tasa | Porcentaje | Aplicación |
|------|------------|------------|
| General | 18% | Mayoría de bienes y servicios |
| Reducida | 16% | Algunos productos específicos |
| Exenta | 0% | Productos y servicios exentos |

**Cálculo automático:**
```python
# En el sistema
subtotal = 1000.00
itbis = subtotal * 0.18  # 180.00
total = subtotal + itbis  # 1180.00
```

### Propina Legal (10%)

Aplicable a restaurantes y bares:

```python
subtotal = 1000.00
propina = subtotal * 0.10  # 100.00
itbis = (subtotal + propina) * 0.18  # 198.00
total = subtotal + propina + itbis  # 1298.00
```

### ISC (Impuesto Selectivo al Consumo)

Aplicable a bebidas alcohólicas:

| Producto | Tasa ISC |
|----------|----------|
| Cerveza | 5% |
| Vino | 10% |
| Licor (hasta 20% alcohol) | 15% |
| Licor (más de 20% alcohol) | 20% |
| Champagne | 25% |

**Cálculo:**
```python
precio_base = 500.00  # Botella de ron
isc = precio_base * 0.20  # 100.00
precio_con_isc = precio_base + isc  # 600.00
itbis = precio_con_isc * 0.18  # 108.00
total = precio_con_isc + itbis  # 708.00
```

---

## 📊 Reportes DGII

### Formato 606 - Compras

Reporte mensual de todas las compras realizadas.

**Generación:**
```bash
# Desde el sistema
docker-compose exec backend python manage.py generar_606 --mes 2 --año 2024
```

**Contenido:**
- RNC del proveedor
- Tipo de comprobante
- Monto facturado
- ITBIS pagado
- Retenciones

### Formato 607 - Ventas

Reporte mensual de todas las ventas realizadas.

**Generación:**
```bash
docker-compose exec backend python manage.py generar_607 --mes 2 --año 2024
```

**Contenido:**
- RNC del cliente (si aplica)
- NCF emitido
- Tipo de ingreso
- Monto facturado
- ITBIS cobrado

### Formato 608 - Anulaciones

Reporte de comprobantes anulados.

**Tipos de anulación:**
1. Deterioro de factura
2. Errores de impresión
3. Corrección de información
4. Devolución de productos
5. Y más...

### Formato 609 - Pagos al Exterior

Para servicios o productos del exterior.

---

## 🔐 Facturación Electrónica (e-CF)

### Requisitos

1. **Certificado Digital:** Obtenido de la DGII
2. **Autorización:** Solicitar habilitación para e-CF
3. **Conexión:** Internet estable para envío a DGII

### Proceso de Facturación Electrónica

```
1. Cliente realiza compra
   ↓
2. Sistema genera e-CF (XML)
   ↓
3. Sistema firma e-CF con certificado digital
   ↓
4. Sistema envía a DGII
   ↓
5. DGII valida y responde con código de seguridad
   ↓
6. Sistema almacena respuesta y actualiza estado
   ↓
7. Cliente recibe factura electrónica
```

### Estados de e-CF

| Estado | Descripción |
|--------|-------------|
| `draft` | Borrador, aún no enviado |
| `to_send` | Pendiente de envío a DGII |
| `sent` | Enviado a DGII, esperando respuesta |
| `delivered_accepted` | Aceptado por DGII |
| `delivered_refused` | Rechazado por DGII |
| `cancelled` | Anulado |
| `contingency` | En modo contingencia |

### Modo Contingencia

Si no hay conexión con DGII:

1. Sistema genera e-CF localmente
2. Marca como "contingencia"
3. Almacena para envío posterior
4. Envía automáticamente cuando se restablece conexión
5. Plazo máximo: 7 días

---

## ✅ Validaciones

### Validación de RNC

```python
from backend.utils.rnc_validator import validar_rnc

# Validar formato
es_valido = validar_rnc("123456789")

# Validar contra DGII (requiere conexión)
from backend.utils.dgii_api import get_dgii_client

client = get_dgii_client()
success, data, error = client.validar_rnc("123456789")

if success:
    print(f"Contribuyente: {data['nombre']}")
    print(f"Estado: {data['estado']}")
```

### Validación de Cédula

```python
from backend.utils.rnc_validator import validar_cedula

# Con guiones
es_valida = validar_cedula("001-1234567-1")

# Sin guiones
es_valida = validar_cedula("00112345671")
```

### Validación de NCF

```python
from backend.utils.ncf_validator import validar_ncf

# Validar formato
es_valido = validar_ncf("A01123456789021234567890")

# Validación completa
from backend.utils.ncf_validator import NCFValidator

es_valido, mensajes = NCFValidator.validar_ncf_completo(
    ncf="A01123456789021234567890",
    rnc_emisor="123456789",
    secuencia_inicio=1,
    secuencia_fin=99999999,
    fecha_vencimiento=datetime(2024, 12, 31)
)
```

---

## 🔄 Configuración en el Sistema

### 1. Configurar Datos de la Empresa

En Admin Django (`/admin`):

1. Ir a **Configuración → Empresa**
2. Completar:
   - RNC
   - Razón Social
   - Dirección
   - Teléfono
   - Email

### 2. Configurar Secuencias de NCF

1. Ir a **DGII → Secuencias NCF**
2. Para cada tipo de comprobante:
   - Serie (ej: A01)
   - Secuencia inicial
   - Secuencia final
   - Fecha de vencimiento

### 3. Subir Certificado Digital

1. Ir a **DGII → Certificados**
2. Subir archivo `.p12`
3. Ingresar contraseña
4. Activar certificado

### 4. Configurar Ambiente DGII

En `.env`:
```env
DGII_ENV=production  # o 'test' para pruebas
```

---

## 📞 Soporte DGII

- **Portal DGII:** https://dgii.gov.do
- **Oficina Virtual:** https://oficinavirtual.dgii.gov.do
- **Teléfono:** 809-689-3444
- **Email:** consultas@dgii.gov.do

---

## 🔗 Enlaces Útiles

- [Normativa General 06-2018](https://dgii.gov.do/normativas)
- [Manual de e-CF](https://dgii.gov.do/ecf)
- [Tipos de Comprobantes](https://dgii.gov.do/comprobantes)
- [Calendario Tributario](https://dgii.gov.do/calendario)

---

**Nota:** Esta documentación se actualiza regularmente según cambios en la normativa DGII.
