import pytest
from playwright.sync_api import Page, expect
from axe_playwright_python.sync_playwright import Axe


@pytest.mark.accessibility
class TestAcessibilidadeWCAG:
    """
    Suíte de auditoria de acessibilidade automatizada em conformidade com a WCAG 2.1 AA
    e testes de usabilidade e navegabilidade exclusivamente por teclado.
    Atende aos requisitos de Usabilidade da ISO/IEC 25010.
    """

    def test_auditoria_automatizada_axe_wcag_21_aa(self, page: Page, live_server_url: str):
        """
        Executa a varredura com o motor Axe-core na interface web da clínica.
        Garante conformidade com WCAG 2.1 níveis A e AA (contraste de cores,
        labels em formulários, hierarquia semântica, atributos ARIA e landmarks).
        """
        # ==================== ARRANGE ====================
        page.goto(live_server_url)
        page.wait_for_load_state("networkidle")

        # ==================== ACT ====================
        axe = Axe()
        # Opcionalmente restringe aos padrões wcag2a e wcag2aa
        results = axe.run(
            page,
            options={
                "runOnly": {
                    "type": "tag",
                    "values": ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]
                }
            }
        )

        # ==================== ASSERT ====================
        # A asserção deve garantir 0 violações de acessibilidade
        assert results.violations_count == 0, (
            f"Foram encontradas {results.violations_count} violações de acessibilidade WCAG:\n"
            f"{results.generate_report()}"
        )

    def test_navegacao_exclusiva_por_teclado_tab_order(self, page: Page, live_server_url: str):
        """
        Valida que todos os controles interativos podem ser acessados via teclado (tecla Tab),
        seguindo a ordem de foco lógica e acionando o foco visível (:focus-visible).
        Utiliza asserções to_be_focused() conforme exigido pela especificação.
        """
        # ==================== ARRANGE ====================
        page.goto(live_server_url)
        page.wait_for_load_state("networkidle")

        # Localizadores esperados na ordem sequencial de tabulação
        skip_link = page.locator(".skip-link")
        input_nome = page.get_by_label("Nome Completo")
        input_email = page.get_by_label("E-mail")
        input_telefone = page.get_by_label("Telefone")
        select_especialidade = page.get_by_label("Especialidade Médica")
        input_data = page.get_by_label("Data e Horário")
        input_obs = page.get_by_label("Observações")
        btn_submit = page.get_by_role("button", name="Confirmar Agendamento")

        # ==================== ACT & ASSERT ====================
        # 1. Primeiro Tab: atinge o skip link
        page.keyboard.press("Tab")
        expect(skip_link).to_be_focused()

        # 2. Segundo Tab: atinge o primeiro campo do formulário (Nome Completo)
        page.keyboard.press("Tab")
        expect(input_nome).to_be_focused()

        # 3. Terceiro Tab: E-mail
        page.keyboard.press("Tab")
        expect(input_email).to_be_focused()

        # 4. Quarto Tab: Telefone
        page.keyboard.press("Tab")
        expect(input_telefone).to_be_focused()

        # 5. Quinto Tab: Especialidade Médica
        page.keyboard.press("Tab")
        expect(select_especialidade).to_be_focused()

        # 6. Sexto Tab: Data e Horário
        page.keyboard.press("Tab")
        expect(input_data).to_be_focused()

        # 7. Sétimo Tab: Observações
        page.keyboard.press("Tab")
        expect(input_obs).to_be_focused()

        # 8. Oitavo Tab: Botão de submissão
        page.keyboard.press("Tab")
        expect(btn_submit).to_be_focused()

