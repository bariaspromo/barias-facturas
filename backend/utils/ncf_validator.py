"""
Validador de NCF (Número de Comprobante Fiscal) y e-NCF
para República Dominicana

Este módulo proporciona funciones para validar NCF y e-NCF según
las especificaciones de la DGII.
"""

import re
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple


class NCFValidator:
    """Validador de Números de Comprobante Fiscal (NCF)"""
    
    # Formato NCF: A01 + RNC (9 dígitos) + Tipo (2 dígitos) + Secuencia (8 dígitos)
    NCF_REGEX = re.compile(r'^[A-Z]\d{2}\d{9}\d{2}\d{8}$')
    NCF_LENGTH = 19
    
    # Tipos de NCF válidos
    TIPOS_VALIDOS = [
        '01', '02', '03', '04', '11', '12', '13', 
        '14', '15', '16', '17'
    ]
    
    # Tipos de e-NCF válidos
    TIPOS_ECF_VALIDOS = [
        '31', '32', '33', '34', '41', '43', '44',
        '45', '46', '47'
    ]
    
    @staticmethod
    def validar_formato(ncf: str) -> Tuple[bool, Optional[str]]:
        """
        Valida el formato de un NCF
        
        Args:
            ncf: Número de comprobante fiscal
            
        Returns:
            Tupla (es_valido, mensaje_error)
        """
        if not ncf:
            return False, "NCF no puede estar vacío"
        
        ncf = ncf.strip().upper()
        
        # Validar longitud
        if len(ncf) != NCFValidator.NCF_LENGTH:
            return False, f"NCF debe tener {NCFValidator.NCF_LENGTH} caracteres"
        
        # Validar formato con regex
        if not NCFValidator.NCF_REGEX.match(ncf):
            return False, "Formato de NCF inválido. Debe ser: A01 + RNC(9) + Tipo(2) + Secuencia(8)"
        
        # Extraer y validar tipo
        tipo = ncf[12:14]
        todos_tipos = NCFValidator.TIPOS_VALIDOS + NCFValidator.TIPOS_ECF_VALIDOS
        
        if tipo not in todos_tipos:
            return False, f"Tipo de NCF '{tipo}' no es válido"
        
        return True, None
    
    @staticmethod
    def extraer_componentes(ncf: str) -> Optional[Dict[str, str]]:
        """
        Extrae los componentes de un NCF
        
        Args:
            ncf: Número de comprobante fiscal
            
        Returns:
            Diccionario con componentes o None si es inválido
        """
        es_valido, error = NCFValidator.validar_formato(ncf)
        
        if not es_valido:
            return None
        
        ncf = ncf.strip().upper()
        
        return {
            'serie': ncf[0:3],          # Ej: A01
            'rnc': ncf[3:12],           # 9 dígitos
            'tipo': ncf[12:14],         # 2 dígitos
            'secuencia': ncf[14:22],    # 8 dígitos
            'es_electronico': ncf[12:14] in NCFValidator.TIPOS_ECF_VALIDOS
        }
    
    @staticmethod
    def es_electronico(ncf: str) -> bool:
        """
        Determina si un NCF es electrónico
        
        Args:
            ncf: Número de comprobante fiscal
            
        Returns:
            True si es e-NCF, False en caso contrario
        """
        componentes = NCFValidator.extraer_componentes(ncf)
        if componentes:
            return componentes['es_electronico']
        return False
    
    @staticmethod
    def obtener_tipo_descripcion(ncf: str) -> Optional[str]:
        """
        Obtiene la descripción del tipo de NCF
        
        Args:
            ncf: Número de comprobante fiscal
            
        Returns:
            Descripción del tipo o None si es inválido
        """
        from ..core.config import TIPOS_NCF, TIPOS_ECF
        
        componentes = NCFValidator.extraer_componentes(ncf)
        if not componentes:
            return None
        
        tipo = componentes['tipo']
        
        if componentes['es_electronico']:
            return TIPOS_ECF.get(tipo, 'Tipo desconocido')
        else:
            return TIPOS_NCF.get(tipo, 'Tipo desconocido')
    
    @staticmethod
    def validar_secuencia(ncf: str, secuencia_inicio: int, secuencia_fin: int) -> Tuple[bool, Optional[str]]:
        """
        Valida que la secuencia del NCF esté dentro del rango autorizado
        
        Args:
            ncf: Número de comprobante fiscal
            secuencia_inicio: Secuencia inicial autorizada
            secuencia_fin: Secuencia final autorizada
            
        Returns:
            Tupla (es_valido, mensaje_error)
        """
        componentes = NCFValidator.extraer_componentes(ncf)
        if not componentes:
            return False, "NCF inválido"
        
        secuencia = int(componentes['secuencia'])
        
        if secuencia < secuencia_inicio:
            return False, f"Secuencia {secuencia} es menor que el inicio autorizado {secuencia_inicio}"
        
        if secuencia > secuencia_fin:
            return False, f"Secuencia {secuencia} excede el fin autorizado {secuencia_fin}"
        
        return True, None
    
    @staticmethod
    def validar_vencimiento(fecha_vencimiento: datetime) -> Tuple[bool, Optional[str]]:
        """
        Valida que un NCF no esté vencido
        
        Args:
            fecha_vencimiento: Fecha de vencimiento de la secuencia NCF
            
        Returns:
            Tupla (es_valido, mensaje_error)
        """
        hoy = datetime.now().date()
        
        if fecha_vencimiento.date() < hoy:
            return False, f"NCF vencido desde {fecha_vencimiento.date()}"
        
        # Advertencia si está próximo a vencer (30 días)
        dias_restantes = (fecha_vencimiento.date() - hoy).days
        if dias_restantes <= 30:
            return True, f"Advertencia: NCF vence en {dias_restantes} días"
        
        return True, None
    
    @staticmethod
    def generar_siguiente_ncf(serie: str, rnc: str, tipo: str, secuencia_actual: int) -> str:
        """
        Genera el siguiente NCF en la secuencia
        
        Args:
            serie: Serie del NCF (ej: A01)
            rnc: RNC del emisor (9 dígitos)
            tipo: Tipo de comprobante (2 dígitos)
            secuencia_actual: Secuencia actual
            
        Returns:
            Siguiente NCF en formato completo
        """
        siguiente_secuencia = secuencia_actual + 1
        secuencia_str = str(siguiente_secuencia).zfill(8)
        
        return f"{serie}{rnc}{tipo}{secuencia_str}"
    
    @staticmethod
    def validar_ncf_completo(
        ncf: str,
        rnc_emisor: str,
        secuencia_inicio: int,
        secuencia_fin: int,
        fecha_vencimiento: datetime
    ) -> Tuple[bool, list]:
        """
        Realiza validación completa de un NCF
        
        Args:
            ncf: Número de comprobante fiscal
            rnc_emisor: RNC del emisor
            secuencia_inicio: Secuencia inicial autorizada
            secuencia_fin: Secuencia final autorizada
            fecha_vencimiento: Fecha de vencimiento
            
        Returns:
            Tupla (es_valido, lista_de_mensajes)
        """
        mensajes = []
        es_valido = True
        
        # Validar formato
        valido_formato, error_formato = NCFValidator.validar_formato(ncf)
        if not valido_formato:
            mensajes.append(error_formato)
            return False, mensajes
        
        # Validar RNC coincide
        componentes = NCFValidator.extraer_componentes(ncf)
        if componentes['rnc'] != rnc_emisor.zfill(9):
            mensajes.append(f"RNC en NCF ({componentes['rnc']}) no coincide con RNC emisor ({rnc_emisor})")
            es_valido = False
        
        # Validar secuencia
        valido_secuencia, error_secuencia = NCFValidator.validar_secuencia(
            ncf, secuencia_inicio, secuencia_fin
        )
        if not valido_secuencia:
            mensajes.append(error_secuencia)
            es_valido = False
        
        # Validar vencimiento
        valido_vencimiento, mensaje_vencimiento = NCFValidator.validar_vencimiento(fecha_vencimiento)
        if not valido_vencimiento:
            mensajes.append(mensaje_vencimiento)
            es_valido = False
        elif mensaje_vencimiento:  # Advertencia
            mensajes.append(mensaje_vencimiento)
        
        if es_valido and not mensajes:
            mensajes.append("NCF válido")
        
        return es_valido, mensajes


