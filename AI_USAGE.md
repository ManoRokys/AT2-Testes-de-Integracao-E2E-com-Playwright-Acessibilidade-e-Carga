# Relatório de Uso e Transparência de IA (AI_USAGE.md)

**Atividade:** AT2 — Testes de Integração, E2E com Playwright, Acessibilidade e Carga  
**Disciplina:** Qualidade e Teste de Software (QTS) — FATEC Registro  
**Estudante:** Luca Fagundes  
**Aplicação:** AutoCar - Agendamento de Serviços e Revisões Automotivas  

---

## 1. Declaração de Uso Mínimo e Pontual de IA

Nesta atividade prática, o uso de Inteligência Artificial foi **estritamente mínimo e pontual**, servindo apenas como suporte secundário para tirar dúvidas de sintaxe e consultar documentações de bibliotecas. 

A concepção da aplicação, as regras de negócio automotivas, a estruturação dos testes (integração, E2E, acessibilidade e carga) e a validação do código foram conduzidas pelo estudante.

---

## 2. Em que a IA foi consultada (Uso Limitado)

1. **Sintaxe da biblioteca `axe-playwright-python`:** Consulta pontual sobre os parâmetros do método `Axe().run()`.
2. **Compatibilidade do Pydantic v2:** Dúvida rápida sobre a anotação `@field_validator` em relação aos validadores antigos da versão v1.
3. **Comandos de linha de comando do `uv`:** Consulta dos comandos para adicionar grupos de desenvolvimento (`uv add --dev`).

---

## 3. O que foi feito integralmente pelo Aluno

- **Escolha do Domínio:** Criação do tema de oficina mecânica e revisão de carros (AutoCar).
- **Regras de Negócio:** Validação de placas brasileiras/Mercosul, checagem de nome/sobrenome e datas futuras.
- **Arquitetura do Projeto:** Separação das pastas em `app/` e `tests/`, criação dos modelos, rotas e repositório em memória.
- **Engenharia de Testes:**
  - Criação da Factory de carros com `Faker("pt_BR")`.
  - Construção das fixtures com `yield` para setup e teardown limpos.
  - Escrita dos testes de integração no padrão **AAA** com mocks de sucesso e falha via `mocker.patch`.
  - Desenvolvimento do **Page Object Model** com seletores semânticos do Playwright.
  - Elaboração do teste de foco sequencial de teclado (`Tab` e `to_be_focused()`).
  - Configuração das tarefas ponderadas no `locustfile.py` e execução do teste de carga.
- **Interface e Acessibilidade:** Construção manual do HTML semântico com contraste adequado para passar sem violações no Axe-core.

---

## 4. Conclusão
A autoria do projeto é do próprio estudante, com total domínio sobre o código-fonte, a execução dos testes e a análise dos resultados obtidos.
