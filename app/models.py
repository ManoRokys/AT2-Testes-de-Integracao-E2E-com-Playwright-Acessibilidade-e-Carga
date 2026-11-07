from enum import Enum
from typing import Optional
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field, EmailStr, field_validator


class EspecialidadeEnum(str, Enum):
    CLINICA_GERAL = "Clínica Geral"
    CARDIOLOGIA = "Cardiologia"
    DERMATOLOGIA = "Dermatologia"
    ORTOPEDIA = "Ortopedia"
    PEDIATRIA = "Pediatria"


class StatusAgendamentoEnum(str, Enum):
    CONFIRMADO = "CONFIRMADO"
    PENDENTE_NOTIFICACAO = "PENDENTE_NOTIFICACAO"
    CANCELADO = "CANCELADO"


class AgendamentoCreate(BaseModel):
    paciente_nome: str = Field(
        ...,
        min_length=3,
        max_length=120,
        description="Nome completo do paciente",
        examples=["João da Silva"]
    )
    paciente_email: EmailStr = Field(
        ...,
        description="E-mail válido para envio da confirmação",
        examples=["joao.silva@exemplo.com.br"]
    )
    paciente_telefone: str = Field(
        ...,
        min_length=10,
        max_length=20,
        description="Telefone de contato do paciente com DDD",
        examples=["(11) 98765-4321"]
    )
    especialidade: EspecialidadeEnum = Field(
        ...,
        description="Especialidade médica desejada"
    )
    data_horario: datetime = Field(
        ...,
        description="Data e horário da consulta agendada"
    )
    observacoes: Optional[str] = Field(
        None,
        max_length=500,
        description="Observações ou histórico relevante para a consulta"
    )

    @field_validator("paciente_nome")
    @classmethod
    def validar_nome_espacos(cls, value: str) -> str:
        clean = value.strip()
        if len(clean.split()) < 2:
            raise ValueError("O nome do paciente deve conter pelo menos nome e sobrenome.")
        return clean

    @field_validator("data_horario")
    @classmethod
    def validar_data_futura(cls, value: datetime) -> datetime:
        # Se for naive datetime, atribuir fuso UTC local
        now = datetime.now(timezone.utc)
        target = value if value.tzinfo else value.replace(tzinfo=timezone.utc)
        if target < now:
            raise ValueError("A data e horário do agendamento devem ser futuros.")
        return value


class AgendamentoResponse(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    paciente_nome: str
    paciente_email: str
    paciente_telefone: str
    especialidade: EspecialidadeEnum
    data_horario: datetime
    observacoes: Optional[str] = None
    status: StatusAgendamentoEnum = StatusAgendamentoEnum.CONFIRMADO
    notificacao_enviada: bool = True
    mensagem_status: str = "Agendamento confirmado com sucesso."
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

