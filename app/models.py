import uuid
from datetime import datetime, timezone
from enum import Enum 
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


class TipoServicoEnum(str, Enum):
    REVISAO_PREVENTIVA = "Revisão Preventiva"
    TROCA_DE_OLEO = "Troca de Óleo"
    ALINHAMENTO = "Alinhamento e Balanceamento"
    FREIOS = "Freios e Suspensão"
    DIAGNOSTICO = "Diagnóstico Geral"


class StatusAgendamentoEnum(str, Enum):
    CONFIRMADO = "CONFIRMADO"
    PENDENTE_AVISO = "PENDENTE_AVISO"
    CANCELADO = "CANCELADO"


class AgendamentoRevisaoCreate(BaseModel):
    cliente_nome: str = Field(..., min_length=3, max_length=100)
    cliente_email: EmailStr
    cliente_telefone: str = Field(..., min_length=10, max_length=20)
    veiculo_modelo: str = Field(..., min_length=2, max_length=60)
    veiculo_placa: str = Field(..., min_length=7, max_length=8)
    tipo_servico: TipoServicoEnum
    data_horario: datetime
    observacoes: Optional[str] = Field(None, max_length=300)

    @field_validator("cliente_nome")
    @classmethod
    def validar_nome_sobrenome(cls, v: str) -> str:
        partes = v.strip().split()
        if len(partes) < 2:
            raise ValueError("O nome do cliente precisa ter nome e sobrenome.")
        return v.strip()

    @field_validator("veiculo_placa")
    @classmethod
    def validar_formato_placa(cls, v: str) -> str:
        placa = v.strip().upper().replace("-", "")
        if len(placa) != 7 or not placa[:3].isalpha() or not placa[3].isalnum():
            raise ValueError("Placa inválida. Use formato ABC1234 ou Mercosul ABC1D23.")
        return placa

    @field_validator("data_horario")
    @classmethod
    def validar_data_futura(cls, v: datetime) -> datetime:
        agora = datetime.now(timezone.utc)
        alvo = v if v.tzinfo else v.replace(tzinfo=timezone.utc)
        if alvo < agora:
            raise ValueError("A data da revisão deve ser em uma data futura.")
        return v


class AgendamentoRevisaoResponse(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    cliente_nome: str
    cliente_email: str
    cliente_telefone: str
    veiculo_modelo: str
    veiculo_placa: str
    tipo_servico: TipoServicoEnum
    data_horario: datetime
    observacoes: Optional[str] = None
    status: StatusAgendamentoEnum = StatusAgendamentoEnum.CONFIRMADO
    aviso_enviado: bool = True
    mensagem_status: str = "Agendamento da revisão confirmado com sucesso."
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
