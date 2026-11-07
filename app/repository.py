import threading
from typing import List, Optional, Dict
from app.models import AgendamentoRevisaoResponse, StatusAgendamentoEnum


class RevisaoRepository:
    """Repositório em memória para armazenar os agendamentos de oficina."""

    def __init__(self):
        self._trava = threading.Lock()
        self._dados: Dict[str, AgendamentoRevisaoResponse] = {}

    def salvar(self, agendamento: AgendamentoRevisaoResponse) -> AgendamentoRevisaoResponse:
        with self._trava:
            self._dados[agendamento.id] = agendamento
            return agendamento

    def listar_todos(self) -> List[AgendamentoRevisaoResponse]:
        with self._trava:
            return sorted(
                list(self._dados.values()),
                key=lambda item: item.criado_em,
                reverse=True,
            )

    def buscar_por_id(self, item_id: str) -> Optional[AgendamentoRevisaoResponse]:
        with self._trava:
            return self._dados.get(item_id)

    def cancelar(self, item_id: str) -> Optional[AgendamentoRevisaoResponse]:
        with self._trava:
            item = self._dados.get(item_id)
            if not item:
                return None
            item.status = StatusAgendamentoEnum.CANCELADO
            item.mensagem_status = "Agendamento de revisão cancelado com sucesso."
            return item

    def limpar(self) -> None:
        """Limpa o repositório entre os testes nas fixtures do pytest."""
        with self._trava:
            self._dados.clear()


repo = RevisaoRepository()
