"""
Aplicação FastAPI - Oficina AutoCar
Autor: Lucas Gomes Fagundes (QTS - FATEC Registro)
Rotas da API de agendamento de revisões e página web.
"""

from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request, status, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.models import (
    AgendamentoRevisaoCreate,
    AgendamentoRevisaoResponse,
    StatusAgendamentoEnum,
    TipoServicoEnum,
)
from app.repository import repo
from app.services.notification import (
    NotificacaoService,
    FalhaEnvioNotificacaoError,
)

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="AutoCar - Sistema de Revisão Automotiva",
    description="Sistema web e API para agendamento de serviços automotivos e revisões de veículos.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Instância do serviço externo de avisos
notificacao_service = NotificacaoService()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Página web da oficina com formulário acessível e listagem de revisões."""
    revisoes = repo.listar_todos()
    servicos = [s.value for s in TipoServicoEnum]
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"revisoes": revisoes, "servicos": servicos},
    )


@app.get("/health")
def health():
    return {"status": "ok", "app": "AutoCar API"}


@app.post(
    "/api/revisoes",
    response_model=AgendamentoRevisaoResponse,
    status_code=status.HTTP_201_CREATED,
)
def agendar_revisao(dados: AgendamentoRevisaoCreate):
    """Registra uma nova revisão e tenta notificar o cliente via serviço externo."""
    aviso_ok = False
    status_inicial = StatusAgendamentoEnum.CONFIRMADO
    mensagem = "Agendamento da revisão confirmado com sucesso."

    try:
        resposta = notificacao_service.enviar_confirmacao(
            cliente_email=dados.cliente_email,
            cliente_nome=dados.cliente_nome,
            veiculo_modelo=dados.veiculo_modelo,
            veiculo_placa=dados.veiculo_placa,
            data_horario=dados.data_horario.isoformat(),
        )
        aviso_ok = bool(resposta.get("enviado", True))
    except (FalhaEnvioNotificacaoError, Exception):
        # Se a API externa de mensagens falhar, a revisão é agendada normalmente (degradação graciosa)
        aviso_ok = False
        status_inicial = StatusAgendamentoEnum.PENDENTE_AVISO
        mensagem = "Revisão agendada com sucesso. O aviso externo ficou pendente."

    novo = AgendamentoRevisaoResponse(
        cliente_nome=dados.cliente_nome,
        cliente_email=dados.cliente_email,
        cliente_telefone=dados.cliente_telefone,
        veiculo_modelo=dados.veiculo_modelo,
        veiculo_placa=dados.veiculo_placa,
        tipo_servico=dados.tipo_servico,
        data_horario=dados.data_horario,
        observacoes=dados.observacoes,
        status=status_inicial,
        aviso_enviado=aviso_ok,
        mensagem_status=mensagem,
    )
    return repo.salvar(novo)


@app.get("/api/revisoes", response_model=List[AgendamentoRevisaoResponse])
def listar_revisoes(servico: Optional[TipoServicoEnum] = Query(None)):
    todos = repo.listar_todos()
    if servico:
        return [item for item in todos if item.tipo_servico == servico]
    return todos


@app.get("/api/revisoes/{revisao_id}", response_model=AgendamentoRevisaoResponse)
def detalhar_revisao(revisao_id: str):
    item = repo.buscar_por_id(revisao_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Revisão com ID '{revisao_id}' não encontrada.",
        )
    return item


@app.patch("/api/revisoes/{revisao_id}/cancelar", response_model=AgendamentoRevisaoResponse)
def cancelar_revisao(revisao_id: str):
    item = repo.cancelar(revisao_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Revisão com ID '{revisao_id}' não encontrada para cancelamento.",
        )
    return item
