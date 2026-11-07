import pytest
from fastapi.testclient import TestClient

from app.models import StatusAgendamentoEnum, EspecialidadeEnum
from app.services.notification import NotificationDeliveryError
from tests.factories.appointment_factory import AgendamentoFactory


@pytest.mark.integration
class TestCriacaoAgendamentoIntegration:
    """Suíte de testes de integração para o fluxo de criação de agendamentos."""

    def test_deve_criar_agendamento_com_sucesso_quando_notificacao_externa_responder_ok(
        self, client: TestClient, mocker
    ):
        """
        Cenário: Notificação externa bem-sucedida.
        Valida: Padrão AAA, Mock de sucesso no serviço externo, status HTTP 201 e payload.
        """
        # ==================== ARRANGE ====================
        payload = AgendamentoFactory.build_valid_payload(
            especialidade=EspecialidadeEnum.CARDIOLOGIA
        )

        mock_send = mocker.patch(
            "app.main.notification_client.send_confirmation",
            return_value={
                "success": True,
                "message_id": "msg_mock_12345",
                "recipient": payload["paciente_email"],
                "status": "DELIVERED",
            },
        )

        # ==================== ACT ====================
        response = client.post("/api/agendamentos", json=payload)

        # ==================== ASSERT ====================
        assert response.status_code == 201
        data = response.json()

        assert "id" in data
        assert data["paciente_nome"] == payload["paciente_nome"]
        assert data["paciente_email"] == payload["paciente_email"]
        assert data["especialidade"] == payload["especialidade"]
        assert data["status"] == StatusAgendamentoEnum.CONFIRMADO.value
        assert data["notificacao_enviada"] is True
        assert data["mensagem_status"] == "Agendamento confirmado com sucesso."

        # Verifica se a dependência externa mockada foi chamada com os parâmetros corretos
        mock_send.assert_called_once_with(
            paciente_email=payload["paciente_email"],
            paciente_nome=payload["paciente_nome"],
            especialidade=payload["especialidade"],
            data_horario=payload["data_horario"],
        )

    def test_deve_registrar_agendamento_com_degradacao_graciosa_quando_notificacao_externa_falhar(
        self, client: TestClient, mocker
    ):
        """
        Cenário: Notificação externa lança exceção (falha de rede / gateway offline).
        Valida: Mock com side_effect de falha, resiliência do sistema e status PENDENTE_NOTIFICACAO.
        """
        # ==================== ARRANGE ====================
        payload = AgendamentoFactory.build_valid_payload(
            especialidade=EspecialidadeEnum.DERMATOLOGIA
        )

        mock_send = mocker.patch(
            "app.main.notification_client.send_confirmation",
            side_effect=NotificationDeliveryError("Gateway de mensageria indisponível (HTTP 503)")
        )

        # ==================== ACT ====================
        response = client.post("/api/agendamentos", json=payload)

        # ==================== ASSERT ====================
        assert response.status_code == 201
        data = response.json()

        assert "id" in data
        assert data["paciente_nome"] == payload["paciente_nome"]
        assert data["status"] == StatusAgendamentoEnum.PENDENTE_NOTIFICACAO.value
        assert data["notificacao_enviada"] is False
        assert "pendente de envio" in data["mensagem_status"]

        mock_send.assert_called_once()


@pytest.mark.integration
class TestValidacoesAgendamentoIntegration:
    """Suíte de testes de integração para validação de regras de negócio e esquemas Pydantic."""

    def test_deve_rejeitar_agendamento_com_data_no_passado(self, client: TestClient):
        # ==================== ARRANGE ====================
        payload_invalido = AgendamentoFactory.build_invalid_payload_past_date()

        # ==================== ACT ====================
        response = client.post("/api/agendamentos", json=payload_invalido)

        # ==================== ASSERT ====================
        assert response.status_code == 422
        data = response.json()
        detalhe_erros = str(data["detail"])
        assert "devem ser futuros" in detalhe_erros

    def test_deve_rejeitar_agendamento_com_nome_sem_sobrenome(self, client: TestClient):
        # ==================== ARRANGE ====================
        payload_invalido = AgendamentoFactory.build_invalid_payload_single_name()

        # ==================== ACT ====================
        response = client.post("/api/agendamentos", json=payload_invalido)

        # ==================== ASSERT ====================
        assert response.status_code == 422
        data = response.json()
        assert "nome e sobrenome" in str(data["detail"])

    def test_deve_rejeitar_agendamento_com_email_invalido(self, client: TestClient):
        # ==================== ARRANGE ====================
        payload_invalido = AgendamentoFactory.build_invalid_payload_email()

        # ==================== ACT ====================
        response = client.post("/api/agendamentos", json=payload_invalido)

        # ==================== ASSERT ====================
        assert response.status_code == 422


@pytest.mark.integration
class TestConsultaECancelamentoIntegration:
    """Suíte de testes de integração para leitura, busca por ID e cancelamento."""

    def test_deve_listar_agendamentos_cadastrados(self, client: TestClient, mocker):
        # ==================== ARRANGE ====================
        mocker.patch("app.main.notification_client.send_confirmation", return_value={"success": True})
        payload_1 = AgendamentoFactory.build_valid_payload()
        payload_2 = AgendamentoFactory.build_valid_payload()

        client.post("/api/agendamentos", json=payload_1)
        client.post("/api/agendamentos", json=payload_2)

        # ==================== ACT ====================
        response = client.get("/api/agendamentos")

        # ==================== ASSERT ====================
        assert response.status_code == 200
        lista = response.json()
        assert len(lista) == 2
        nomes = [item["paciente_nome"] for item in lista]
        assert payload_1["paciente_nome"] in nomes
        assert payload_2["paciente_nome"] in nomes

    def test_deve_buscar_agendamento_por_id_com_sucesso(self, client: TestClient, mocker):
        # ==================== ARRANGE ====================
        mocker.patch("app.main.notification_client.send_confirmation", return_value={"success": True})
        payload = AgendamentoFactory.build_valid_payload()
        created = client.post("/api/agendamentos", json=payload).json()
        agendamento_id = created["id"]

        # ==================== ACT ====================
        response = client.get(f"/api/agendamentos/{agendamento_id}")

        # ==================== ASSERT ====================
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == agendamento_id
        assert data["paciente_nome"] == payload["paciente_nome"]

    def test_deve_retornar_404_quando_agendamento_nao_existir(self, client: TestClient):
        # ==================== ARRANGE ====================
        id_inexistente = "uuid-inexistente-12345"

        # ==================== ACT ====================
        response = client.get(f"/api/agendamentos/{id_inexistente}")

        # ==================== ASSERT ====================
        assert response.status_code == 404
        assert "não encontrado" in response.json()["detail"]

    def test_deve_cancelar_agendamento_com_sucesso(self, client: TestClient, mocker):
        # ==================== ARRANGE ====================
        mocker.patch("app.main.notification_client.send_confirmation", return_value={"success": True})
        payload = AgendamentoFactory.build_valid_payload()
        created = client.post("/api/agendamentos", json=payload).json()
        agendamento_id = created["id"]

        # ==================== ACT ====================
        response = client.patch(f"/api/agendamentos/{agendamento_id}/cancelar")

        # ==================== ASSERT ====================
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == StatusAgendamentoEnum.CANCELADO.value
        assert "cancelado com sucesso" in data["mensagem_status"]