class SecuenciaNCF:
    """Gestión de secuencias de NCF"""
    
    @staticmethod
    def calcular_disponibles(secuencia_actual: int, secuencia_fin: int) -> int:
        """
        Calcula cuántos NCF quedan disponibles en la secuencia
        
        Args:
            secuencia_actual: Secuencia actual utilizada
            secuencia_fin: Secuencia final autorizada
            
        Returns:
            Cantidad de NCF disponibles
        """
        return secuencia_fin - secuencia_actual
    
    @staticmethod
    def calcular_porcentaje_uso(secuencia_actual: int, secuencia_inicio: int, secuencia_fin: int) -> float:
        """
        Calcula el porcentaje de uso de la secuencia
        
        Args:
            secuencia_actual: Secuencia actual utilizada
            secuencia_inicio: Secuencia inicial autorizada
            secuencia_fin: Secuencia final autorizada
            
        Returns:
            Porcentaje de uso (0-100)
        """
        total = secuencia_fin - secuencia_inicio + 1
        usados = secuencia_actual - secuencia_inicio + 1
        
        return (usados / total) * 100 if total > 0 else 0
    
    @staticmethod
    def necesita_reorden(
        secuencia_actual: int,
        secuencia_fin: int,
        umbral_minimo: int = 100
    ) -> bool:
        """
        Determina si se necesita solicitar nueva secuencia de NCF
        
        Args:
            secuencia_actual: Secuencia actual utilizada
            secuencia_fin: Secuencia final autorizada
            umbral_minimo: Cantidad mínima de NCF antes de alertar
            
        Returns:
            True si necesita reorden
        """
        disponibles = SecuenciaNCF.calcular_disponibles(secuencia_actual, secuencia_fin)
        return disponibles <= umbral_minimo


# Funciones de conveniencia
def validar_ncf(ncf: str) -> bool:
    """
    Valida el formato de un NCF
    
    Args:
        ncf: Número de comprobante fiscal
        
    Returns:
        True si es válido, False en caso contrario
    """
    es_valido, _ = NCFValidator.validar_formato(ncf)
    return es_valido


def es_ncf_electronico(ncf: str) -> bool:
    """
    Determina si un NCF es electrónico
    
    Args:
        ncf: Número de comprobante fiscal
        
    Returns:
        True si es e-NCF
    """
    return NCFValidator.es_electronico(ncf)


def obtener_info_ncf(ncf: str) -> Optional[Dict[str, str]]:
    """
    Obtiene información de un NCF
    
    Args:
        ncf: Número de comprobante fiscal
        
    Returns:
        Diccionario con información del NCF
    """
    componentes = NCFValidator.extraer_componentes(ncf)
    if not componentes:
        return None
    
    return {
        **componentes,
        'descripcion_tipo': NCFValidator.obtener_tipo_descripcion(ncf)
    }
