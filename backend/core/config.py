"""
Configuración Fiscal DGII - República Dominicana
Barias ERP - Sistema de Gestión para Restaurantes, Bares y Licor Stores

Este módulo contiene toda la configuración necesaria para cumplir con
la normativa fiscal de la Dirección General de Impuestos Internos (DGII)
de República Dominicana.
"""

from decimal import Decimal

# ============================================================================
# TIPOS DE COMPROBANTES FISCALES (NCF)
# ============================================================================

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

# ============================================================================
# TIPOS DE COMPROBANTES FISCALES ELECTRÓNICOS (e-CF)
# ============================================================================

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

# ============================================================================
# TIPOS DE ANULACIÓN
# ============================================================================

TIPOS_ANULACION = {
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
}

# ============================================================================
# TIPOS DE INGRESOS (Para Formato 607)
# ============================================================================

TIPOS_INGRESO = {
    '01': 'Ingresos por Operaciones (No Financieros)',
    '02': 'Ingresos Financieros',
    '03': 'Ingresos Extraordinarios',
    '04': 'Ingresos por Arrendamientos',
    '05': 'Ingresos por Venta de Activo Depreciable',
    '06': 'Otros Ingresos',
}

# ============================================================================
# TIPOS DE BIENES Y SERVICIOS COMPRADOS
# ============================================================================

TIPOS_BIENES_SERVICIOS = {
    '01': 'Gastos de Personal',
    '02': 'Gastos por Trabajo, Suministros y Servicios',
    '03': 'Arrendamientos',
    '04': 'Gastos de Activos Fijos',
    '05': 'Gastos de Representación',
    '06': 'Otras Deducciones Admitidas',
    '07': 'Gastos Financieros',
    '08': 'Gastos Extraordinarios',
    '09': 'Compras y Gastos que forman parte del Costo de Venta',
    '10': 'Adquisiciones de Activos',
    '11': 'Gastos de Seguros',
}

# ============================================================================
# TASAS DE IMPUESTOS
# ============================================================================

# ITBIS (Impuesto a la Transferencia de Bienes Industrializados y Servicios)
ITBIS_TASA = Decimal('0.18')  # 18% tasa general
ITBIS_TASA_REDUCIDA = Decimal('0.16')  # 16% tasa reducida
ITBIS_EXENTO = Decimal('0.00')  # 0% exento

# Propina Legal (Restaurantes y Bares)
PROPINA_LEGAL = Decimal('0.10')  # 10%

# Retenciones
RETENCION_ISR_SERVICIOS = Decimal('0.10')  # 10% retención ISR en servicios
RETENCION_ITBIS = Decimal('0.30')  # 30% del ITBIS (proporción del 18%)
RETENCION_ISR_ASALARIADOS = Decimal('0.15')  # 15% tasa estándar

# ISC (Impuesto Selectivo al Consumo) - Bebidas Alcohólicas
# Las tasas varían según el tipo de bebida y grados de alcohol
ISC_BEBIDAS_ALCOHOLICAS = {
    'cerveza': Decimal('0.05'),  # 5%
    'vino': Decimal('0.10'),  # 10%
    'licor_bajo': Decimal('0.15'),  # 15% (hasta 20% alcohol)
    'licor_alto': Decimal('0.20'),  # 20% (más de 20% alcohol)
    'champagne': Decimal('0.25'),  # 25%
}

# ============================================================================
# ESTADOS DE COMPROBANTES FISCALES
# ============================================================================

ESTADOS_NCF = {
    'draft': 'Borrador',
    'to_send': 'Por Enviar',
    'sent': 'Enviado',
    'delivered_accepted': 'Entregado y Aceptado',
    'delivered_refused': 'Entregado y Rechazado',
    'cancelled': 'Anulado',
    'contingency': 'Contingencia',
}

# ============================================================================
# FORMAS DE PAGO
# ============================================================================

FORMAS_PAGO = {
    '01': 'Efectivo',
    '02': 'Cheques/Transferencias/Depósitos',
    '03': 'Tarjeta de Crédito/Débito',
    '04': 'Compra a Crédito',
    '05': 'Bonos o Certificados de Regalo',
    '06': 'Permuta',
    '07': 'Nota de Crédito',
    '08': 'Otras Formas de Venta',
}

# ============================================================================
# TIPOS DE IDENTIFICACIÓN
# ============================================================================

TIPOS_IDENTIFICACION = {
    '1': 'Cédula',
    '2': 'RNC (Registro Nacional del Contribuyente)',
    '3': 'Pasaporte',
    '4': 'Extranjero sin identificación',
}

# ============================================================================
# CONFIGURACIÓN DE REPORTES DGII
# ============================================================================

# Formato 606 - Compras
FORMATO_606_COLUMNAS = [
    'RNC/Cédula',
    'Tipo de Identificación',
    'Tipo de Bienes y Servicios Comprados',
    'NCF',
    'NCF Modificado',
    'Fecha de Comprobante',
    'Fecha de Pago',
    'Monto Facturado',
    'ITBIS Facturado',
    'ITBIS Retenido por Terceros',
    'ITBIS Sujeto a Proporcionalidad',
    'ITBIS Llevado al Costo',
    'ITBIS por Adelantar',
    'ITBIS Percibido en Compras',
    'Tipo de Retención en ISR',
    'Monto Retención Renta',
    'ISR Percibido en Compras',
    'Impuesto Selectivo al Consumo',
    'Otros Impuestos/Tasas',
    'Monto Propina Legal',
]

