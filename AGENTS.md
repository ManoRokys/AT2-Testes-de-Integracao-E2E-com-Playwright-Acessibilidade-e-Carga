# Diretrizes de Governança e Regras de Contexto para Agentes de IA

Este documento define os padrões arquiteturais, diretrizes de codificação e políticas de garantia de qualidade para agentes de IA e desenvolvedores atuando no repositório **ClinicaMed**.

---

## 1. Stack e Gerenciamento de Dependências
- **Linguagem:** Python 3.12+ (compatível com Python 3.14).
- **Gerenciador de Pacotes:** `uv`. Nunca utilize comandos `pip install` soltos; utilize `uv add` e `uv run`.
- **Framework Web:** FastAPI com tipagem estrita e validação via Pydantic v2 (`BaseModel`, `Field`, `field_validator`).
- **Templating:** Jinja2 para a interface gráfica web acessível.

---

## 2. Padrões de Teste e Qualidade (Pirâmide de Testes)

### 2.1. Testes de Integração (`@pytest.mark.integration`)
- Todas as rotas HTTP devem ser cobertas utilizando `fastapi.testclient.TestClient`.
- **Padrão Obrigatório AAA (Arrange, Act, Assert):** Todo método de teste deve conter comentários explícitos demarcando cada etapa.
- **Isolamento de Estado:** Utilizar fixtures do pytest com `yield` para garantir setup e teardown limpos (ex: limpeza do repositório em memória).
- **Mocks para Serviços Externos:** O serviço de mensageria externa (`app.services.notification.ExternalNotificationClient`) DEVE ser isolado utilizando `pytest-mock` (`mocker.patch`). Devem existir testes obrigatórios tanto para o cenário de **sucesso** (retorno 200/201) quanto de **falha** (`side_effect=NotificationDeliveryError`).
- **Massa de Dados Sintéticos:** Nunca hardcodar valores randômicos nos testes. Utilizar o padrão Factory (`tests.factories.appointment_factory.AgendamentoFactory`) integrado com `Faker("pt_BR")`.

### 2.2. Testes End-to-End (`@pytest.mark.e2e`)
- Implementar testes de ponta a ponta com **Playwright** (`pytest-playwright`).
- Seguir estritamente o padrão **Page Object Model (POM)**: as interações com elementos devem ser encapsuladas em classes dentro de `tests/e2e/pages/`.
- **Seletores Semânticos:** É proibido o uso de seletores frágeis como XPath ou classes CSS profundas. Utilizar exclusivamente:
  - `page.get_by_role()`
  - `page.get_by_label()`
  - `page.get_by_text()`

### 2.3. Auditoria de Acessibilidade (`@pytest.mark.accessibility`)
- Utilizar **Axe-core** (`axe-playwright-python`) para auditoria automatizada WCAG 2.1 níveis A e AA.
- A asserção deve garantir `results.violations_count == 0`.
- Validar navegação exclusiva por teclado utilizando `page.keyboard.press("Tab")` em conjunto com asserções de foco `expect(locator).to_be_focused()`.

### 2.4. Testes de Carga com Locust
- O arquivo `locustfile.py` deve herdar de `HttpUser` e conter tarefas ponderadas com `@task(peso)`.
- Medir e registrar no `README.md`:
  - RPS (Requisições por segundo)
  - Tempo de resposta no percentil 95 (p95)
  - Taxa de falhas (%)

---

## 3. Diretrizes de Acessibilidade Web (WCAG 2.1 AA)
- Contraste de cor mínimo de 4.5:1 para texto normal e 3:1 para controles visuais.
- Todo `<input>` deve ter um `<label for="...">` correspondente.
- Todos os botões interativos devem possuir nomes acessíveis visíveis ou via `aria-label`.
- Áreas dinâmicas com feedback ao usuário devem utilizar `role="status"` e `aria-live="polite"`.
- Estilos de foco (:focus-visible) não podem ser removidos com `outline: none`.

