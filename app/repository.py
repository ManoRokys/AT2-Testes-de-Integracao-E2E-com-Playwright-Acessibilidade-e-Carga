import threading
from typing import List, Optional, Dict
from app.models import AgendamentoResponse, StatusAgendamentoEnum


class AgendamentoRepository:
    """
    Repositório thread-safe em memória para persistência de agendamentos.
    Permite isolamento confiável entre cenários de teste através do método clear().
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._items: Dict[str, AgendamentoResponse] = {}

    def create(self, item: AgendamentoResponse) -> AgendamentoResponse:
        with self._lock:
            self._items[item.id] = item
            return item

    def list_all(self) -> List[AgendamentoResponse]:
        with self._lock:
            # Retorna ordenado do mais recente para o mais antigo
            return sorted(
                list(self._items.values()),
                key=lambda x: x.criado_em,
                reverse=True
            )

    def get_by_id(self, item_id: str) -> Optional[AgendamentoResponse]:
        with self._lock:
            return self._items.get(item_id)

    def update_status(self, item_id: str, status: StatusAgendamentoEnum) -> Optional[AgendamentoResponse]:
        with self._lock:
            item = self._items.get(item_id)
            if not item:
                return None
            item.status = status
            return item

    def delete(self, item_id: str) -> bool:
        with self._lock:
            if item_id in self._items:
                del self._items[item_id]
                return True
            return False

    def clear(self) -> None:
        """Limpa o repositório. Utilizado em teardown de fixtures de teste."""
        with self._lock:
            self._items.clear()


# Instância global singleton do repositório
repository = AgendamentoRepository()

