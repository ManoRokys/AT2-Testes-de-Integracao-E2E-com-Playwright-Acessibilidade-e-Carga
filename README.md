# ClinicaMed - Sistema de Agendamento Médico
### Trabalho Prático Individual (AT2) — Qualidade e Teste de Software (QTS)
**FATEC Registro — Curso de Desenvolvimento de Software Multiplataforma**  
**Autor:** Luca Fagundes  
**Ambiente:** Python 3.12+ (Python 3.14) gerenciado com `uv`  

---

## 1. Visão Geral do Projeto

O **ClinicaMed** é um sistema completo e resiliente para agendamento de consultas médicas ambulatoriais, composto por:
- **Backend API REST:** Construído em **FastAPI** com validações estritas em **Pydantic v2**.
- **Interface Web Semântica:** Páginas HTML5 com suporte integral às diretrizes de acessibilidade **WCAG 2.1 AA** e estilização CSS moderna com foco visual contrastante.
- **Integração Externa:** Módulo de envio de notificações (SMS/E-mail) com tratamento resiliente (*graceful degradation*) e dublês de teste (Mocks).
- **Pirâmide de Testes Completa:**
  - Testes de Integração com `TestClient`, Fixtures com `yield`, Mocks (`pytest-mock`) e Factory com `Faker("pt_BR")`.
  - Testes End-to-End (E2E) com **Playwright** e **Page Object Model (POM)** via seletores semânticos.
  - Auditoria Automatizada de Acessibilidade com **Axe-core** (0 violações) e testes de foco por teclado (`Tab` e `to_be_focused()`).
  - Testes de Carga e Performance com **Locust** simulando múltiplos usuários concorrentes.

---

## 2. Artefatos de Governança e Especificação

- 📄 [PRD.md](./PRD.md) — Product Requirements Document: especificação das rotas, interface web e requisitos não funcionais alinhados à norma **ISO/IEC 25010**.
- 📄 [AGENTS.md](./AGENTS.md) / [.cursorrules](./.cursorrules) — Diretrizes de contexto, padrões arquiteturais e regras para agentes de IA e desenvolvedores.
- 📄 [AI_USAGE.md](./AI_USAGE.md) — Relatório de transparência: declaração das ferramentas utilizadas, metodologia de prompting e auditoria humana detalhada.
- 📄 [ROTEIRO_GRAVACAO.md](./ROTEIRO_GRAVACAO.md) — Roteiro detalhado com minutagem e linhas de código para o vídeo demonstrativo de até 4 minutos.

---

## 3. Estrutura do Repositório

```text
├── .cursorrules                   # Regras de contexto para IDEs com IA
├── AGENTS.md                      # Governança e padrões para agentes de IA
├── AI_USAGE.md                    # Relatório de transparência e auditoria de IA
├── PRD.md                         # Especificação de requisitos e ISO/IEC 25010
├── README.md                      # Documentação geral e guia de execução
├── ROTEIRO_GRAVACAO.md            # Roteiro passo a passo para o vídeo de até 4 min
├── locustfile.py                  # Script de teste de carga com Locust (HttpUser)
├── pyproject.toml                 # Gerenciamento de projeto e dependências com uv
├── uv.lock                        # Lockfile determinístico do uv
│
├── app/                           # Código-fonte da aplicação (SUT)
│   ├── __init__.py
│   ├── main.py                    # Instância FastAPI, rotas da API e da interface web
│   ├── models.py                  # Esquemas Pydantic v2 (validações e Enums)
│   ├── repository.py              # Repositório em memória thread-safe com isolamento
│   ├── services/
│   │   └── notification.py        # Dependência externa de mensageria (alvo de mock)
│   ├── static/                    # Arquivos estáticos acessíveis (CSS e JS)
│   │   ├── css/style.css          # Estilos com alto contraste e :focus-visible
│   │   └── js/app.js              # Interações dinâmicas e aria-live updates
│   └── templates/
│       └── index.html             # Interface web semântica WCAG 2.1 AA
│
└── tests/                         # Suíte de testes automatizados
    ├── conftest.py                # Fixtures pytest (yield setup/teardown e live server)
    ├── factories/
    │   └── appointment_factory.py # Factory de dados sintéticos com Faker pt_BR
    ├── integration/
    │   └── test_appointments_integration.py # Testes de integração (AAA + mocks)
    └── e2e/
        ├── pages/
        │   └── appointment_page.py # Page Object Model com seletores semânticos
        ├── test_appointment_e2e.py # Testes E2E com Playwright
        └── test_accessibility.py   # Auditoria WCAG com Axe-core e teclado
```

