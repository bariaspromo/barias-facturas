"""
Validador de RNC (Registro Nacional del Contribuyente) y Cédula
para República Dominicana

Este módulo proporciona funciones para validar RNC y Cédulas según
las especificaciones de la DGII.
"""

import re
from typing import Optional, Tuple


class RNCValidator:
    """Validador de RNC (Registro Nacional del Contribuyente)"""
    
    # RNC tiene 9 dígitos
    RNC_REGEX = re.compile(r'^\d{9}$')
    RNC_LENGTH = 9
    
    @staticmethod
    def validar_formato(rnc: str) -> Tuple[bool, Optional[str]]:
        """
        Valida el formato de un RNC
        
        Args:
            rnc: Registro Nacional del Contribuyente
            
        Returns:
            Tupla (es_valido, mensaje_error)
        """
        if not rnc:
            return False, "RNC no puede estar vacío"
        
        # Limpiar espacios y guiones
        rnc_limpio = rnc.strip().replace('-', '').replace(' ', '')
        
        # Validar longitud
        if len(rnc_limpio) != RNCValidator.RNC_LENGTH:
            return False, f"RNC debe tener {RNCValidator.RNC_LENGTH} dígitos"
        
        # Validar que sean solo números
        if not RNCValidator.RNC_REGEX.match(rnc_limpio):
            return False, "RNC debe contener solo dígitos"
        
        return True, None
    
    @staticmethod
    def limpiar(rnc: str) -> str:
        """
        Limpia un RNC removiendo espacios y guiones
        
        Args:
            rnc: RNC a limpiar
            
        Returns:
            RNC limpio (solo dígitos)
        """
        return rnc.strip().replace('-', '').replace(' ', '')
    
    @staticmethod
    def formatear(rnc: str) -> Optional[str]:
        """
        Formatea un RNC agregando guiones para mejor legibilidad
        Formato: XXX-XXXXX-X
        
        Args:
            rnc: RNC a formatear
            
        Returns:
            RNC formateado o None si es inválido
        """
        es_valido, _ = RNCValidator.validar_formato(rnc)
        if not es_valido:
            return None
        
        rnc_limpio = RNCValidator.limpiar(rnc)
        return f"{rnc_limpio[0:3]}-{rnc_limpio[3:8]}-{rnc_limpio[8]}"


