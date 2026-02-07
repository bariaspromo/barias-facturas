"""
Cliente para la API de la DGII (Dirección General de Impuestos Internos)
República Dominicana

Este módulo proporciona funciones para interactuar con los servicios de la DGII:
- Validación de RNC
- Envío de comprobantes electrónicos (e-CF)
- Consulta de estado de e-CF
- Cancelación de e-CF
"""

import os
import requests
import logging
from typing import Dict, Optional, Tuple
from datetime import datetime
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)


class DGIIAPIClient:
    """Cliente para la API de la DGII"""
    
    def __init__(self, environment: str = 'test'):
        """
        Inicializa el cliente de la API DGII
        
        Args:
            environment: 'test' o 'production'
        """
        self.environment = environment
        self.base_url = self._get_base_url()
        self.timeout = 30  # segundos
        self.session = requests.Session()
        
    def _get_base_url(self) -> str:
        """Obtiene la URL base según el ambiente"""
        from ..core.config import DGII_API_URLS
        return DGII_API_URLS.get(self.environment, DGII_API_URLS['test'])
    
    def _get_headers(self) -> Dict[str, str]:
        """Obtiene los headers para las peticiones"""
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'BarasERP/1.0',
        }
    
    def _handle_response(self, response: requests.Response) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Maneja la respuesta de la API
        
        Args:
            response: Respuesta HTTP
            
        Returns:
            Tupla (success, data, error_message)
        """
        try:
            response.raise_for_status()
            data = response.json() if response.content else {}
            return True, data, None
        except requests.exceptions.HTTPError as e:
            error_msg = f"Error HTTP {response.status_code}: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg
        except requests.exceptions.RequestException as e:
            error_msg = f"Error de conexión: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg
        except ValueError as e:
            error_msg = f"Error al parsear respuesta JSON: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg
    
    def validar_rnc(self, rnc: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Valida un RNC contra la base de datos de la DGII
        
        Args:
            rnc: Registro Nacional del Contribuyente
            
        Returns:
            Tupla (success, data, error_message)
            data contiene: {
                'rnc': str,
                'nombre': str,
                'nombre_comercial': str,
                'categoria': str,
                'regimen': str,
                'estado': str,
                'actividad_economica': str
            }
        """
        from ..core.config import DGII_ENDPOINTS
        
        endpoint = DGII_ENDPOINTS['validar_rnc']
        url = f"{self.base_url}{endpoint}/{rnc}"
        
        try:
            logger.info(f"Validando RNC: {rnc}")
            response = self.session.get(
                url,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            success, data, error = self._handle_response(response)
            
            if success:
                logger.info(f"RNC {rnc} validado exitosamente")
            else:
                logger.warning(f"Error al validar RNC {rnc}: {error}")
            
            return success, data, error
            
        except Exception as e:
            error_msg = f"Excepción al validar RNC: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg
    
    def enviar_ecf(
        self,
        xml_firmado: str,
        certificado_path: Optional[str] = None,
        certificado_password: Optional[str] = None
    ) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Envía un comprobante fiscal electrónico (e-CF) a la DGII
        
        Args:
            xml_firmado: XML del comprobante firmado digitalmente
            certificado_path: Ruta al certificado digital (.p12)
            certificado_password: Contraseña del certificado
            
        Returns:
            Tupla (success, data, error_message)
            data contiene: {
                'track_id': str,
                'estado': str,
                'fecha_recepcion': str,
                'codigo_seguridad': str
            }
        """
        from ..core.config import DGII_ENDPOINTS
        
        endpoint = DGII_ENDPOINTS['enviar_ecf']
        url = f"{self.base_url}{endpoint}"
        
        try:
            logger.info("Enviando e-CF a DGII")
            
            payload = {
                'xml': xml_firmado,
                'fecha_envio': datetime.now().isoformat()
            }
            
            headers = self._get_headers()
            headers['Content-Type'] = 'application/xml'
            
            response = self.session.post(
                url,
                data=xml_firmado,
                headers=headers,
                timeout=self.timeout,
                # Agregar certificado si está disponible
                cert=(certificado_path, certificado_password) if certificado_path else None
            )
            
            success, data, error = self._handle_response(response)
            
            if success:
                logger.info(f"e-CF enviado exitosamente. Track ID: {data.get('track_id')}")
            else:
                logger.error(f"Error al enviar e-CF: {error}")
            
            return success, data, error
            
        except Exception as e:
            error_msg = f"Excepción al enviar e-CF: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg
    
    def consultar_estado_ecf(self, track_id: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Consulta el estado de un e-CF enviado
        
        Args:
            track_id: ID de seguimiento del e-CF
            
        Returns:
            Tupla (success, data, error_message)
            data contiene: {
                'track_id': str,
                'estado': str,  # 'to_send', 'sent', 'delivered_accepted', 'delivered_refused'
                'fecha_consulta': str,
                'mensaje': str,
                'codigo_seguridad': str (si fue aceptado)
            }
        """
        from ..core.config import DGII_ENDPOINTS
        
        endpoint = DGII_ENDPOINTS['consultar_estado']
        url = f"{self.base_url}{endpoint}/{track_id}"
        
        try:
            logger.info(f"Consultando estado de e-CF: {track_id}")
            
            response = self.session.get(
                url,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            success, data, error = self._handle_response(response)
            
            if success:
                estado = data.get('estado', 'desconocido')
                logger.info(f"Estado de e-CF {track_id}: {estado}")
            else:
                logger.warning(f"Error al consultar estado de e-CF {track_id}: {error}")
            
            return success, data, error
            
        except Exception as e:
            error_msg = f"Excepción al consultar estado de e-CF: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg
    
    def cancelar_ecf(
        self,
        track_id: str,
        motivo: str,
        tipo_anulacion: str
    ) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Cancela un e-CF previamente enviado
        
        Args:
            track_id: ID de seguimiento del e-CF
            motivo: Motivo de la cancelación
            tipo_anulacion: Código de tipo de anulación (01-10)
            
        Returns:
            Tupla (success, data, error_message)
        """
        from ..core.config import DGII_ENDPOINTS
        
        endpoint = DGII_ENDPOINTS['cancelar_ecf']
        url = f"{self.base_url}{endpoint}"
        
        try:
            logger.info(f"Cancelando e-CF: {track_id}")
            
            payload = {
                'track_id': track_id,
                'tipo_anulacion': tipo_anulacion,
                'motivo': motivo,
                'fecha_anulacion': datetime.now().isoformat()
            }
            
            response = self.session.post(
                url,
                json=payload,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            success, data, error = self._handle_response(response)
            
            if success:
                logger.info(f"e-CF {track_id} cancelado exitosamente")
            else:
                logger.error(f"Error al cancelar e-CF {track_id}: {error}")
            
            return success, data, error
            
        except Exception as e:
            error_msg = f"Excepción al cancelar e-CF: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg
    
    def reenviar_ecf(self, track_id: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Reenvía un e-CF que falló en el envío inicial
        
        Args:
            track_id: ID de seguimiento del e-CF
            
        Returns:
            Tupla (success, data, error_message)
        """
        from ..core.config import DGII_ENDPOINTS
        
        endpoint = DGII_ENDPOINTS['reenviar_ecf']
        url = f"{self.base_url}{endpoint}/{track_id}"
        
        try:
            logger.info(f"Reenviando e-CF: {track_id}")
            
            response = self.session.post(
                url,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            success, data, error = self._handle_response(response)
            
            if success:
                logger.info(f"e-CF {track_id} reenviado exitosamente")
            else:
                logger.error(f"Error al reenviar e-CF {track_id}: {error}")
            
            return success, data, error
            
        except Exception as e:
            error_msg = f"Excepción al reenviar e-CF: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg


class DGIIReportGenerator:
    """Generador de reportes DGII (606, 607, 608)"""
    
    @staticmethod
    def generar_formato_606(datos_compras: list) -> str:
        """
        Genera el formato 606 (Compras) en formato TXT
        
        Args:
            datos_compras: Lista de diccionarios con datos de compras
            
        Returns:
            String con el contenido del archivo formato 606
        """
        lineas = []
        
        for compra in datos_compras:
            linea = "|".join([
                compra.get('rnc', ''),
                compra.get('tipo_identificacion', ''),
                compra.get('tipo_bienes_servicios', ''),
                compra.get('ncf', ''),
                compra.get('ncf_modificado', ''),
                compra.get('fecha_comprobante', ''),
                compra.get('fecha_pago', ''),
                str(compra.get('monto_facturado', 0)),
                str(compra.get('itbis_facturado', 0)),
                str(compra.get('itbis_retenido', 0)),
                str(compra.get('itbis_proporcionalidad', 0)),
                str(compra.get('itbis_costo', 0)),
                str(compra.get('itbis_adelantar', 0)),
                str(compra.get('itbis_percibido', 0)),
                compra.get('tipo_retencion_isr', ''),
                str(compra.get('monto_retencion_renta', 0)),
                str(compra.get('isr_percibido', 0)),
                str(compra.get('isc', 0)),
                str(compra.get('otros_impuestos', 0)),
                str(compra.get('propina_legal', 0)),
            ])
            lineas.append(linea)
        
        return "\n".join(lineas)
    
    @staticmethod
    def generar_formato_607(datos_ventas: list) -> str:
        """
        Genera el formato 607 (Ventas) en formato TXT
        
        Args:
            datos_ventas: Lista de diccionarios con datos de ventas
            
        Returns:
            String con el contenido del archivo formato 607
        """
        lineas = []
        
        for venta in datos_ventas:
            linea = "|".join([
                venta.get('rnc', ''),
                venta.get('tipo_identificacion', ''),
                venta.get('ncf', ''),
                venta.get('ncf_modificado', ''),
                venta.get('tipo_ingreso', ''),
                venta.get('fecha_comprobante', ''),
                venta.get('fecha_retencion', ''),
                str(venta.get('monto_facturado', 0)),
                str(venta.get('itbis_facturado', 0)),
                str(venta.get('itbis_retenido', 0)),
                str(venta.get('itbis_percibido', 0)),
                str(venta.get('retencion_renta', 0)),
                str(venta.get('isr_percibido', 0)),
                str(venta.get('isc', 0)),
                str(venta.get('otros_impuestos', 0)),
                str(venta.get('propina_legal', 0)),
                venta.get('forma_pago', ''),
            ])
            lineas.append(linea)
        
        return "\n".join(lineas)
    
    @staticmethod
    def generar_formato_608(datos_anulaciones: list) -> str:
        """
        Genera el formato 608 (Anulaciones) en formato TXT
        
        Args:
            datos_anulaciones: Lista de diccionarios con datos de anulaciones
            
        Returns:
            String con el contenido del archivo formato 608
        """
        lineas = []
        
        for anulacion in datos_anulaciones:
            linea = "|".join([
                anulacion.get('ncf', ''),
                anulacion.get('fecha_emision', ''),
                anulacion.get('tipo_anulacion', ''),
            ])
            lineas.append(linea)
        
        return "\n".join(lineas)


# Funciones de conveniencia
def get_dgii_client(environment: Optional[str] = None) -> DGIIAPIClient:
    """
    Obtiene una instancia del cliente DGII
    
    Args:
        environment: 'test' o 'production'. Si es None, usa la variable de entorno DGII_ENV
        
    Returns:
        Instancia de DGIIAPIClient
    """
    if environment is None:
        environment = os.getenv('DGII_ENV', 'test')
    
    return DGIIAPIClient(environment=environment)
