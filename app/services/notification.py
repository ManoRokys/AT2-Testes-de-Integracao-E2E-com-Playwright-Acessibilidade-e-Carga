import logging
import time
from typing import Dict, Any

logger = logging.getLogger(__name__)


class NotificationDeliveryError(Exception):
    """Exceção levantada quando a integração externa de notificação falha."""
    pass


class ExternalNotificationClient:
    """
    Cliente de integração com serviço externo de notificações (SMS/E-mail/WhatsApp).
    Em ambiente de produção, este componente se comunica via HTTP com APIs como SendGrid ou Twilio.
    Em testes de integração, este serviço é isolado e mockado via pytest-mock (mocker.patch).
    """

    def __init__(self, api_key: str = "live_secret_key_mock"):
        self.api_key = api_key

    def send_confirmation(
        self,
        paciente_email: str,
        paciente_nome: str,
        especialidade: str,
        data_horario: str
    ) -> Dict[str, Any]:
        """
        Dispara a mensagem de confirmação para o paciente.
        Simula latência de rede e retorno estruturado.
        """
        logger.info(
            f"[NotificationClient] Enviando confirmação para {paciente_email} - Paciente: {paciente_nome}"
        )
        # Simulação de envio com sucesso padrão
        return {
            "success": True,
            "message_id": f"msg_{int(time.time() * 1000)}",
            "recipient": paciente_email,
            "status": "DELIVERED"
        }

