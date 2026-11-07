# AutoCar - Sistema de Agendamento de Revisão Automotiva
### Trabalho Prático Individual (AT2) — Qualidade e Teste de Software (QTS)
**FATEC Registro — Curso de Desenvolvimento de Software Multiplataforma**  
**Autor:** Luca Fagundes  
**Ambiente:** Python 3.12+ (Python 3.14) gerenciado com `uv`  

---

## 1. Sobre o Projeto

O **AutoCar** é um sistema para agendamento de revisões e manutenções automotivas em oficinas mecânicas. O projeto possui:
- **API REST com FastAPI e Pydantic v2:** Validações de clientes, veículos, placas no padrão brasileiro e datas futuras.
- **Interface Web Acessível (WCAG 2.1 AA):** HTML5 semântico com suporte completo a navegação por teclado e leitores de tela.
- **Integração Externa com Tratamento Resiliente:** Simulação de envio de avisos via SMS/WhatsApp com dublês (Mocks) para testar sucesso e falhas de rede.
- **Suíte de Testes Automatizados:**
  - Testes de Integração com `TestClient`, padrão AAA, fixtures com `yield`, mocks e dados sintéticos (`Faker pt_BR`).
  - Testes E2E com Playwright usando Page Object Model (POM).
  - Auditoria de Acessibilidade com Axe-core (0 violações) e teste de foco de teclado.
  - Teste de carga com Locust simulando múltiplos acessos concorrentes.

---

## 2. Documentação e Governança

- 📄 [PRD.md](./PRD.md) — Requisitos do produto, rotas e requisitos não funcionais alinhados à **ISO/IEC 25010**.
- 📄 [AGENTS.md](./AGENTS.md) / [.cursorrules](./.cursorrules) — Diretrizes de contexto do projeto.
- 📄 [AI_USAGE.md](./AI_USAGE.md) — Relatório de transparência destacando o **uso mínimo e pontual** de IA no projeto.
- 📄 [ROTEIRO_GRAVACAO.md](./ROTEIRO_GRAVACAO.md) — Roteiro detalhado com linhas e explicação para a gravação do vídeo de até 4 minutos.

---

## 3. Estrutura de Pastas

```text
├── .cursorrules                   # Regras de contexto da IDE
├── AGENTS.md                      # Diretrizes de projeto
├── AI_USAGE.md                    # Relatório de transparência de IA
├── PRD.md                         # Requisitos e ISO/IEC 25010
├── README.md                      # Instruções de execução e resultados
├── ROTEIRO_GRAVACAO.md            # Roteiro passo a passo do vídeo (até 4 min)
├── locustfile.py                  # Script de teste de carga com Locust
├── pyproject.toml                 # Configuração do projeto e pacotes uv
│
├── app/                           # Aplicação da oficina (SUT)
│   ├── main.py                    # Rotas da API e da página web
│   ├── models.py                  # Modelos Pydantic v2 e regras de validação
│   ├── repository.py              # Repositório em memória com trava thread-safe
│   ├── services/
│   │   └── notification.py        # Serviço externo de aviso (alvo de mock)
│   ├── static/                    # CSS acessível com alto contraste e JS
│   └── templates/
│       └── index.html             # Página HTML acessível WCAG 2.1 AA
│
└── tests/                         # Suíte de testes com Pytest
    ├── conftest.py                # Fixtures com yield e servidor de teste
    ├── factories/
    │   └── carro_factory.py       # Factory de dados sintéticos com Faker pt_BR
    ├── integration/
    │   └── test_revisoes_integration.py # Testes de integração (AAA + Mocks)
    └── e2e/
        ├── pages/
        │   └── revisao_page.py    # Page Object Model com seletores semânticos
        ├── test_revisao_e2e.py    # Teste de ponta a ponta com Playwright
        └── test_accessibility.py   # Auditoria Axe-core WCAG e navegação por teclado
```

---

## 4. Como Rodar o Projeto

O projeto utiliza o **uv** para gerenciar o ambiente e as dependências:

### 4.1. Instalar as dependências
```bash
uv sync
```

### 4.2. Instalar o navegador do Playwright
```bash
uv run playwright install chromium
```

### 4.3. Iniciar a aplicação web
```bash
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
- Acesse a interface web: **http://127.0.0.1:8000/**
- Documentação Swagger da API: **http://127.0.0.1:8000/docs**

---

## 5. Como Rodar os Testes (Pytest)

A suíte possui 13 testes automatizados:

```bash
# Executar todos os 13 testes
uv run pytest -v

# Executar apenas testes de integração
uv run pytest -m integration -v

# Executar apenas testes E2E com Playwright
uv run pytest -m e2e -v

# Executar apenas testes de acessibilidade com Axe-core e teclado
uv run pytest -m accessibility -v
```

---

## 6. Testes de Carga com Locust

O arquivo `locustfile.py` simula motoristas acessando a home da oficina, consultando revisões cadastradas e agendando novos serviços.

### 6.1. Como executar o teste de carga (Headless)
```bash
# 1. Em um terminal, inicie a aplicação:
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000

# 2. Em outro terminal, execute o Locust:
uv run locust --headless -u 40 -r 10 --run-time 15s --host http://127.0.0.1:8000 --csv=locust_results
```

### 6.2. Métricas Obtidas no Teste de Carga

Resultados obtidos com **40 usuários concorrentes** e taxa de spawn de 10 usuários/s durante 15 segundos:

| Rota / Operação | Método | Requisições | Falhas (%) | Média (ms) | Mediana (ms) | Percentil 95 (p95) | Taxa (RPS) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `GET /` (Home da Oficina) | GET | 98 | 0.00% | 12 ms | 5 ms | 44 ms | 7.41 req/s |
| `GET /api/revisoes` | GET | 94 | 0.00% | 18 ms | 6 ms | 53 ms | 7.10 req/s |
| `POST /api/revisoes` | POST | 56 | 0.00% | 9 ms | 6 ms | 39 ms | 4.23 req/s |
| `GET /health` | GET | 31 | 0.00% | 14 ms | 5 ms | 100 ms | 2.34 req/s |
| **Total Consolidado** | **ALL** | **279** | **0.00%** | **14 ms** | **6 ms** | **50 ms** | **21.09 req/s** |

> **Análise segundo a ISO/IEC 25010 (Eficiência de Desempenho):**  
> A aplicação atingiu tempo de resposta p95 de apenas **50 ms** (muito abaixo do teto de 500 ms) e **0.00% de taxa de falhas**, suportando com tranquilidade o fluxo concorrente.

---

## 7. Itens para Envio da Atividade

1. **Repositório Público no GitHub:** URL deste repositório com todo o código-fonte, testes e documentação.
2. **Vídeo Demonstrativo de até 4 minutos:** Link do vídeo gravado (YouTube Não Listado, Google Drive ou Loom).
