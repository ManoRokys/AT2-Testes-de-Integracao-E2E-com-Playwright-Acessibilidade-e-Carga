import random
from locust import HttpUser, task, between
from tests.factories.appointment_factory import AgendamentoFactory


class ClinicaMedUser(HttpUser):
    """
    Simulação de usuário concorrente no sistema ClinicaMed.
    Modela o comportamento de pacientes e atendentes acessando a interface web,
    consultando a lista de agendamentos e submetendo novas marcações de consulta.
    """

    # Intervalo de espera ponderado entre tarefas (1 a 2.5 segundos)
    wait_time = between(1.0, 2.5)

    @task(4)
    def acessar_pagina_principal(self):
        """Simula a navegação de um usuário na página inicial da clínica (HTML/CSS)."""
        with self.client.get("/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Falha ao carregar home: {response.status_code}")

    @task(3)
    def listar_consultas_agendadas(self):
        """Simula a consulta frequente à API de agendamentos."""
        with self.client.get("/api/agendamentos", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Falha ao listar agendamentos: {response.status_code}")

    @task(2)
    def criar_novo_agendamento(self):
        """Simula a submissão de um novo agendamento com dados sintéticos válidos."""
        payload = AgendamentoFactory.build_valid_payload(
            dias_a_frente=random.randint(1, 30)
        )
        headers = {"Content-Type": "application/json"}
        with self.client.post("/api/agendamentos", json=payload, headers=headers, catch_response=True) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure(f"Erro na criação de agendamento: {response.status_code} - {response.text}")

    @task(1)
    def monitorar_saude_da_api(self):
        """Simula probes periódicos de health check."""
        self.client.get("/health")

