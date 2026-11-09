"""
Fixtures compartilhadas para testes com Pytest e Playwright.
Autor: Lucas Gomes Fagundes (QTS - FATEC Registro)
"""

import socket
import threading
import time
import pytest
import uvicorn
from fastapi.testclient import TestClient

from app.main import app
from app.repository import repo


def encontrar_porta_livre() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(autouse=True)
def limpar_dados_repo():
    # Setup: limpa os dados antes de iniciar o teste
    repo.limpar()
    yield
    # Teardown: limpa os dados após terminar o teste
    repo.limpar()


@pytest.fixture
def client():
    # Setup do TestClient do FastAPI
    test_client = TestClient(app)
    yield test_client
    # Teardown do cliente
    test_client.close()


class ServidorTesteUvicorn(uvicorn.Server):
    def install_signal_handlers(self):
        pass


@pytest.fixture(scope="session")
def live_server_url():
    # Inicia uvicorn em background para os testes do Playwright
    porta = encontrar_porta_livre()
    host = "127.0.0.1"
    url = f"http://{host}:{porta}"

    config = uvicorn.Config(
        app=app,
        host=host,
        port=porta,
        log_level="warning",
        loop="asyncio",
    )
    servidor = ServidorTesteUvicorn(config=config)

    thread = threading.Thread(target=servidor.run, daemon=True)
    thread.start()

    inicio = time.time()
    pronto = False
    while time.time() - inicio < 10:
        try:
            with socket.create_connection((host, porta), timeout=0.5):
                pronto = True
                break
        except OSError:
            time.sleep(0.1)

    if not pronto:
        raise RuntimeError("Não foi possível subir o servidor de testes.")

    yield url

    servidor.should_exit = True
    thread.join(timeout=3)