class CedulaValidator:
    """Validador de Cédula de Identidad dominicana"""
    
    # Cédula tiene 11 dígitos
    CEDULA_REGEX = re.compile(r'^\d{11}$')
    CEDULA_REGEX_CON_GUIONES = re.compile(r'^\d{3}-\d{7}-\d{1}$')
    CEDULA_LENGTH = 11
    
    @staticmethod
    def validar_formato(cedula: str) -> Tuple[bool, Optional[str]]:
        """
        Valida el formato de una cédula
        
        Args:
            cedula: Cédula de identidad
            
        Returns:
            Tupla (es_valido, mensaje_error)
        """
        if not cedula:
            return False, "Cédula no puede estar vacía"
        
        cedula = cedula.strip()
        
        # Verificar formato con guiones
        if CedulaValidator.CEDULA_REGEX_CON_GUIONES.match(cedula):
            return CedulaValidator._validar_digito_verificador(cedula)
        
        # Verificar formato sin guiones
        cedula_limpia = cedula.replace('-', '').replace(' ', '')
        
        if len(cedula_limpia) != CedulaValidator.CEDULA_LENGTH:
            return False, f"Cédula debe tener {CedulaValidator.CEDULA_LENGTH} dígitos"
        
        if not CedulaValidator.CEDULA_REGEX.match(cedula_limpia):
            return False, "Cédula debe contener solo dígitos"
        
        # Validar dígito verificador
        return CedulaValidator._validar_digito_verificador(cedula_limpia)
    
    @staticmethod
    def _validar_digito_verificador(cedula: str) -> Tuple[bool, Optional[str]]:
        """
        Valida el dígito verificador de la cédula usando el algoritmo de Luhn modificado
        
        Args:
            cedula: Cédula (puede tener o no guiones)
            
        Returns:
            Tupla (es_valido, mensaje_error)
        """
        cedula_limpia = cedula.replace('-', '').replace(' ', '')
        
        if len(cedula_limpia) != 11:
            return False, "Cédula debe tener 11 dígitos"
        
        # Los primeros 10 dígitos
        digitos = cedula_limpia[:10]
        # El último dígito es el verificador
        digito_verificador = int(cedula_limpia[10])
        
        # Calcular suma ponderada
        suma = 0
        pesos = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
        
        for i, digito in enumerate(digitos):
            producto = int(digito) * pesos[i]
            # Si el producto es mayor a 9, sumar sus dígitos
            if producto > 9:
                producto = (producto // 10) + (producto % 10)
            suma += producto
        
        # El dígito verificador debe hacer que la suma sea múltiplo de 10
        verificador_calculado = (10 - (suma % 10)) % 10
        
        if verificador_calculado != digito_verificador:
            return False, "Dígito verificador de cédula inválido"
        
        return True, None
    
    @staticmethod
    def limpiar(cedula: str) -> str:
        """
        Limpia una cédula removiendo espacios y guiones
        
        Args:
            cedula: Cédula a limpiar
            
        Returns:
            Cédula limpia (solo dígitos)
        """
        return cedula.strip().replace('-', '').replace(' ', '')
    
    @staticmethod
    def formatear(cedula: str) -> Optional[str]:
        """
        Formatea una cédula agregando guiones
        Formato: XXX-XXXXXXX-X
        
        Args:
            cedula: Cédula a formatear
            
        Returns:
            Cédula formateada o None si es inválida
        """
        es_valida, _ = CedulaValidator.validar_formato(cedula)
        if not es_valida:
            return None
        
        cedula_limpia = CedulaValidator.limpiar(cedula)
        return f"{cedula_limpia[0:3]}-{cedula_limpia[3:10]}-{cedula_limpia[10]}"


class IdentificacionValidator:
    """Validador genérico que detecta y valida RNC o Cédula"""
    
    @staticmethod
    def detectar_tipo(identificacion: str) -> Optional[str]:
        """
        Detecta si una identificación es RNC o Cédula
        
        Args:
            identificacion: Número de identificación
            
        Returns:
            'rnc', 'cedula' o None si no se puede determinar
        """
        identificacion_limpia = identificacion.strip().replace('-', '').replace(' ', '')
        
        if len(identificacion_limpia) == 9:
            return 'rnc'
        elif len(identificacion_limpia) == 11:
            return 'cedula'
        else:
            return None
    
    @staticmethod
    def validar(identificacion: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Valida una identificación (RNC o Cédula) detectando automáticamente el tipo
        
        Args:
            identificacion: Número de identificación
            
        Returns:
            Tupla (es_valido, tipo, mensaje_error)
            donde tipo es 'rnc', 'cedula' o None
        """
        tipo = IdentificacionValidator.detectar_tipo(identificacion)
        
        if tipo == 'rnc':
            es_valido, error = RNCValidator.validar_formato(identificacion)
            return es_valido, 'rnc', error
        elif tipo == 'cedula':
            es_valido, error = CedulaValidator.validar_formato(identificacion)
            return es_valido, 'cedula', error
        else:
            return False, None, "Formato de identificación no reconocido (debe ser RNC de 9 dígitos o Cédula de 11 dígitos)"
    
    @staticmethod
    def limpiar(identificacion: str) -> str:
        """
        Limpia una identificación removiendo espacios y guiones
        
        Args:
            identificacion: Identificación a limpiar
            
        Returns:
            Identificación limpia (solo dígitos)
        """
        return identificacion.strip().replace('-', '').replace(' ', '')
    
    @staticmethod
    def formatear(identificacion: str) -> Optional[str]:
        """
        Formatea una identificación agregando guiones según su tipo
        
        Args:
            identificacion: Identificación a formatear
            
        Returns:
            Identificación formateada o None si es inválida
        """
        tipo = IdentificacionValidator.detectar_tipo(identificacion)
        
        if tipo == 'rnc':
            return RNCValidator.formatear(identificacion)
        elif tipo == 'cedula':
            return CedulaValidator.formatear(identificacion)
        else:
            return None


# Funciones de conveniencia
def validar_rnc(rnc: str) -> bool:
    """
    Valida un RNC
    
    Args:
        rnc: Registro Nacional del Contribuyente
        
    Returns:
        True si es válido
    """
    es_valido, _ = RNCValidator.validar_formato(rnc)
    return es_valido


def validar_cedula(cedula: str) -> bool:
    """
    Valida una cédula
    
    Args:
        cedula: Cédula de identidad
        
    Returns:
        True si es válida
    """
    es_valida, _ = CedulaValidator.validar_formato(cedula)
    return es_valida


def validar_identificacion(identificacion: str) -> Tuple[bool, Optional[str]]:
    """
    Valida una identificación (RNC o Cédula) detectando automáticamente el tipo
    
    Args:
        identificacion: Número de identificación
        
    Returns:
        Tupla (es_valido, tipo) donde tipo es 'rnc' o 'cedula'
    """
    es_valido, tipo, _ = IdentificacionValidator.validar(identificacion)
    return es_valido, tipo


def formatear_identificacion(identificacion: str) -> Optional[str]:
    """
    Formatea una identificación (RNC o Cédula) con guiones
    
    Args:
        identificacion: Número de identificación
        
    Returns:
        Identificación formateada o None si es inválida
    """
    return IdentificacionValidator.formatear(identificacion)
