from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional
from faker import Faker
from app.models import EspecialidadeEnum

fake = Faker("pt_BR")
# Fixa seed opcional ou gera dinâmico mantendo validade
Faker.seed(42)


class AgendamentoFactory:
    """
    Factory de dados sintéticos para agendamentos médicos utilizando Faker no locale pt_BR.
    Segue o padrão Factory para desacoplar a geração de massa de testes dos cenários de teste.
    """

    @classmethod
    def build_valid_payload(
        cls,
        especialidade: Optional[EspecialidadeEnum] = None,
        dias_a_frente: int = 5,
        **kwargs
    ) -> Dict[str, Any]:
        """Gera um payload válido para o endpoint POST /api/agendamentos."""
        data_consulta = datetime.now(timezone.utc) + timedelta(days=dias_a_frente, hours=2)
        # Formato ISO sem microssegundos para simplificar serialização
        data_iso = data_consulta.replace(microsecond=0).isoformat()

        if not especialidade:
            especialidade = fake.random_element(elements=list(EspecialidadeEnum))

        # Gera telefone brasileiro válido formatado
        ddd = fake.random_int(min=11, max=99)
        numero = fake.random_int(min=910000000, max=999999999)
        telefone = f"({ddd}) {str(numero)[:5]}-{str(numero)[5:]}"

        payload = {
            "paciente_nome": f"{fake.first_name()} {fake.last_name()}",
            "paciente_email": fake.email(),
            "paciente_telefone": telefone,
            "especialidade": especialidade.value,
            "data_horario": data_iso,
            "observacoes": fake.sentence(nb_words=8),
        }
        payload.update(kwargs)
        return payload

    @classmethod
    def build_invalid_payload_past_date(cls) -> Dict[str, Any]:
        """Gera payload com data no passado (violação da regra de negócio)."""
        payload = cls.build_valid_payload(dias_a_frente=-2)
        return payload

    @classmethod
    def build_invalid_payload_single_name(cls) -> Dict[str, Any]:
        """Gera payload com nome único sem sobrenome (violação do validador customizado)."""
        payload = cls.build_valid_payload()
        payload["paciente_nome"] = "Carlos"
        return payload

    @classmethod
    def build_invalid_payload_email(cls) -> Dict[str, Any]:
        """Gera payload com email inválido."""
        payload = cls.build_valid_payload()
        payload["paciente_email"] = "email-invalido-sem-arroba"
        return payload

