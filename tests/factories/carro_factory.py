"""
Factory para geração de massa de dados sintéticos com Faker pt_BR.
Autor: Lucas Gomes Fagundes (QTS - FATEC Registro)
"""

import random
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional
from faker import Faker
from app.models import TipoServicoEnum

faker = Faker("pt_BR")

MODELOS_CARROS = [
    "Chevrolet Onix 1.0",
    "Hyundai HB20 1.6",
    "Volkswagen Gol 1.6",
    "Fiat Argo 1.3",
    "Toyota Corolla XEi",
    "Honda Civic 2.0",
    "Jeep Renegade Longitude",
    "Nissan Kicks 1.6",
]


class CarroFactory:
    """Factory simples com Faker para gerar dados de testes de agendamento de carros."""

    @classmethod
    def gerar_placa_valida(cls) -> str:
        # Gera formato Mercosul: 3 letras, 1 numero, 1 letra, 2 numeros (ex: BRA2E19)
        letras = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3))
        num1 = random.choice("0123456789")
        letra4 = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        num2 = "".join(random.choices("0123456789", k=2))
        return f"{letras}{num1}{letra4}{num2}"

    @classmethod
    def payload_valido(
        cls,
        tipo_servico: Optional[TipoServicoEnum] = None,
        dias_a_frente: int = 4,
        **kwargs
    ) -> Dict[str, Any]:
        data_agendamento = datetime.now(timezone.utc) + timedelta(days=dias_a_frente, hours=3)
        data_iso = data_agendamento.replace(microsecond=0).isoformat()

        if not tipo_servico:
            tipo_servico = random.choice(list(TipoServicoEnum))

        ddd = random.randint(11, 19)
        num = random.randint(910000000, 999999999)
        telefone = f"({ddd}) {str(num)[:5]}-{str(num)[5:]}"

        dados = {
            "cliente_nome": f"{faker.first_name()} {faker.last_name()}",
            "cliente_email": faker.email(),
            "cliente_telefone": telefone,
            "veiculo_modelo": random.choice(MODELOS_CARROS),
            "veiculo_placa": cls.gerar_placa_valida(),
            "tipo_servico": tipo_servico.value,
            "data_horario": data_iso,
            "observacoes": "Troca de filtros e checagem de freios.",
        }
        dados.update(kwargs)
        return dados

    @classmethod
    def payload_data_passada(cls) -> Dict[str, Any]:
        return cls.payload_valido(dias_a_frente=-3)

    @classmethod
    def payload_nome_invalido(cls) -> Dict[str, Any]:
        d = cls.payload_valido()
        d["cliente_nome"] = "Lucas"  # sem sobrenome
        return d

    @classmethod
    def payload_placa_invalida(cls) -> Dict[str, Any]:
        d = cls.payload_valido()
        d["veiculo_placa"] = "1234567"  # 7 caracteres mas sem formato de letras inicial
        return d

