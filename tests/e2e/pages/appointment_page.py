from playwright.sync_api import Page, Locator, expect


class AppointmentPage:
    """
    Page Object Model (POM) para a interface de agendamento da ClinicaMed.
    Encapsula as interações com o DOM utilizando estritamente seletores semânticos
    e de acessibilidade (get_by_role, get_by_label, get_by_text).
    """

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

        # Elementos semânticos mapeados por Label, Role ou Text
        self.heading: Locator = page.get_by_role("heading", name="ClinicaMed")
        self.form_heading: Locator = page.get_by_role("heading", name="Agendar Consulta")
        self.tabela_heading: Locator = page.get_by_role("heading", name="Consultas Cadastradas")

        # Campos do formulário obtidos por get_by_label
        self.input_nome: Locator = page.get_by_label("Nome Completo")
        self.input_email: Locator = page.get_by_label("E-mail")
        self.input_telefone: Locator = page.get_by_label("Telefone")
        self.select_especialidade: Locator = page.get_by_label("Especialidade Médica")
        self.input_data_horario: Locator = page.get_by_label("Data e Horário")
        self.input_observacoes: Locator = page.get_by_label("Observações")

        # Botão de submissão por get_by_role
        self.btn_submit: Locator = page.get_by_role("button", name="Confirmar Agendamento")

        # Região viva de status / alerta
        self.alert_status: Locator = page.get_by_role("status")

    def navigate(self) -> "AppointmentPage":
        """Navega até a página inicial da aplicação."""
        self.page.goto(self.base_url)
        self.page.wait_for_load_state("networkidle")
        return self

    def fill_form(
        self,
        nome: str,
        email: str,
        telefone: str,
        especialidade: str,
        data_horario_iso: str,
        observacoes: str = ""
    ) -> "AppointmentPage":
        """Preenche todos os campos do formulário de agendamento usando seletores semânticos."""
        self.input_nome.fill(nome)
        self.input_email.fill(email)
        self.input_telefone.fill(telefone)
        self.select_especialidade.select_option(label=especialidade)

        # Formata datetime ISO para 'YYYY-MM-DDTHH:mm' aceito pelo input datetime-local
        formatted_dt = data_horario_iso[:16]
        self.input_data_horario.fill(formatted_dt)

        if observacoes:
            self.input_observacoes.fill(observacoes)
        return self

    def submit_form(self) -> None:
        """Clica no botão de submissão do formulário."""
        self.btn_submit.click()

    def get_status_message(self) -> Locator:
        """Retorna o localizador do alerta de status."""
        return self.alert_status

    def get_row_by_patient_name(self, patient_name: str) -> Locator:
        """Localiza a linha na tabela contendo o nome do paciente via texto semântico."""
        return self.page.locator("tr").filter(has_text=patient_name)

