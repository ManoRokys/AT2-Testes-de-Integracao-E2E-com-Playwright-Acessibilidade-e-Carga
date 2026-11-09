# Diretrizes do Projeto e Contexto de IA (AutoCar)
**Estudante:** Lucas Gomes Fagundes — FATEC Registro (Disciplina QTS)

Este arquivo documenta as diretrizes do projeto e registra que a atividade foi desenvolvida pelo estudante, com uso da IA apenas para auxílio com sintaxes e consultas rápidas de documentação.

---

## 1. Padrões de Código e Tecnologias
- **Linguagem e Ferramentas:** Python 3.12+ com gerenciador `uv`.
- **Framework:** FastAPI com Pydantic v2 para validação dos dados de clientes e veículos.
- **Frontend:** Jinja2 e HTML semântico com foco em acessibilidade WCAG 2.1 AA.

---

## 2. Regras para os Testes
- **Integração:** Padrão AAA obrigatório, fixtures com `yield` no `conftest.py`, dublês com `mocker.patch` testando sucesso e erro do serviço externo, e massa de dados com `Faker("pt_BR")` na Factory.
- **E2E e Acessibilidade:** Playwright usando Page Object Model (POM), seletores semânticos (`get_by_role`, `get_by_label`), Axe-core sem violações e validação de `Tab` com `to_be_focused()`.
- **Carga:** Script `locustfile.py` com tarefas ponderadas (`@task`).

---

## 3. Nota sobre o uso de IA
O design do sistema, as regras de negócio automotivas, os casos de testes e a arquitetura das pastas foram pensados e implementados pelo aluno. 
