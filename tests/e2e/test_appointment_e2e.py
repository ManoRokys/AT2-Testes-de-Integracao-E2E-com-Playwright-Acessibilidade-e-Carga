import pytest
from playwright.sync_api import Page, expect

from tests.factories.appointment_factory import AgendamentoFactory
from tests.e2e.pages.appointment_page import AppointmentPage


@pytest.mark.e2e
class TestAppointmentE2E:
    """Suíte de testes End-to-End (E2E) com Playwright e Page Object Model."""

    def test_fluxo_completo_agendamento_e_listagem(self, page: Page, live_server_url: str):
        """
        Testa o fluxo ponta a ponta:
        1. Acessa a página web da clínica médica.
        2. Preenche o formulário usando dados sintéticos gerados pela Factory (Faker pt_BR).
        3. Submete o formulário via clique no botão.
        4. Valida a exibição do alerta de sucesso na interface.
        5. Valida a inclusão da consulta na tabela de agendamentos.
        """
        # ==================== ARRANGE ====================
        dados = AgendamentoFactory.build_valid_payload(dias_a_frente=7)
        appointment_page = AppointmentPage(page, live_server_url)

        # ==================== ACT ====================
        appointment_page.navigate()

        # Valida carregamento inicial dos títulos
        expect(appointment_page.heading).to_be_visible()
        expect(appointment_page.form_heading).to_be_visible()

        # Preenchimento e submissão através do Page Object
        appointment_page.fill_form(
            nome=dados["paciente_nome"],
            email=dados["paciente_email"],
            telefone=dados["paciente_telefone"],
            especialidade=dados["especialidade"],
            data_horario_iso=dados["data_horario"],
            observacoes=dados["observacoes"]
        )
        appointment_page.submit_form()

        # ==================== ASSERT ====================
        # Valida a mensagem de sucesso via seletores semânticos
        alerta = page.locator("#alert-status")
        expect(alerta).to_be_visible()
        expect(alerta).to_contain_text("Agendamento realizado com sucesso!")

        # Valida a presença do registro na tabela
        linha = appointment_page.get_row_by_patient_name(dados["paciente_nome"])
        expect(linha).to_be_visible()
        expect(linha).to_contain_text(dados["especialidade"])
        expect(linha).to_contain_text("CONFIRMADO")

    def test_cancelamento_de_agendamento_pela_interface(self, page: Page, live_server_url: str):
        """
        Testa o cancelamento de uma consulta diretamente na interface gráfica.
        """
        # ==================== ARRANGE ====================
        dados = AgendamentoFactory.build_valid_payload(dias_a_frente=10)
        appointment_page = AppointmentPage(page, live_server_url)
        appointment_page.navigate()

        appointment_page.fill_form(
            nome=dados["paciente_nome"],
            email=dados["paciente_email"],
            telefone=dados["paciente_telefone"],
            especialidade=dados["especialidade"],
            data_horario_iso=dados["data_horario"]
        )
        appointment_page.submit_form()

        linha = appointment_page.get_row_by_patient_name(dados["paciente_nome"])
        expect(linha).to_be_visible()

        # Configura diálogo para confirmar automaticamente o confirm() do navegador
        page.on("dialog", lambda dialog: dialog.accept())

        # ==================== ACT ====================
        btn_cancelar = linha.get_by_role("button", name="Cancelar")
        btn_cancelar.click()

        # ==================== ASSERT ====================
        expect(linha).to_contain_text("CANCELADO")

