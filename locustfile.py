import random
from locust import HttpUser, task, between
from tests.factories.carro_factory import CarroFactory


class UsuarioOficina(HttpUser):
    # Simula tempo de espera de um usuário navegando (1 a 2.5 segundos)
    wait_time = between(1.0, 2.5)

    @task(4)
    def acessar_pagina_oficina(self):
        """Acessa a home da AutoCar."""
        self.client.get("/")

    @task(3)
    def listar_revisoes(self):
        """Consulta as revisões cadastradas."""
        self.client.get("/api/revisoes")

    @task(2)
    def agendar_servico_carro(self):
        """Cadastra uma revisão com dados sintéticos válidos."""
        payload = CarroFactory.payload_valido(dias_a_frente=random.randint(1, 20))
        headers = {"Content-Type": "application/json"}
        self.client.post("/api/revisoes", json=payload, headers=headers)

    @task(1)
    def checar_saude(self):
        """Checagem rápida da rota de health."""
        self.client.get("/health")