---

## 4. Pré-requisitos e Instalação

O projeto é gerenciado com o **uv**, o gerenciador de pacotes ultrarrápido para Python.

### 4.1. Instalação das dependências
```bash
# Sincroniza o ambiente virtual e instala todas as dependências
uv sync
```

### 4.2. Instalação dos navegadores do Playwright
```bash
# Instala o navegador Chromium para os testes E2E e de acessibilidade
uv run playwright install chromium
```

---

## 5. Execução da Aplicação Web

Para iniciar o servidor FastAPI localmente:
```bash
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
- Acesso à interface web: **http://127.0.0.1:8000/**
- Documentação interativa Swagger: **http://127.0.0.1:8000/docs**
- Documentação ReDoc: **http://127.0.0.1:8000/redoc**

---

## 6. Execução da Suíte de Testes Automatizados (Pytest)

A suíte possui 13 testes distribuídos pelas camadas da pirâmide de testes e requisitos não funcionais.

### 6.1. Executar todos os testes
```bash
uv run pytest -v
```

### 6.2. Executar por marcadores específicos
```bash
# Apenas testes de integração (TestClient, AAA, Fixtures, Mocks e Faker)
uv run pytest -m integration -v

# Apenas testes End-to-End com Playwright (Page Object Model)
uv run pytest -m e2e -v

# Apenas testes de acessibilidade (Axe-core WCAG 2.1 AA e foco de teclado)
uv run pytest -m accessibility -v
```

---

## 7. Testes de Carga e Performance com Locust

O arquivo `locustfile.py` simula usuários concorrentes realizando tarefas ponderadas (acesso à home, listagem de agendamentos, submissão de novas consultas com dados sintéticos e sondagem de saúde).

### 7.1. Execução via Interface Web do Locust
```bash
# Em um terminal, inicie a aplicação:
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000

# Em outro terminal, inicie o Locust:
uv run locust
```
Acesse a interface em **http://localhost:8089**, informe o host `http://127.0.0.1:8000`, configure 50 usuários e taxa de spawn de 10 usuários/s.

### 7.2. Execução Headless (via Linha de Comando)
```bash
uv run locust --headless -u 50 -r 10 --run-time 20s --host http://127.0.0.1:8000 --csv=locust_results
```

### 7.3. Métricas Obtidas no Teste de Carga

Resultados consolidados com **50 usuários concorrentes**, taxa de spawn de 10 usuários/segundo por 20 segundos:

| Rota / Operação | Método | Requisições | Falhas (%) | Média (ms) | Mínimo (ms) | Mediana (ms) | Percentil 95 (p95) | Taxa (RPS) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `GET /` (Página Principal) | GET | 168 | 0.00% | 11 ms | 2 ms | 6 ms | 32 ms | 9.90 req/s |
| `GET /api/agendamentos` | GET | 142 | 0.00% | 9 ms | 2 ms | 6 ms | 34 ms | 8.37 req/s |
| `POST /api/agendamentos` | POST | 104 | 0.00% | 9 ms | 3 ms | 6 ms | 28 ms | 6.13 req/s |
| `GET /health` | GET | 41 | 0.00% | 8 ms | 2 ms | 4 ms | 29 ms | 2.42 req/s |
| **Total / Consolidado** | **ALL** | **455** | **0.00%** | **9 ms** | **2 ms** | **6 ms** | **32 ms** | **26.81 req/s** |

> **Análise conforme ISO/IEC 25010 (Eficiência de Desempenho):**
> O sistema atendeu com ampla margem a meta de tempo de resposta percentil 95 abaixo de 500 ms (**p95 obtido: 32 ms**) e obteve **taxa de falhas de 0.00%**, comprovando alta estabilidade e capacidade de vazão.

---

## 8. Itens de Submissão Acadêmica

1. **Repositório Público no GitHub:** `https://github.com/lucafagundes/AT2-Testes-de-Integracao-E2E-com-Playwright-Acessibilidade-e-Carga`
2. **Vídeo Demonstrativo (Até 4 minutos):** [Inserir link do YouTube/Loom/Drive com acesso liberado]
