# Roteiro Detalhado para Gravação do Vídeo Demonstrativo (Até 4 Minutos)
## Atividade Avaliativa AT2 — Qualidade e Teste de Software (QTS) — FATEC Registro
**Estudante:** Luca Fagundes  
**Aplicação:** ClinicaMed (FastAPI + Pydantic + Playwright + Axe-core + Locust)  

---

## 🎯 Orientações Gerais para a Gravação
- **Duração Máxima:** 4 minutos (240 segundos).
- **Formato:** Gravação de tela com áudio (voz clara). Câmera aberta é opcional.
- **Ferramentas recomendadas:** OBS Studio, Loom, Clipchamp ou gravador de tela nativo do Windows (`Win + Alt + R`).
- **Dica de tela:** Deixe o VS Code / IDE aberto em uma metade da tela ou tela cheia com fonte legível (Ctrl + "+"). Deixe um terminal aberto pronto para os comandos.

---

## ⏱️ Cronograma e Minutagem do Vídeo

```text
[00:00 - 00:50] Bloco 1: Apresentação Inicial, Domínio, PRD e Governança de IA
[00:50 - 01:55] Bloco 2: Integração, Fixtures com Yield, Mocks e Factory com Faker
[01:55 - 02:55] Bloco 3: E2E com Playwright (POM) e Acessibilidade WCAG com Axe-core
[02:55 - 03:55] Bloco 4: Execução Prática no Terminal (Pytest e Locust)
[03:55 - 04:00] Bloco 5: Conclusão e Encerramento
```

---

## 🎬 Detalhamento Passo a Passo (O Que Mostrar e O Que Falar)

---

### 🔹 BLOCO 1: Apresentação Inicial, Domínio e Governança de IA (00:00 a 00:50)

