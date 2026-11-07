import pytest
from playwright.sync_api import Page, expect
from axe_playwright_python.sync_playwright import Axe


@pytest.mark.accessibility
class TestAcessibilidadeWCAG:
    """Auditoria WCAG 2.1 AA e teste de foco de teclado na página da AutoCar."""

    def test_auditoria_axe_wcag_21_aa(self, page: Page, live_server_url: str):
        page.goto(live_server_url)
        page.wait_for_load_state("networkidle")

        axe = Axe()
        resultados = axe.run(
            page,
            options={
                "runOnly": {
                    "type": "tag",
                    "values": ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]
                }
            }
        )
        assert resultados.violations_count == 0, (
            f"Violações de acessibilidade encontradas:\n{resultados.generate_report()}"
        )

    def test_navegacao_por_teclado_tab(self, page: Page, live_server_url: str):
        page.goto(live_server_url)
        page.wait_for_load_state("networkidle")

        # Elementos esperados no ciclo de tabulação
        skip_link = page.locator(".skip-link")
        campo_nome = page.get_by_label("Nome do Cliente")
        campo_email = page.get_by_label("E-mail")
        campo_telefone = page.get_by_label("Telefone")
        campo_modelo = page.get_by_label("Modelo do Carro")
        campo_placa = page.get_by_label("Placa do Veículo")
        campo_servico = page.get_by_label("Tipo de Serviço")
        campo_data = page.get_by_label("Data e Horário")
        campo_obs = page.get_by_label("Observações do Veículo")
        botao_submit = page.get_by_role("button", name="Confirmar Agendamento")

        # Sequência de tabs e asserções to_be_focused()
        page.keyboard.press("Tab")
        expect(skip_link).to_be_focused()

        page.keyboard.press("Tab")
        expect(campo_nome).to_be_focused()

        page.keyboard.press("Tab")
        expect(campo_email).to_be_focused()

        page.keyboard.press("Tab")
        expect(campo_telefone).to_be_focused()

        page.keyboard.press("Tab")
        expect(campo_modelo).to_be_focused()

        page.keyboard.press("Tab")
        expect(campo_placa).to_be_focused()

        page.keyboard.press("Tab")
        expect(campo_servico).to_be_focused()

        page.keyboard.press("Tab")
        expect(campo_data).to_be_focused()

        page.keyboard.press("Tab")
        expect(campo_obs).to_be_focused()

        page.keyboard.press("Tab")
        expect(botao_submit).to_be_focused()
