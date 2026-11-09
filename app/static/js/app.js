// Script da interface web da oficina AutoCar
// Autor: Lucas Gomes Fagundes (QTS - FATEC Registro)

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form-revisao");
  const alertBox = document.getElementById("alert-status");
  const tableBody = document.getElementById("tabela-revisoes-body");
  const emptyState = document.getElementById("empty-state");

  function showAlert(message, type = "success") {
    alertBox.textContent = message;
    alertBox.className = `alert alert-${type}`;
    alertBox.style.display = "block";
    alertBox.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  function hideAlert() {
    alertBox.style.display = "none";
    alertBox.textContent = "";
  }

  function formatDateTime(isoString) {
    try {
      const date = new Date(isoString);
      return date.toLocaleString("pt-BR", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    } catch {
      return isoString;
    }
  }

  function appendRowToTable(item) {
    if (emptyState) {
      emptyState.style.display = "none";
    }

    const row = document.createElement("tr");
    row.id = `row-${item.id}`;
    row.innerHTML = `
      <td><strong>${escapeHtml(item.cliente_nome)}</strong></td>
      <td>${escapeHtml(item.veiculo_modelo)} (${escapeHtml(item.veiculo_placa)})</td>
      <td>${escapeHtml(item.tipo_servico)}</td>
      <td>${formatDateTime(item.data_horario)}</td>
      <td><span class="badge badge-${escapeHtml(item.status)}">${escapeHtml(item.status)}</span></td>
      <td>
        <button type="button" class="btn-cancel" data-id="${escapeHtml(item.id)}" aria-label="Cancelar agendamento de ${escapeHtml(item.cliente_nome)}">
          Cancelar
        </button>
      </td>
    `;
    tableBody.prepend(row);
    attachCancelHandler(row.querySelector(".btn-cancel"));
  }

  function escapeHtml(str) {
    if (!str) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function attachCancelHandler(btn) {
    if (!btn) return;
    btn.addEventListener("click", async () => {
      const id = btn.getAttribute("data-id");
      if (!confirm("Deseja cancelar o agendamento desta revisão?")) {
        return;
      }
      try {
        const response = await fetch(`/api/revisoes/${id}/cancelar`, {
          method: "PATCH",
        });
        if (response.ok) {
          const row = document.getElementById(`row-${id}`);
          if (row) {
            const statusCell = row.children[4];
            statusCell.innerHTML = `<span class="badge badge-CANCELADO">CANCELADO</span>`;
            btn.disabled = true;
            btn.textContent = "Cancelado";
          }
          showAlert("Agendamento de revisão cancelado com sucesso.", "success");
        } else {
          showAlert("Não foi possível cancelar o agendamento.", "error");
        }
      } catch (err) {
        showAlert("Erro ao se comunicar com a oficina.", "error");
      }
    });
  }

  document.querySelectorAll(".btn-cancel").forEach(attachCancelHandler);

  if (form) {
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      hideAlert();

      const nome = document.getElementById("cliente_nome").value.trim();
      const email = document.getElementById("cliente_email").value.trim();
      const telefone = document.getElementById("cliente_telefone").value.trim();
      const modelo = document.getElementById("veiculo_modelo").value.trim();
      const placa = document.getElementById("veiculo_placa").value.trim();
      const servico = document.getElementById("tipo_servico").value;
      const dataHorario = document.getElementById("data_horario").value;
      const observacoes = document.getElementById("observacoes").value.trim();

      const payload = {
        cliente_nome: nome,
        cliente_email: email,
        cliente_telefone: telefone,
        veiculo_modelo: modelo,
        veiculo_placa: placa,
        tipo_servico: servico,
        data_horario: new Date(dataHorario).toISOString(),
        observacoes: observacoes || null,
      };

      try {
        const response = await fetch("/api/revisoes", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        });

        const data = await response.json();

        if (response.ok) {
          showAlert("Agendamento de revisão realizado com sucesso!", "success");
          appendRowToTable(data);
          form.reset();
        } else {
          const msg = data.detail
            ? Array.isArray(data.detail)
              ? data.detail.map((e) => e.msg).join(", ")
              : data.detail
            : "Erro ao registrar revisão.";
          showAlert(`Erro: ${msg}`, "error");
        }
      } catch (err) {
        showAlert("Erro de conexão com o servidor da oficina.", "error");
      }
    });
  }
});
