document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form-agendamento");
  const alertBox = document.getElementById("alert-status");
  const tableBody = document.getElementById("tabela-agendamentos-body");
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
      <td><strong>${escapeHtml(item.paciente_nome)}</strong></td>
      <td>${escapeHtml(item.especialidade)}</td>
      <td>${formatDateTime(item.data_horario)}</td>
      <td><span class="badge badge-${escapeHtml(item.status)}">${escapeHtml(item.status)}</span></td>
      <td>
        <button type="button" class="btn-cancel" data-id="${escapeHtml(item.id)}" aria-label="Cancelar agendamento de ${escapeHtml(item.paciente_nome)}">
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
      if (!confirm("Deseja realmente cancelar este agendamento?")) {
        return;
      }
      try {
        const response = await fetch(`/api/agendamentos/${id}/cancelar`, {
          method: "PATCH",
        });
        if (response.ok) {
          const data = await response.json();
          const row = document.getElementById(`row-${id}`);
          if (row) {
            const statusCell = row.children[3];
            statusCell.innerHTML = `<span class="badge badge-CANCELADO">CANCELADO</span>`;
            btn.disabled = true;
            btn.textContent = "Cancelado";
          }
          showAlert("Agendamento cancelado com sucesso.", "success");
        } else {
          showAlert("Não foi possível cancelar o agendamento.", "error");
        }
      } catch (err) {
        showAlert("Erro de rede ao cancelar agendamento.", "error");
      }
    });
  }

  // Attach handlers to existing buttons rendered by Jinja
  document.querySelectorAll(".btn-cancel").forEach(attachCancelHandler);

  if (form) {
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      hideAlert();

      const nome = document.getElementById("paciente_nome").value.trim();
      const email = document.getElementById("paciente_email").value.trim();
      const telefone = document.getElementById("paciente_telefone").value.trim();
      const especialidade = document.getElementById("especialidade").value;
      const dataHorario = document.getElementById("data_horario").value;
      const observacoes = document.getElementById("observacoes").value.trim();

      const payload = {
        paciente_nome: nome,
        paciente_email: email,
        paciente_telefone: telefone,
        especialidade: especialidade,
        data_horario: new Date(dataHorario).toISOString(),
        observacoes: observacoes || null,
      };

      try {
        const response = await fetch("/api/agendamentos", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        });

        const data = await response.json();

        if (response.ok) {
          showAlert("Agendamento realizado com sucesso!", "success");
          appendRowToTable(data);
          form.reset();
        } else {
          const errorMsg = data.detail
            ? Array.isArray(data.detail)
              ? data.detail.map((e) => e.msg).join(", ")
              : data.detail
            : "Erro ao processar agendamento.";
          showAlert(`Erro: ${errorMsg}`, "error");
        }
      } catch (err) {
        showAlert("Falha na conexão com o servidor da clínica.", "error");
      }
    });
  }
});

