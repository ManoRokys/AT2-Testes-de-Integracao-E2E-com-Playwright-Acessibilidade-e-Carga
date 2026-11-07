# Product Requirements Document (PRD)
## Sistema: ClinicaMed - Agendamento Inteligente de Consultas Médicas

**Disciplina:** Qualidade e Teste de Software (QTS) — FATEC Registro  
**Atividade:** AT2 — Testes de Integração, E2E com Playwright, Acessibilidade e Carga  
**Autor:** Luca Fagundes  
**Versão:** 1.0.0  
**Stack Tecnológica:** Python 3.12+, FastAPI, Pydantic v2, Jinja2, Uv, Pytest, Playwright, Axe-core, Locust  

---

## 1. Visão Geral do Produto
O **ClinicaMed** é um sistema web e API REST desenvolvido para automatizar e otimizar o fluxo de agendamento de consultas médicas ambulatoriais. A solução visa proporcionar aos pacientes uma interface web intuitiva e totalmente acessível (WCAG 2.1 AA), enquanto oferece aos atendentes e gestores uma API robusta para integração com sistemas hospitalares e serviços externos de mensageria (SMS/E-mail).

---

## 2. Especificação das Rotas da API REST

A API do ClinicaMed segue as diretrizes RESTful, com payloads em JSON e tipagem estrita validada via Pydantic v2.

### 2.1. `POST /api/agendamentos`
- **Descrição:** Cria uma nova solicitação de consulta médica e despacha a notificação para o serviço externo de mensageria.
- **Status HTTP de Sucesso:** `201 Created`
- **Status HTTP de Erro de Validação:** `422 Unprocessable Entity`
- **Payload de Requisição:**
  ```json
  {
    "paciente_nome": "Carlos Eduardo de Souza",
    "paciente_email": "carlos.souza@exemplo.com.br",
    "paciente_telefone": "(11) 98765-4321",
    "especialidade": "Cardiologia",
    "data_horario": "2026-11-20T14:30:00Z",
    "observacoes": "Primeira consulta para check-up de rotina."
  }
  ```
- **Regras de Negócio e Validações:**
  - `paciente_nome`: obrigatório, mínimo de 3 caracteres, deve conter ao menos nome e sobrenome (validador customizado).
  - `paciente_email`: obrigatório, formato de e-mail sintaticamente válido (`EmailStr`).
  - `paciente_telefone`: obrigatório, formato com DDD (mínimo 10 caracteres).
  - `especialidade`: restrita ao enum: `Clínica Geral`, `Cardiologia`, `Dermatologia`, `Ortopedia`, `Pediatria`.
  - `data_horario`: obrigatório, deve representar uma data e horário estritamente futuros.
- **Payload de Resposta (Sucesso):**
  ```json
  {
    "id": "e4f8b91c-14d2-43bb-a320-1a2b3c4d5e6f",
    "paciente_nome": "Carlos Eduardo de Souza",
    "paciente_email": "carlos.souza@exemplo.com.br",
    "paciente_telefone": "(11) 98765-4321",
    "especialidade": "Cardiologia",
    "data_horario": "2026-11-20T14:30:00Z",
    "observacoes": "Primeira consulta para check-up de rotina.",
    "status": "CONFIRMADO",
    "notificacao_enviada": true,
    "mensagem_status": "Agendamento confirmado com sucesso.",
    "criado_em": "2026-11-07T15:00:00Z"
  }
  ```

### 2.2. `GET /api/agendamentos`
- **Descrição:** Retorna a listagem de todos os agendamentos cadastrados, com opção de filtro por especialidade.
- **Status HTTP:** `200 OK`
- **Query Params:** `especialidade` (opcional).

### 2.3. `GET /api/agendamentos/{id}`
- **Descrição:** Obtém os dados completos de um agendamento individual por UUID.
- **Status HTTP:** `200 OK` ou `404 Not Found`.

### 2.4. `PATCH /api/agendamentos/{id}/cancelar`
- **Descrição:** Atualiza o estado da consulta para `CANCELADO`.
- **Status HTTP:** `200 OK` ou `404 Not Found`.

### 2.5. `GET /health`
- **Descrição:** Endpoint leve de diagnóstico (liveness probe).
- **Status HTTP:** `200 OK` -> `{"status": "healthy", "service": "ClinicaMed API"}`.

---

## 3. Especificação da Interface Web

A interface web é servida na rota raiz `GET /` e foi projetada com foco total em usabilidade, semântica e acessibilidade universal:
1. **Estrutura Semântica:** Uso correto de landmarks HTML5 (`<header role="banner">`, `<main id="main-content" role="main">`, `<section aria-labelledby="...">`, `<footer role="contentinfo">`).
2. **Navegação por Teclado:**
   - Link de salto rápido (*Skip Link*) oculto visualmente que se torna visível ao receber foco (`:focus`), permitindo ao usuário de teclado ir direto ao formulário principal.
   - Ordem de tabulação lógica (`tabindex` natural) sem armadilhas de foco (*keyboard traps*).
   - Estilização clara de `:focus-visible` com anel de foco de alto contraste (3px).
3. **Formulário Acessível:**
   - Rótulos explícitos com `<label for="...">` devidamente associados a cada `<input>`, `<select>` e `<textarea>`.
   - Marcação de campos obrigatórios com `aria-required="true"`.
   - Textos de ajuda conectados aos inputs via `aria-describedby`.
4. **Comunicação com Leitores de Tela:**
   - Região viva dinâmica (`role="status" aria-live="polite"`) que anuncia o resultado das ações de agendamento e cancelamento sem recarregar a tela.
5. **Tabela de Dados Acessível:**
   - Elemento `<table>` contendo `<caption>`, cabeçalhos semânticos `<th scope="col">` e botões de ação com `aria-label` descritivo contextualizando o nome do paciente.

---

## 4. Requisitos Não Funcionais (Conforme ISO/IEC 25010)

| Característica ISO 25010 | Subcaracterística | Requisito Específico e Critério de Aceite |
| :--- | :--- | :--- |
| **Adequação Funcional** | Completude e Correção | Todas as regras de negócio (validação de nome com sobrenome, e-mail sintaticamente válido e datas futuras) devem ser validadas e testadas via suíte de testes automatizados com cobertura nas rotas. |
| **Eficiência de Desempenho** | Comportamento Temporal e Capacidade | Sob carga de 50 usuários concorrentes com Locust, a API deve sustentar um tempo de resposta percentil 95 (p95) inferior a **500 ms** e taxa de falhas igual a **0.00%**. |
| **Usabilidade** | Acessibilidade (WCAG 2.1 AA) | A página web deve ser auditada pelo motor **Axe-core**, atingindo **0 violações** de severidade crítica ou séria nas regras WCAG 2.1 A e AA. A navegação sequencial por teclado deve ser 100% suportada. |
| **Confiabilidade** | Tolerância a Falhas e Maturidade | Se a dependência externa de notificação falhar (ex: queda de rede, timeout), a aplicação deve degradar graciosamente: salvar o agendamento como `PENDENTE_NOTIFICACAO` sem falhar com erro 500 para o usuário final. |
| **Manutenibilidade** | Modularidade e Testabilidade | A arquitetura deve isolar repositório, serviço externo e modelos, implementando padrões de teste estabelecidos: **Page Object Model (POM)** nos testes E2E e **Factory Pattern com Faker pt_BR** para dados sintéticos. |
| **Compatibilidade** | Coexistência e Interoperabilidade | A aplicação deve operar de forma headless em qualquer ambiente compatível com Python 3.12+ gerenciado via `uv`. |

