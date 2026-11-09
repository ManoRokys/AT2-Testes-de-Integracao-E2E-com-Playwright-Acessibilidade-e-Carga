"""
Page Object Model (POM) para a tela de agendamento de revisão.
Autor: Lucas Gomes Fagundes (QTS - FATEC Registro)
"""

from playwright.sync_api import Page, Locator


class RevisaoPage:
    """Page Object para a tela de agendamento de revisão da AutoCar."""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

        # Títulos
        self.titulo_principal: Locator = page.get_by_role("heading", name="AutoCar Oficina Mecânica")
        self.titulo_formulario: Locator = page.get_by_role("heading", name="Agendar Serviço")

        # Campos do formulário (seletores semânticos por label)
        self.campo_nome: Locator = page.get_by_label("Nome do Cliente")
        self.campo_email: Locator = page.get_by_label("E-mail")
        self.campo_telefone: Locator = page.get_by_label("Telefone")
        self.campo_modelo: Locator = page.get_by_label("Modelo do Carro")
        self.campo_placa: Locator = page.get_by_label("Placa do Veículo")
        self.campo_servico: Locator = page.get_by_label("Tipo de Serviço")
        self.campo_data: Locator = page.get_by_label("Data e Horário")
        self.campo_obs: Locator = page.get_by_label("Observações do Veículo")

        # Botão
        self.botao_confirmar: Locator = page.get_by_role("button", name="Confirmar Agendamento")

    def abrir(self) -> "RevisaoPage":
        self.page.goto(self.base_url)
        self.page.wait_for_load_state("networkidle")
        return self

    def preencher_e_enviar(
        self,
        nome: str,
        email: str,
        telefone: str,
        modelo: str,
        placa: str,
        servico: str,
        data_iso: str,
        observacoes: str = "",
    ) -> None:
        self.campo_nome.fill(nome)
        self.campo_email.fill(email)
        self.campo_telefone.fill(telefone)
        self.campo_modelo.fill(modelo)
        self.campo_placa.fill(placa)
        self.campo_servico.select_option(label=servico)
        self.campo_data.fill(data_iso[:16])
        if observacoes:
            self.campo_obs.fill(observacoes)
        self.botao_confirmar.click()

    def obter_linha_por_placa(self, placa: str) -> Locator:
        return self.page.locator("tr").filter(has_text=placa)

