"""
Serviço de envio de notificações externas para confirmação de agendamentos.
Autor: Lucas Gomes Fagundes (QTS - FATEC Registro)
"""

import time
from typing import Dict, Any


class FalhaEnvioNotificacaoError(Exception):
    """Lançada quando a API externa de mensagens falha (ex: timeout ou fora do ar)."""
    pass


class NotificacaoService:
    """
    Serviço externo que simula o disparo de mensagens (SMS/WhatsApp)
    notificando o cliente sobre o agendamento da revisão do veículo.
    """

    def __init__(self, api_url: str = "https://api.avisos-oficina.fake/v1"):
        self.api_url = api_url

    def enviar_confirmacao(
        self,
        cliente_email: str,
        cliente_nome: str,
        veiculo_modelo: str,
        veiculo_placa: str,
        data_horario: str,
    ) -> Dict[str, Any]:
        # Simula envio para provedor de mensageria externo
        return {
            "enviado": True,
            "id_mensagem": f"msg_oficina_{int(time.time() * 1000)}",
            "destinatario": cliente_email,
            "status": "ENTREGUE",
        }
