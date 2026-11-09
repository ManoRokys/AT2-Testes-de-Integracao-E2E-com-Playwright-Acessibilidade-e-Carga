"""
Testes End-to-End com Playwright simulando jornada de usuário na oficina AutoCar.
Autor: Lucas Gomes Fagundes (QTS - FATEC Registro)
"""

import pytest
from playwright.sync_api import Page, expect

from tests.factories.carro_factory import CarroFactory
from tests.e2e.pages.revisao_page import RevisaoPage


@pytest.mark.e2e
class TestRevisaoE2E:

    def test_fluxo_completo_agendamento_de_carro(self, page: Page, live_server_url: str):
        # 1. Arrange: dados sintéticos do carro e motorista
        dados = CarroFactory.payload_valido(dias_a_frente=5)
        revisao_page = RevisaoPage(page, live_server_url)

        # 2. Act: abre a página e preenche o formulário
        revisao_page.abrir()
        expect(revisao_page.titulo_principal).to_be_visible()

        revisao_page.preencher_e_enviar(
            nome=dados["cliente_nome"],
            email=dados["cliente_email"],
            telefone=dados["cliente_telefone"],
            modelo=dados["veiculo_modelo"],
            placa=dados["veiculo_placa"],
            servico=dados["tipo_servico"],
            data_iso=dados["data_horario"],
            observacoes=dados["observacoes"],
        )

        # 3. Assert: valida mensagem de sucesso e linha na tabela
        alerta = page.locator("#alert-status")
        expect(alerta).to_be_visible()
        expect(alerta).to_contain_text("Agendamento de revisão realizado com sucesso!")

        linha = revisao_page.obter_linha_por_placa(dados["veiculo_placa"])
        expect(linha).to_be_visible()
        expect(linha).to_contain_text(dados["cliente_nome"])
        expect(linha).to_contain_text(dados["tipo_servico"])
        expect(linha).to_contain_text("CONFIRMADO")

    def test_cancelar_revisao_pela_interface(self, page: Page, live_server_url: str):
        dados = CarroFactory.payload_valido(dias_a_frente=7)
        revisao_page = RevisaoPage(page, live_server_url)
        revisao_page.abrir()

        revisao_page.preencher_e_enviar(
            nome=dados["cliente_nome"],
            email=dados["cliente_email"],
            telefone=dados["cliente_telefone"],
            modelo=dados["veiculo_modelo"],
            placa=dados["veiculo_placa"],
            servico=dados["tipo_servico"],
            data_iso=dados["data_horario"],
        )

        linha = revisao_page.obter_linha_por_placa(dados["veiculo_placa"])
        expect(linha).to_be_visible()

        # Aceita a confirmação do navegador automaticamente
        page.on("dialog", lambda dialog: dialog.accept())

        botao_cancelar = linha.get_by_role("button", name="Cancelar")
        botao_cancelar.click()

        expect(linha).to_contain_text("CANCELADO")

