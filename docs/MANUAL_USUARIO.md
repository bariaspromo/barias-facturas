# 📖 Manual de Usuario - Barias ERP

Manual de usuario para el sistema Barias ERP.

---

## 🚀 Inicio Rápido

### Acceso al Sistema

1. Abre tu navegador y ve a: `http://localhost:3000`
2. Ingresa tus credenciales
3. Selecciona tu rol (Cajero, Mesero, Administrador, etc.)

---

## 💳 Módulo POS (Punto de Venta)

### Realizar una Venta

1. **Iniciar sesión en POS**
   - Click en "POS" en el menú principal
   - Selecciona tu caja
   - Ingresa tu PIN

2. **Agregar Productos**
   - Busca el producto por nombre o código
   - O selecciona desde las categorías
   - Ajusta la cantidad si es necesario

3. **Aplicar Descuentos** (opcional)
   - Click en "Descuento"
   - Ingresa porcentaje o monto fijo

4. **Procesar Pago**
   - Click en "Cobrar"
   - Selecciona método de pago:
     - Efectivo
     - Tarjeta
     - Transferencia
     - Mixto
   - Ingresa monto recibido
   - Confirma la venta

5. **Imprimir/Enviar Factura**
   - Impresión automática (si está configurada)
   - O enviar por email/WhatsApp

### División de Cuenta

Para dividir una cuenta entre varios clientes:

1. Click en "Dividir Cuenta"
2. Selecciona los ítems para cada cliente
3. Procesa cada pago individualmente

---

## 🍽️ Módulo de Meseros

### Tomar un Pedido

1. **Seleccionar Mesa**
   - Click en la mesa en el mapa
   - O ingresa el número de mesa

2. **Agregar Ítems**
   - Busca o selecciona productos
   - Agrega modificadores:
     - "Sin cebolla"
     - "Término 3/4"
     - "Extra queso"

3. **Enviar a Cocina**
   - Click en "Enviar"
   - El pedido aparece en la pantalla de cocina

4. **Agregar Más Ítems** (después)
   - Selecciona la mesa nuevamente
   - Agrega nuevos productos
   - Envía actualización

5. **Solicitar Cuenta**
   - Click en "Cuenta"
   - Se genera pre-cuenta
   - Cliente revisa y aprueba
   - Procesar pago en caja

### Transferir Mesa

1. Selecciona la mesa original
2. Click en "Transferir"
3. Selecciona mesa destino
4. Confirmar transferencia

---

## 📦 Módulo de Inventario

### Registrar Entrada de Productos

1. **Ir a Inventario → Entradas**
2. **Click en "Nueva Entrada"**
3. **Completar formulario:**
   - Proveedor
   - Producto
   - Cantidad
   - Costo unitario
   - Fecha de vencimiento (si aplica)
4. **Guardar**

### Toma de Inventario Físico

1. **Ir a Inventario → Toma Física**
2. **Click en "Nueva Toma"**
3. **Contar productos**:
   - Escanea código de barras
   - O busca manualmente
   - Ingresa cantidad física
4. **Completar y Comparar**
   - Sistema compara con stock teórico
   - Muestra diferencias
5. **Ajustar** (si es necesario)

---

## 🍹 Gestión de Bar

### Registrar Nivel de Botellas

1. **Ir a Bar → Botellas Abiertas**
2. **Seleccionar botella**
3. **Ingresar nivel actual**:
   - Porcentaje restante
   - O onzas restantes
4. **Guardar**

### Crear Receta de Cóctel

1. **Ir a Bar → Recetas**
2. **Click en "Nueva Receta"**
3. **Completar:**
   - Nombre del cóctel
   - Ingredientes con cantidades exactas
   - Método de preparación
4. **Guardar**
   - Sistema calcula costo automáticamente

---

## 📄 Facturación

### Generar Factura con NCF

1. **Completar venta en POS**
2. **Ingresar datos del cliente:**
   - Nombre
   - RNC o Cédula
   - Dirección
3. **Seleccionar tipo de NCF:**
   - 01: Crédito Fiscal (con RNC)
   - 02: Consumo (sin RNC)
4. **Confirmar**
   - Sistema asigna NCF automáticamente
   - Genera factura

### Anular Factura

1. **Buscar factura a anular**
2. **Click en "Anular"**
3. **Seleccionar motivo:**
   - Error en información
   - Devolución
   - Etc.
4. **Confirmar**
   - Sistema registra en Formato 608

---

## 📊 Reportes

### Ver Ventas del Día

1. **Ir a Reportes → Ventas**
2. **Seleccionar fecha: Hoy**
3. **Ver gráficas y totales:**
   - Ventas por hora
   - Métodos de pago
   - Productos más vendidos

### Generar Reporte DGII (607)

1. **Ir a DGII → Reportes**
2. **Seleccionar:** Formato 607
3. **Elegir mes y año**
4. **Click en "Generar"**
5. **Descargar archivo TXT**
6. **Subir a Portal DGII**

---

## ⚙️ Configuración

### Cambiar Contraseña

1. **Click en tu perfil** (esquina superior derecha)
2. **Configuración → Seguridad**
3. **Cambiar Contraseña**
4. **Guardar**

### Configurar Impresora

1. **Ir a Configuración → Dispositivos**
2. **Agregar Impresora**
3. **Seleccionar tipo:**
   - Impresora térmica
   - Impresora láser
4. **Configurar**
5. **Hacer prueba de impresión**

---

## 🆘 Preguntas Frecuentes

### ¿Cómo funciona el modo offline?

El sistema POS funciona sin internet. Las transacciones se guardan localmente y se sincronizan automáticamente cuando se restablece la conexión.

### ¿Puedo modificar un pedido ya enviado a cocina?

Sí, puedes agregar más ítems. Para cancelar ítems ya enviados, debes tener permisos de gerente.

### ¿Cómo sé cuántos NCF me quedan?

El sistema te alerta automáticamente cuando quedan menos de 100 NCF disponibles.

### ¿Qué hago si se acabaron los NCF?

1. Solicita nueva secuencia a DGII
2. En el sistema: DGII → Secuencias → Agregar Nueva
3. Ingresa los datos de la nueva secuencia

---

## 📞 Soporte

- 🐛 [Reportar problema](https://github.com/bariaspromo/barias-facturas/issues)
- 📧 Email: support@bariaserp.com
- 📱 WhatsApp: +1-809-555-1234

---

**¡Gracias por usar Barias ERP!** 🎉
