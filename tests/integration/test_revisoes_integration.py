import pytest
from fastapi.testclient import TestClient

from app.models import StatusAgendamentoEnum, TipoServicoEnum
from app.services.notification import FalhaEnvioNotificacaoError
from tests.factories.carro_factory import CarroFactory


@pytest.mark.integration
class TestAgendamentoRevisaoIntegration:

    def test_deve_criar_revisao_com_sucesso_quando_notificacao_externa_funcionar(
        self, client: TestClient, mocker
    ):
        # Arrange (preparação dos dados sintéticos e mock de sucesso)
        payload = CarroFactory.payload_valido(
            tipo_servico=TipoServicoEnum.TROCA_DE_OLEO
        )
        mock_envio = mocker.patch(
            "app.main.notificacao_service.enviar_confirmacao",
            return_value={"enviado": True, "status": "ENTREGUE"},
        )

        # Act (ação chamando a API)
        response = client.post("/api/revisoes", json=payload)

        # Assert (validação do resultado)
        assert response.status_code == 201
        dados = response.json()
        assert dados["cliente_nome"] == payload["cliente_nome"]
        assert dados["veiculo_placa"] == payload["veiculo_placa"]
        assert dados["tipo_servico"] == payload["tipo_servico"]
        assert dados["status"] == StatusAgendamentoEnum.CONFIRMADO.value
        assert dados["aviso_enviado"] is True

        mock_envio.assert_called_once_with(
            cliente_email=payload["cliente_email"],
            cliente_nome=payload["cliente_nome"],
            veiculo_modelo=payload["veiculo_modelo"],
            veiculo_placa=payload["veiculo_placa"],
            data_horario=payload["data_horario"],
        )

    def test_deve_salvar_revisao_com_aviso_pendente_quando_servico_externo_falhar(
        self, client: TestClient, mocker
    ):
        # Arrange (simula falha de conexão no provedor de mensagens)
        payload = CarroFactory.payload_valido(
            tipo_servico=TipoServicoEnum.REVISAO_PREVENTIVA
        )
        mock_envio = mocker.patch(
            "app.main.notificacao_service.enviar_confirmacao",
            side_effect=FalhaEnvioNotificacaoError("Serviço de SMS indisponível"),
        )

        # Act
        response = client.post("/api/revisoes", json=payload)

        # Assert (o sistema não cai com erro 500, aplica degradação graciosa)
        assert response.status_code == 201
        dados = response.json()
        assert dados["status"] == StatusAgendamentoEnum.PENDENTE_AVISO.value
        assert dados["aviso_enviado"] is False
        assert "pendente" in dados["mensagem_status"]
        mock_envio.assert_called_once()


@pytest.mark.integration
class TestValidacoesRevisaoIntegration:

    def test_deve_rejeitar_revisao_com_data_no_passado(self, client: TestClient):
        # Arrange
        payload = CarroFactory.payload_data_passada()

        # Act
        response = client.post("/api/revisoes", json=payload)

        # Assert
        assert response.status_code == 422
        assert "futura" in str(response.json()["detail"])

    def test_deve_rejeitar_cliente_sem_sobrenome(self, client: TestClient):
        # Arrange
        payload = CarroFactory.payload_nome_invalido()

        # Act
        response = client.post("/api/revisoes", json=payload)

        # Assert
        assert response.status_code == 422
        assert "nome e sobrenome" in str(response.json()["detail"])

    def test_deve_rejeitar_placa_invalida(self, client: TestClient):
        # Arrange
        payload = CarroFactory.payload_placa_invalida()

        # Act
        response = client.post("/api/revisoes", json=payload)

        # Assert
        assert response.status_code == 422
        assert "Placa inválida" in str(response.json()["detail"])


@pytest.mark.integration
class TestListagemECancelamentoIntegration:

    def test_deve_listar_revisoes_cadastradas(self, client: TestClient, mocker):
        # Arrange
        mocker.patch("app.main.notificacao_service.enviar_confirmacao", return_value={"enviado": True})
        p1 = CarroFactory.payload_valido()
        p2 = CarroFactory.payload_valido()
        client.post("/api/revisoes", json=p1)
        client.post("/api/revisoes", json=p2)

        # Act
        response = client.get("/api/revisoes")

        # Assert
        assert response.status_code == 200
        lista = response.json()
        assert len(lista) == 2
        placas = [item["veiculo_placa"] for item in lista]
        assert p1["veiculo_placa"] in placas
        assert p2["veiculo_placa"] in placas

    def test_deve_detalhar_revisao_por_id(self, client: TestClient, mocker):
        # Arrange
        mocker.patch("app.main.notificacao_service.enviar_confirmacao", return_value={"enviado": True})
        p = CarroFactory.payload_valido()
        criado = client.post("/api/revisoes", json=p).json()
        revisao_id = criado["id"]

        # Act
        response = client.get(f"/api/revisoes/{revisao_id}")

        # Assert
        assert response.status_code == 200
        assert response.json()["id"] == revisao_id

    def test_deve_retornar_404_para_revisao_inexistente(self, client: TestClient):
        # Arrange & Act
        response = client.get("/api/revisoes/id-que-nao-existe")

        # Assert
        assert response.status_code == 404

    def test_deve_cancelar_revisao_com_sucesso(self, client: TestClient, mocker):
        # Arrange
        mocker.patch("app.main.notificacao_service.enviar_confirmacao", return_value={"enviado": True})
        p = CarroFactory.payload_valido()
        criado = client.post("/api/revisoes", json=p).json()
        revisao_id = criado["id"]

        # Act
        response = client.patch(f"/api/revisoes/{revisao_id}/cancelar")

        # Assert
        assert response.status_code == 200
        assert response.json()["status"] == StatusAgendamentoEnum.CANCELADO.value

