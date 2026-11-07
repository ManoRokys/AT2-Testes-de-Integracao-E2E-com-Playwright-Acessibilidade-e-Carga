import logging
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request, status, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.models import (
    AgendamentoCreate,
    AgendamentoResponse,
    StatusAgendamentoEnum,
    EspecialidadeEnum,
)
from app.repository import repository
from app.services.notification import (
    ExternalNotificationClient,
    NotificationDeliveryError,
)

logger = logging.getLogger("clinica_med")
logging.basicConfig(level=logging.INFO)

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="ClinicaMed - Sistema de Agendamento Médico",
    description="API e Interface Web para agendamento de consultas médicas com suporte a testes de integração, E2E, acessibilidade WCAG e testes de carga.",
    version="1.0.0",
)

# Montagem de arquivos estáticos e templates Jinja2
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Instância padrão do serviço de notificação externa (pode ser sobrescrita em testes)
notification_client = ExternalNotificationClient()


@app.get("/", response_class=HTMLResponse, summary="Interface Web Principal")
def render_index(request: Request):
    """
    Renderiza a interface gráfica web da Clínica Médica, com semântica acessível,
    formulário para novo agendamento e listagem atual de consultas.
    """
    agendamentos = repository.list_all()
    especialidades = [esp.value for esp in EspecialidadeEnum]
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "agendamentos": agendamentos,
            "especialidades": especialidades,
        },
    )


@app.get("/health", tags=["Monitoramento"])
def health_check():
    """Endpoint leve para verificação de saúde e testes de carga rápidos."""
    return {"status": "healthy", "service": "ClinicaMed API"}


@app.post(
    "/api/agendamentos",
    response_model=AgendamentoResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Agendamentos"],
    summary="Cria um novo agendamento de consulta",
)
def criar_agendamento(payload: AgendamentoCreate):
    """
    Cria um novo agendamento e dispara confirmação via serviço externo de notificação.
    Aplica tratamento resiliente caso o serviço de mensageria externo falhe.
    """
    notificacao_sucesso = False
    status_inicial = StatusAgendamentoEnum.CONFIRMADO
    mensagem_status = "Agendamento confirmado com sucesso."

    try:
        # Chamada ao serviço externo (ponto de injeção/mock para testes)
        result = notification_client.send_confirmation(
            paciente_email=payload.paciente_email,
            paciente_nome=payload.paciente_nome,
            especialidade=payload.especialidade.value,
            data_horario=payload.data_horario.isoformat(),
        )
        notificacao_sucesso = bool(result.get("success", True))
    except (NotificationDeliveryError, Exception) as exc:
        logger.warning(
            f"Falha na comunicação com o serviço externo de notificação: {exc}"
        )
        notificacao_sucesso = False
        status_inicial = StatusAgendamentoEnum.PENDENTE_NOTIFICACAO
        mensagem_status = (
            "Agendamento registrado com sucesso. Notificação externa pendente de envio."
        )

    novo_agendamento = AgendamentoResponse(
        paciente_nome=payload.paciente_nome,
        paciente_email=payload.paciente_email,
        paciente_telefone=payload.paciente_telefone,
        especialidade=payload.especialidade,
        data_horario=payload.data_horario,
        observacoes=payload.observacoes,
        status=status_inicial,
        notificacao_enviada=notificacao_sucesso,
        mensagem_status=mensagem_status,
    )

    saved = repository.create(novo_agendamento)
    return saved


@app.get(
    "/api/agendamentos",
    response_model=List[AgendamentoResponse],
    tags=["Agendamentos"],
    summary="Lista todos os agendamentos cadastrados",
)
def listar_agendamentos(
    especialidade: Optional[EspecialidadeEnum] = Query(
        None, description="Filtrar por especialidade médica"
    )
):
    """Retorna os agendamentos registrados no repositório."""
    todos = repository.list_all()
    if especialidade:
        return [item for item in todos if item.especialidade == especialidade]
    return todos


@app.get(
    "/api/agendamentos/{agendamento_id}",
    response_model=AgendamentoResponse,
    tags=["Agendamentos"],
    summary="Busca agendamento por ID",
)
def obter_agendamento(agendamento_id: str):
    """Recupera detalhes de um agendamento específico."""
    item = repository.get_by_id(agendamento_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agendamento com ID '{agendamento_id}' não encontrado.",
        )
    return item


@app.patch(
    "/api/agendamentos/{agendamento_id}/cancelar",
    response_model=AgendamentoResponse,
    tags=["Agendamentos"],
    summary="Cancela um agendamento existente",
)
def cancelar_agendamento(agendamento_id: str):
    """Altera o status de um agendamento para CANCELADO."""
    item = repository.update_status(agendamento_id, StatusAgendamentoEnum.CANCELADO)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agendamento com ID '{agendamento_id}' não encontrado para cancelamento.",
        )
    item.mensagem_status = "Agendamento cancelado com sucesso."
    return item

