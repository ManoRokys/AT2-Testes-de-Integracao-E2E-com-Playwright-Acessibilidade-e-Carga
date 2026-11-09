# Documento de Requisitos de Produto (PRD)
## Sistema: AutoCar - Agendamento de Serviços Automotivos e Revisões

**Disciplina:** Qualidade e Teste de Software (QTS) — FATEC Registro  
**Autor:** Lucas Gomes Fagundes  
**Curso:** Desenvolvimento de Software Multiplataforma (DSM)  
**Semestre:** 2026  

---

## 1. Visão Geral
O **AutoCar** é um sistema web e API REST desenvolvido para facilitar o agendamento de revisões preventivas e manutenções mecânicas em oficinas automotivas. O motorista pode escolher o serviço, informar dados do seu carro (modelo e placa) e receber a confirmação por mensagem externa.

---

## 2. Rotas da API REST

### 2.1. `POST /api/revisoes`
- **Função:** Cadastra um novo agendamento de revisão para um carro e aciona o serviço de aviso.
- **Status Sucesso:** `201 Created`
- **Status Erro de Validação:** `422 Unprocessable Entity`
- **Payload:**
  ```json
  {
    "cliente_nome": "Lucas Silva",
    "cliente_email": "lucas.silva@exemplo.com.br",
    "cliente_telefone": "(13) 99876-5432",
    "veiculo_modelo": "Volkswagen Gol 1.6",
    "veiculo_placa": "BRA2E19",
    "tipo_servico": "Troca de Óleo",
    "data_horario": "2026-11-25T09:00:00Z",
    "observacoes": "Trocar filtro de óleo e checar nível de água."
  }
  ```
- **Validações aplicadas (Pydantic):**
  - Nome deve ter pelo menos duas palavras (nome e sobrenome).
  - Placa deve seguir o padrão brasileiro de 7 caracteres (comum ou Mercosul).
  - Data do agendamento deve ser estritamente no futuro.

### 2.2. `GET /api/revisoes`
- **Função:** Lista todos os agendamentos cadastrados.
- **Status:** `200 OK`

### 2.3. `GET /api/revisoes/{id}`
- **Função:** Busca os detalhes de uma revisão específica.
- **Status:** `200 OK` ou `404 Not Found`.

### 2.4. `PATCH /api/revisoes/{id}/cancelar`
- **Função:** Cancela o agendamento de uma revisão.
- **Status:** `200 OK` ou `404 Not Found`.

### 2.5. `GET /health`
- **Função:** Rota simples de checagem para testes de carga e monitoramento.
- **Status:** `200 OK`

---

## 3. Interface Web Acessível (`GET /`)
- HTML5 semântico com navegação por teclado fluida.
- Suporte a leitor de telas com link de salto rápido (*skip link*).
- Mensagens de feedback dinâmicas através de `role="status"` e `aria-live="polite"`.
- Campos de formulário com rótulos explícitos `<label for="...">`.
- Tabela com listagem dos carros agendados e botão de cancelamento.

---

## 4. Requisitos Não Funcionais (ISO/IEC 25010)

| Característica | Critério de Aceite |
| :--- | :--- |
| **Adequação Funcional** | Validações de nome, placa e datas futuras garantidas por testes automatizados de integração. |
| **Eficiência de Desempenho** | Sob teste de carga com o Locust, tempo de resposta percentil 95 abaixo de 500 ms e 0% de falhas. |
| **Usabilidade / Acessibilidade** | Conformidade com WCAG 2.1 AA validada via **Axe-core** (0 violações) e navegação completa por teclado via `Tab`. |
| **Confiabilidade** | Degradação graciosa: se o serviço externo de mensagem falhar, a revisão é salva como `PENDENTE_AVISO` sem gerar erro 500 para o cliente. |
| **Manutenibilidade** | Código modular com Factory (`Faker`), Page Object Model no E2E e fixtures com `yield`. |