#### 🖥️ O que mostrar na tela:
1. Abra o arquivo [PRD.md](file:///c:/Users/Roky/AT2-Testes-de-Integracao-E2E-com-Playwright-Acessibilidade-e-Carga/PRD.md) e mostre a seção de rotas e a tabela da **ISO/IEC 25010** (linhas 85 a 100).
2. Abra brevemente o [AGENTS.md](file:///c:/Users/Roky/AT2-Testes-de-Integracao-E2E-com-Playwright-Acessibilidade-e-Carga/AGENTS.md) (linhas 1 a 25) e o [AI_USAGE.md](file:///c:/Users/Roky/AT2-Testes-de-Integracao-E2E-com-Playwright-Acessibilidade-e-Carga/AI_USAGE.md) (linhas 25 a 45).
3. Abra o [app/models.py](file:///c:/Users/Roky/AT2-Testes-de-Integracao-E2E-com-Playwright-Acessibilidade-e-Carga/app/models.py) destacando os esquemas Pydantic v2 (linhas 20 a 55).

#### 🗣️ O que falar (Roteiro falado):
> *"Olá professor(a)! Meu nome é Luca Fagundes e esta é a apresentação da atividade AT2 da disciplina Qualidade e Teste de Software na Fatec Registro.*  
> *Para o trabalho prático, desenvolvi o **ClinicaMed**, um sistema em Python 3.12+ com FastAPI e Pydantic para agendamento de consultas médicas e integração com serviços externos de mensageria.*  
> *Iniciando pela governança, temos o **PRD.md**, onde especificamos todas as rotas da API, a interface web acessível e os requisitos não funcionais mapeados diretamente na norma **ISO/IEC 25010**, cobrindo usabilidade WCAG 2.1 AA, eficiência de desempenho e confiabilidade.*  
> *Também estruturamos o arquivo de regras de contexto **AGENTS.md** e o relatório de transparência **AI_USAGE.md**, detalhando a metodologia de IA assistida e as auditorias humanas rigorosas que realizamos no código."*

---

### 🔹 BLOCO 2: Testes de Integração, Fixtures, Mocks e Faker (00:50 a 01:55)

#### 🖥️ O que mostrar na tela:
1. Abra o arquivo [tests/factories/appointment_factory.py](file:///c:/Users/Roky/AT2-Testes-de-Integracao-E2E-com-Playwright-Acessibilidade-e-Carga/tests/factories/appointment_factory.py) e aponte para:
   - Linhas **7 a 35**: A instância `Faker("pt_BR")` e o método `build_valid_payload` gerando nomes brasileiros, telefones com DDD e datas futuras.
2. Abra o arquivo [tests/conftest.py](file:///c:/Users/Roky/AT2-Testes-de-Integracao-E2E-com-Playwright-Acessibilidade-e-Carga/tests/conftest.py) e aponte para:
   - Linhas **17 a 36**: As fixtures `clean_repository` e `client` utilizando `yield` para setup e teardown limpos.
3. Abra o arquivo [tests/integration/test_appointments_integration.py](file:///c:/Users/Roky/AT2-Testes-de-Integracao-E2E-com-Playwright-Acessibilidade-e-Carga/tests/integration/test_appointments_integration.py) e aponte para:
   - Linhas **10 a 45**: O marcador `@pytest.mark.integration`, a estrutura comentada **Arrange, Act, Assert (AAA)** e o mock de sucesso via `mocker.patch("app.main.notification_client.send_confirmation")`.
   - Linhas **50 a 80**: O teste de resiliência e degradação graciosa com `side_effect=NotificationDeliveryError`, comprovando que o agendamento permanece salvo com status `PENDENTE_NOTIFICACAO`.

#### 🗣️ O que falar (Roteiro falado):
> *"Passando para a camada de integração, implementamos o padrão **Factory** no arquivo `appointment_factory.py`, utilizando o `Faker` com o locale `pt_BR` para gerar dados sintéticos dinâmicos e realistas, evitando valores hardcoded.*  
> *No `conftest.py`, criamos fixtures com o ciclo completo de **setup e teardown via yield**, garantindo o isolamento de estado do repositório a cada teste.*  
> *Aqui no arquivo de testes de integração, seguimos estritamente o padrão **AAA (Arrange, Act, Assert)**.*  
> *Isolamos a dependência externa de notificação utilizando `mocker.patch`: no primeiro teste, validamos o cenário de sucesso com status 201 e status CONFIRMADO. E no segundo teste, simulamos uma falha do serviço externo com `side_effect=NotificationDeliveryError`, onde a aplicação aplica degradação graciosa, registrando o agendamento como PENDENTE_NOTIFICACAO sem derrubar o sistema."*

---

### 🔹 BLOCO 3: E2E com Playwright (POM) e Acessibilidade com Axe-core (01:55 a 02:55)

#### 🖥️ O que mostrar na tela:
1. Abra o arquivo [tests/e2e/pages/appointment_page.py](file:///c:/Users/Roky/AT2-Testes-de-Integracao-E2E-com-Playwright-Acessibilidade-e-Carga/tests/e2e/pages/appointment_page.py) e aponte para:
   - Linhas **12 a 28**: O Page Object Model encapsulando os seletores semânticos: `get_by_role`, `get_by_label` e `get_by_text`.
2. Abra o arquivo [tests/e2e/test_appointment_e2e.py](file:///c:/Users/Roky/AT2-Testes-de-Integracao-E2E-com-Playwright-Acessibilidade-e-Carga/tests/e2e/test_appointment_e2e.py) e aponte para:
   - Linhas **10 a 50**: O fluxo ponta a ponta preenchendo o formulário, submetendo e conferindo a mensagem de sucesso na interface web.
3. Abra o arquivo [tests/e2e/test_accessibility.py](file:///c:/Users/Roky/AT2-Testes-de-Integracao-E2E-com-Playwright-Acessibilidade-e-Carga/tests/e2e/test_accessibility.py) e aponte para:
   - Linhas **15 a 45**: Auditoria automatizada **WCAG 2.1 AA** com o motor `Axe(page).run()`, assinalando a garantia de **0 violações**.
   - Linhas **50 a 95**: Teste de navegabilidade por teclado sequencial acionando `page.keyboard.press("Tab")` e checando o foco com `expect(locator).to_be_focused()`.

#### 🗣️ O que falar (Roteiro falado):
> *"No topo da pirâmide de testes, implementamos os testes End-to-End com **Playwright** adotando o padrão **Page Object Model** no arquivo `appointment_page.py`.*  
> *Note que utilizamos estritamente seletores semânticos como `get_by_role`, `get_by_label` e `get_by_text`, tornando os testes desacoplados da estrutura CSS e resilientes a mudanças.*  
> *Para os requisitos de Acessibilidade da ISO 25010 e WCAG 2.1 AA, criamos o arquivo `test_accessibility.py`.*  
> *Aqui executamos o motor do **Axe-core** na página da aplicação para auditar contraste de cores, rótulos e marcos semânticos, garantindo zero violações. Além disso, criamos um teste específico que simula um usuário navegando exclusivamente pela tecla Tab, validando o foco em cada elemento através de asserções `to_be_focused()`."*

---

### 🔹 BLOCO 4: Execução Prática no Terminal (Pytest e Locust) (02:55 a 03:55)

#### 🖥️ O que mostrar na tela:
1. Abra o terminal integrado e digite o comando:
   ```bash
   uv run pytest -v
   ```
   Aguarde os 5 segundos de execução e mostre os **13 testes passando em verde**.
2. Abra o arquivo [locustfile.py](file:///c:/Users/Roky/AT2-Testes-de-Integracao-E2E-com-Playwright-Acessibilidade-e-Carga/locustfile.py) brevemente (linhas 10 a 45) mostrando as tarefas com pesos `@task(4)`, `@task(3)`, `@task(2)`.
3. Abra o [README.md](file:///c:/Users/Roky/AT2-Testes-de-Integracao-E2E-com-Playwright-Acessibilidade-e-Carga/README.md) na tabela de métricas de carga (linhas 120 a 140) ou execute o comando headless:
   ```bash
   uv run locust --headless -u 50 -r 10 --run-time 10s --host http://127.0.0.1:8000
   ```
   (Se o servidor estiver no ar, ou simplesmente aponte a tabela de métricas documentada no README).

#### 🗣️ O que falar (Roteiro falado):
> *"Vamos agora executar a suíte de testes completa no terminal utilizando o comando `uv run pytest -v`.*  
> *(Aguarde os testes rodarem)*  
> *Como podemos ver no terminal, todos os 13 testes passaram com 100% de sucesso em pouco mais de 5 segundos, cobrindo integração, E2E e acessibilidade.*  
> *Por fim, para a avaliação de desempenho da ISO 25010, elaboramos o `locustfile.py` com tarefas ponderadas simulando usuários reais.*  
> *Executamos um teste de carga com 50 usuários concorrentes. Conforme documentado na tabela de métricas do nosso README, obtivemos uma vazão de 26.81 requisições por segundo, com tempo de resposta percentil 95 de apenas 32 milissegundos — bem abaixo do limite de 500 ms — e com taxa de falhas absoluta de 0.00%."*

---

### 🔹 BLOCO 5: Encerramento (03:55 a 04:00)

#### 🖥️ O que mostrar na tela:
- Tela inicial do repositório no VS Code ou o topo do README.md.

#### 🗣️ O que falar:
> *"Com isso, cobrimos com êxito todos os níveis da pirâmide de testes e os critérios de qualidade da atividade AT2. Muito obrigado pela atenção!"*

---

## 📋 Checklist Rápido Pré-Gravação
- [ ] O ambiente virtual está pronto (`uv sync`).
- [ ] O Chromium do Playwright está instalado (`uv run playwright install chromium`).
- [ ] O comando `uv run pytest -v` foi testado previamente e está passando 13/13.
- [ ] As abas dos arquivos principais estão abertas no VS Code na ordem da gravação:
  1. `PRD.md`
  2. `tests/factories/appointment_factory.py`
  3. `tests/conftest.py`
  4. `tests/integration/test_appointments_integration.py`
  5. `tests/e2e/pages/appointment_page.py`
  6. `tests/e2e/test_accessibility.py`
  7. `locustfile.py` e `README.md`
- [ ] O microfone está configurado e o gravador de tela pronto para iniciar.