# Formato 607 - Ventas
FORMATO_607_COLUMNAS = [
    'RNC/Cédula',
    'Tipo de Identificación',
    'NCF',
    'NCF Modificado',
    'Tipo de Ingreso',
    'Fecha de Comprobante',
    'Fecha de Retención',
    'Monto Facturado',
    'ITBIS Facturado',
    'ITBIS Retenido',
    'ITBIS Percibido',
    'Retención Renta por Terceros',
    'ISR Percibido',
    'Impuesto Selectivo al Consumo',
    'Otros Impuestos/Tasas',
    'Monto Propina Legal',
    'Forma de Pago',
]

# Formato 608 - Anulaciones
FORMATO_608_COLUMNAS = [
    'NCF',
    'Fecha de Emisión',
    'Tipo de Anulación',
]

# ============================================================================
# CONFIGURACIÓN DE API DGII
# ============================================================================

DGII_API_URLS = {
    'test': 'https://ecf-test.dgii.gov.do/',
    'production': 'https://ecf.dgii.gov.do/',
}

# Endpoints de API
DGII_ENDPOINTS = {
    'validar_rnc': '/contribuyentes/validation',
    'enviar_ecf': '/ecf/send',
    'consultar_estado': '/ecf/status',
    'cancelar_ecf': '/ecf/cancel',
    'reenviar_ecf': '/ecf/resend',
}

# ============================================================================
# VALIDACIÓN DE NCF
# ============================================================================

# Formato: A01 + RNC (9 dígitos) + Tipo (2 dígitos) + Secuencia (8 dígitos)
# Ejemplo: A01123456789011234567890
NCF_FORMATO_REGEX = r'^[A-Z]\d{2}\d{9}\d{2}\d{8}$'
NCF_LONGITUD = 19

# Formato RNC: 9 dígitos
RNC_FORMATO_REGEX = r'^\d{9}$'
RNC_LONGITUD = 9

# Formato Cédula: 11 dígitos con guiones (XXX-XXXXXXX-X)
CEDULA_FORMATO_REGEX = r'^\d{3}-\d{7}-\d{1}$'
CEDULA_FORMATO_REGEX_SIN_GUIONES = r'^\d{11}$'

# ============================================================================
# CONFIGURACIÓN DE SECUENCIAS NCF
# ============================================================================

# Longitud de secuencia para NCF
SECUENCIA_NCF_LONGITUD = 8
SECUENCIA_NCF_INICIO = 1
SECUENCIA_NCF_FIN = 99999999

# Días de alerta antes del vencimiento de secuencia NCF
DIAS_ALERTA_VENCIMIENTO_NCF = 30

# ============================================================================
# MONEDAS
# ============================================================================

MONEDAS = {
    'DOP': 'Peso Dominicano',
    'USD': 'Dólar Estadounidense',
    'EUR': 'Euro',
}

MONEDA_DEFAULT = 'DOP'

# ============================================================================
# CONFIGURACIÓN ESPECÍFICA PARA RESTAURANTES Y BARES
# ============================================================================

# Categorías de productos sujetos a propina legal
CATEGORIAS_CON_PROPINA = [
    'alimentos',
    'bebidas',
    'servicio_mesa',
]

# Categorías de bebidas alcohólicas para ISC
CATEGORIAS_BEBIDAS_ALCOHOLICAS = [
    'cerveza',
    'vino',
    'licor',
    'whisky',
    'ron',
    'vodka',
    'tequila',
    'champagne',
    'cocktail',
]

# Límite para gastos menores (NCF tipo 13)
LIMITE_GASTOS_MENORES = Decimal('50000.00')  # RD$ 50,000

# ============================================================================
# CONFIGURACIÓN DE FACTURACIÓN ELECTRÓNICA
# ============================================================================

# Tiempo máximo para envío a DGII (en horas)
TIEMPO_MAX_ENVIO_ECF = 48

# Tiempo de contingencia permitido (en días)
TIEMPO_CONTINGENCIA_PERMITIDO = 7

# Reintentos de envío en caso de fallo
REINTENTOS_ENVIO_ECF = 3
TIEMPO_ENTRE_REINTENTOS = 300  # 5 minutos

# ============================================================================
# CONFIGURACIÓN DE IMPRESIÓN
# ============================================================================

# Información obligatoria en comprobantes
INFO_OBLIGATORIA_COMPROBANTE = [
    'razon_social',
    'rnc',
    'direccion',
    'telefono',
    'ncf',
    'fecha_emision',
    'fecha_vencimiento_ncf',
    'total',
    'itbis',
]

# ============================================================================
# EXPORTAR CONFIGURACIÓN
# ============================================================================

DGII_CONFIG = {
    'tipos_ncf': TIPOS_NCF,
    'tipos_ecf': TIPOS_ECF,
    'tipos_anulacion': TIPOS_ANULACION,
    'tipos_ingreso': TIPOS_INGRESO,
    'tipos_bienes_servicios': TIPOS_BIENES_SERVICIOS,
    'itbis_tasa': ITBIS_TASA,
    'itbis_tasa_reducida': ITBIS_TASA_REDUCIDA,
    'itbis_exento': ITBIS_EXENTO,
    'propina_legal': PROPINA_LEGAL,
    'retencion_isr_servicios': RETENCION_ISR_SERVICIOS,
    'retencion_itbis': RETENCION_ITBIS,
    'isc_bebidas_alcoholicas': ISC_BEBIDAS_ALCOHOLICAS,
    'estados_ncf': ESTADOS_NCF,
    'formas_pago': FORMAS_PAGO,
    'tipos_identificacion': TIPOS_IDENTIFICACION,
    'monedas': MONEDAS,
    'moneda_default': MONEDA_DEFAULT,
    'categorias_con_propina': CATEGORIAS_CON_PROPINA,
    'categorias_bebidas_alcoholicas': CATEGORIAS_BEBIDAS_ALCOHOLICAS,
    'limite_gastos_menores': LIMITE_GASTOS_MENORES,
}
