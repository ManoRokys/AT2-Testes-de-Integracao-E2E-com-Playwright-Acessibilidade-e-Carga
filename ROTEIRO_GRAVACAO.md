# Roteiro para Gravação do Vídeo Demonstrativo (Até 4 Minutos)
## Atividade AT2 — Qualidade e Teste de Software (QTS) — FATEC Registro
**Estudante:** Luca Fagundes  
**Aplicação:** AutoCar - Agendamento de Serviços e Revisões Automotivas  

---

## 🎯 Dicas Rápidas para a Gravação
- **Tempo Limite:** Máximo de 4 minutos (240 segundos).
- **Formato:** Gravação da tela do computador com áudio. Não precisa aparecer na câmera.
- **Preparação:** Deixe as abas dos arquivos já abertas no VS Code na ordem abaixo e um terminal pronto para rodar os testes.

---

## ⏱️ Minutagem do Vídeo

```text
[00:00 - 00:50] Bloco 1: Apresentação, Domínio de Carros, PRD e Governança
[00:50 - 01:55] Bloco 2: Integração, Fixtures com Yield, Mocks e Factory com Faker
[01:55 - 02:55] Bloco 3: E2E com Playwright (POM) e Acessibilidade WCAG com Axe-core
[02:55 - 03:55] Bloco 4: Execução Prática no Terminal (Pytest e Locust)
[03:55 - 04:00] Bloco 5: Conclusão
```

---

## 🎬 Roteiro Passo a Passo (Linhas de Código e O Que Falar)

---

### 🔹 BLOCO 1: Apresentação, Tema de Carros e Governança (00:00 a 00:50)

