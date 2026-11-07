import socket
import threading
import time
import pytest
import uvicorn
from fastapi.testclient import TestClient

from app.main import app
from app.repository import repository


def find_free_port() -> int:
    """Encontra uma porta TCP livre dinamicamente para o servidor de teste E2E."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(autouse=True)
def clean_repository():
    """
    Fixture de isolamento com setup e teardown via yield.
    Garante que o estado do repositório seja limpo antes e após cada teste executado.
    """
    # Setup: limpa qualquer resíduo antes de iniciar o teste
    repository.clear()
    yield
    # Teardown: limpa os dados gerados pelo teste após a execução
    repository.clear()


@pytest.fixture
def client():
    """
    Fixture com setup e teardown via yield para TestClient do FastAPI.
    Utilizada nos testes de integração.
    """
    # Setup: instanciação do TestClient com o app FastAPI
    test_client = TestClient(app)
    yield test_client
    # Teardown: fechamento explícito do cliente
    test_client.close()


class UvicornTestServer(uvicorn.Server):
    """Subclasse do Uvicorn Server com controle de inicialização para testes."""

    def install_signal_handlers(self):
        # Desabilita manipuladores de sinal padrão em threads secundárias
        pass


@pytest.fixture(scope="session")
def live_server_url():
    """
    Fixture de escopo de sessão com setup e teardown via yield.
    Inicia uma instância real do servidor FastAPI via Uvicorn em uma thread de background
    para que o Playwright execute testes End-to-End e auditoria de acessibilidade.
    """
    port = find_free_port()
    host = "127.0.0.1"
    base_url = f"http://{host}:{port}"

    config = uvicorn.Config(
        app=app,
        host=host,
        port=port,
        log_level="warning",
        loop="asyncio"
    )
    server = UvicornTestServer(config=config)

    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    # Aguarda o servidor estar pronto para receber requisições
    start_time = time.time()
    server_ready = False
    while time.time() - start_time < 10:
        try:
            with socket.create_connection((host, port), timeout=0.5):
                server_ready = True
                break
        except OSError:
            time.sleep(0.1)

    if not server_ready:
        raise RuntimeError("Não foi possível iniciar o Uvicorn para os testes E2E do Playwright.")

    # Entrega da URL do servidor para os testes E2E
    yield base_url

    # Teardown: finalização do servidor uvicorn
    server.should_exit = True
    thread.join(timeout=3)

