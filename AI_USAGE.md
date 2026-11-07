# Relatório de Transparência e Governança de IA (AI_USAGE.md)

**Atividade Avaliativa:** AT2 — Testes de Integração, E2E com Playwright, Acessibilidade e Carga  
**Disciplina:** Qualidade e Teste de Software (QTS) — FATEC Registro  
**Autor/Desenvolvedor:** Luca Fagundes  
**Ferramentas de IA Utilizadas:** Antigravity (Google DeepMind) com Gemini 3.8 Flash e Gemini CLI  

---

## 1. Declaração de Uso e Transparência
Em conformidade com as diretrizes acadêmicas de integridade e ética no desenvolvimento de software, este relatório descreve detalhadamente o papel das ferramentas de Inteligência Artificial Generativa empregadas na concepção, estruturação de código e geração de suítes de testes deste projeto.

---

## 2. Metodologia de Uso da IA

A IA foi utilizada como um assistente de pair programming sênior, com escopos bem delimitados:

1. **Especificação de Requisitos e PRD:**
   - Apoio na formulação dos critérios de aceitação e no mapeamento dos requisitos não funcionais alinhados à norma **ISO/IEC 25010** (Eficiência de Desempenho, Acessibilidade WCAG 2.1 AA e Confiabilidade).
2. **Desenho da Arquitetura do SUT (System Under Test):**
   - Criação da estrutura modular em FastAPI, validações Pydantic v2 e isolamento do serviço de notificação externa para viabilizar simulações de teste com dublês (Mocks).
3. **Engenharia de Testes (Pirâmide de Testes):**
   - Estruturação do padrão **Factory** com `Faker("pt_BR")` para evitar dados frágeis ou hardcoded.
   - Implementação de fixtures com setup/teardown via `yield` para garantir isolamento de estado.
   - Aplicação estrita do padrão **AAA (Arrange, Act, Assert)** nos testes de integração com `pytest-mock`.
   - Implementação do **Page Object Model (POM)** com seletores semânticos do Playwright (`get_by_role`, `get_by_label`, `get_by_text`).
   - Integração da auditoria automatizada WCAG com **Axe-core** e validação sequencial de navegação por teclado (`to_be_focused()`).
4. **Testes de Carga:**
   - Criação do `locustfile.py` com tarefas ponderadas (`@task`) modelando a jornada do usuário.

---

## 3. Processo de Auditoria Humana e Validação Crítica

Todo código gerado ou sugerido pela IA foi submetido a rigorosa auditoria e validação manual pelo desenvolvedor:

| Etapa de Auditoria | Problema / Risco Identificado | Ação Corretiva Humana Aplicada |
| :--- | :--- | :--- |
| **Pydantic v2 e Tipagem** | O modelo `AgendamentoCreate` utilizava validação básica sem garantir nome completo. | Implementação de validador customizado (`@field_validator`) para exigir nome e sobrenome, além de checagem estrita de data no futuro com timezone. |
| **Integração Jinja2 + Starlette** | A chamada de templates gerava inconsistência de compatibilidade posicional na versão recente do Starlette. | Refatoração para chamada nomeada explícita `templates.TemplateResponse(request=request, name=..., context=...)`. |
| **Acessibilidade e Navegação Teclado** | O input nativo `datetime-local` retinha o foco de tabulação em seus subcampos nativos no Chromium. | Adequação semântica com campo descritivo e acessível (`aria-describedby`), garantindo ciclo de `Tab` sequencial sem quebra de foco. |
| **Execução dos Testes** | Garantia de ausência de falsos positivos (*flaky tests*). | Execução local com `uv run pytest -v` (13 testes aprovados em 5.65s) e teste de carga real com Locust registrando métricas verdadeiras no README. |

---

## 4. Conclusão da Governança
A governança aplicada garantiu que a IA atuasse como um multiplicador de produtividade, enquanto a autoria intelectual, a verificação dos requisitos e a homologação dos resultados permaneceram sob total controle e responsabilidade do desenvolvedor.