#### 🖥️ O que mostrar na tela:
1. Abra o arquivo [PRD.md](file:///c:/Users/Roky/AT2-Testes-de-Integracao-E2E-com-Playwright-Acessibilidade-e-Carga/PRD.md) nas **linhas 12 a 45** (rotas de agendamento de revisão e validações) e **linhas 55 a 65** (tabela da ISO/IEC 25010).
2. Abra rapidamente o [AI_USAGE.md](file:///c:/Users/Roky/AT2-Testes-de-Integracao-E2E-com-Playwright-Acessibilidade-e-Carga/AI_USAGE.md) nas **linhas 10 a 35** destacando a declaração de uso mínimo de IA.
3. Abra o [app/models.py](file:///c:/Users/Roky/AT2-Testes-de-Integracao-E2E-com-Playwright-Acessibilidade-e-Carga/app/models.py) nas **linhas 22 a 55** (modelos Pydantic v2 validando placa do carro e datas futuras).

#### 🗣️ O que falar:
> *"Olá professor(a)! Meu nome é Luca Fagundes e esta é a apresentação da atividade prática AT2 de Qualidade e Teste de Software.*  
> *Para o trabalho, escolhi o domínio automotivo e desenvolvi o **AutoCar**, um sistema em Python com FastAPI e Pydantic para agendamento de revisões e serviços mecânicos em oficinas.*  
> *Aqui no **PRD.md**, especifiquei as rotas da API e os requisitos não funcionais alinhados à norma **ISO/IEC 25010**, cobrindo usabilidade WCAG 2.1 AA, eficiência de desempenho e confiabilidade.*  
> *Também deixei registrado no **AI_USAGE.md** e no **AGENTS.md** que a atividade foi feita por mim, utilizando IA de forma mínima apenas para consultas pontuais de sintaxe de bibliotecas.*  
> *No código, como vemos em `models.py`, criamos validações estritas com Pydantic v2 para garantir placa válida no padrão brasileiro, nome e sobrenome do cliente e datas futuras."*

---

### 🔹 BLOCO 2: Testes de Integração, Fixtures, Mocks e Faker (00:50 a 01:55)

#### 🖥️ O que mostrar na tela:
1. Abra [tests/factories/carro_factory.py](file:///c:/Users/Roky/AT2-Testes-de-Integracao-E2E-com-Playwright-Acessibilidade-e-Carga/tests/factories/carro_factory.py) e mostre as **linhas 15 a 45**: a geração de placas válidas, modelos de carros populares e dados dinâmicos com `Faker("pt_BR")`.
2. Abra [tests/conftest.py](file:///c:/Users/Roky/AT2-Testes-de-Integracao-E2E-com-Playwright-Acessibilidade-e-Carga/tests/conftest.py) nas **linhas 16 a 32**: a fixture `limpar_dados_repo` e `client` com o ciclo de **setup e teardown via yield**.
3. Abra [tests/integration/test_revisoes_integration.py](file:///c:/Users/Roky/AT2-Testes-de-Integracao-E2E-com-Playwright-Acessibilidade-e-Carga/tests/integration/test_revisoes_integration.py):
   - Aponte para as **linhas 10 a 40**: padrão **Arrange, Act, Assert (AAA)** e o mock de sucesso via `mocker.patch("app.main.notificacao_service.enviar_confirmacao")`.
   - Aponte para as **linhas 45 a 70**: o mock com `side_effect=FalhaEnvioNotificacaoError` testando a resiliência do sistema e o status `PENDENTE_AVISO`.

#### 🗣️ O que falar:
> *"Na camada de integração, estruturei a geração de massa de testes através do padrão **Factory** no arquivo `carro_factory.py`, utilizando a biblioteca **Faker** para gerar dados sintéticos dinâmicos como nomes brasileiros, modelos de veículos e placas válidas.*  
> *No `conftest.py`, criei fixtures utilizando **setup e teardown com yield**, garantindo que o repositório seja limpo antes e depois de cada teste.*  
> *Nos testes de integração em `test_revisoes_integration.py`, segui à risca o padrão **AAA (Arrange, Act, Assert)**.*  
> *Isolei o serviço externo de mensagens usando `mocker.patch`: no primeiro teste valido o cenário de sucesso com retorno 201 e status CONFIRMADO. E no segundo teste simulo uma falha de conexão na mensageria com `side_effect`, comprovando que o sistema aplica degradação graciosa, salvando o agendamento como PENDENTE_AVISO sem quebrar a requisição."*

---

### 🔹 BLOCO 3: E2E com Playwright (POM) e Acessibilidade WCAG (01:55 a 02:55)

#### 🖥️ O que mostrar na tela:
1. Abra [tests/e2e/pages/revisao_page.py](file:///c:/Users/Roky/AT2-Testes-de-Integracao-E2E-com-Playwright-Acessibilidade-e-Carga/tests/e2e/pages/revisao_page.py) e aponte para as **linhas 12 a 28**: Page Object Model utilizando seletores semânticos (`get_by_role`, `get_by_label`).
2. Abra [tests/e2e/test_revisao_e2e.py](file:///c:/Users/Roky/AT2-Testes-de-Integracao-E2E-com-Playwright-Acessibilidade-e-Carga/tests/e2e/test_revisao_e2e.py) nas **linhas 10 a 45**: fluxo de ponta a ponta preenchendo o formulário do carro e conferindo na tabela.
3. Abra [tests/e2e/test_accessibility.py](file:///c:/Users/Roky/AT2-Testes-de-Integracao-E2E-com-Playwright-Acessibilidade-e-Carga/tests/e2e/test_accessibility.py):
   - Aponte para as **linhas 10 a 28**: auditoria automatizada WCAG 2.1 AA com `Axe().run()` garantindo **0 violações**.
   - Aponte para as **linhas 30 a 70**: teste de navegação sequencial por teclado com `page.keyboard.press("Tab")` e checagens `expect(campo).to_be_focused()`.

#### 🗣️ O que falar:
> *"No nível End-to-End, implementei os testes com **Playwright** adotando o padrão **Page Object Model** no arquivo `revisao_page.py`.*  
> *Utilizei apenas seletores semânticos e amigáveis à acessibilidade, como `get_by_role` e `get_by_label`, evitando seletores CSS frágeis.*  
> *Para atender aos requisitos de Acessibilidade da ISO 25010 e WCAG 2.1 AA, criei o arquivo `test_accessibility.py`.*  
> *Nele, rodo o motor do **Axe-core** na interface web da oficina para verificar contraste, labels e tags HTML, atestando zero violações de acessibilidade. Além disso, fiz um teste que simula o uso exclusivo do teclado, percorrendo o formulário com a tecla Tab e validando cada foco com `to_be_focused()`."*

---

### 🔹 BLOCO 4: Execução Prática no Terminal (Pytest e Locust) (02:55 a 03:55)

#### 🖥️ O que mostrar na tela:
1. Abra o terminal e digite:
   ```bash
   uv run pytest -v
   ```
   Aguarde os testes rodarem e aponte os **13 testes passando em verde**.
2. Abra o arquivo [locustfile.py](file:///c:/Users/Roky/AT2-Testes-de-Integracao-E2E-com-Playwright-Acessibilidade-e-Carga/locustfile.py) nas **linhas 8 a 30** mostrando as tarefas `@task(4)`, `@task(3)` e `@task(2)`.
3. Abra o [README.md](file:///c:/Users/Roky/AT2-Testes-de-Integracao-E2E-com-Playwright-Acessibilidade-e-Carga/README.md) na tabela de métricas do teste de carga (**linhas 110 a 130**).

#### 🗣️ O que falar:
> *"Agora vou rodar todos os testes automatizados no terminal com `uv run pytest -v`.*  
> *(Aguarde a execução)*  
> *Como podemos ver, todos os 13 testes foram executados com sucesso em cerca de 6 segundos, cobrindo integração com mocks, ponta a ponta com Playwright e acessibilidade.*  
> *Por fim, para avaliar o desempenho segundo a ISO 25010, criei o `locustfile.py` com tarefas ponderadas simulando motoristas agendando revisões e consultando serviços.*  
> *Executamos um teste de carga com 40 usuários simultâneos. Conforme documentado na tabela de métricas do nosso README, obtivemos uma vazão de 21 requisições por segundo, tempo de resposta percentil 95 de apenas 50 milissegundos — muito abaixo do limite de 500 ms — e taxa de falhas absoluta de 0.00%."*

---

### 🔹 BLOCO 5: Encerramento (03:55 a 04:00)

#### 🖥️ O que mostrar na tela:
- O topo do arquivo README.md.

#### 🗣️ O que falar:
> *"Com isso, cobrimos todos os requisitos práticos da atividade AT2 e os padrões de qualidade de software. Muito obrigado!"*
