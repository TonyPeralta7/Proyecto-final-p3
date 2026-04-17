// ─── Cargar tarea en formulario para editar ───────────────────────────────
function editTask(index) {
  const task = tasks[index];

  document.getElementById("editIndex").value       = index;
  document.getElementById("taskTitle").value       = task.title;
  document.getElementById("taskDescription").value = task.description || "";
  document.getElementById("taskDueDate").value     = task.dueDate || "";
  document.getElementById("taskPriority").value    = task.priority || "Media";

  document.getElementById("formTitle").textContent  = "Editar Tarea";
  document.getElementById("saveBtn").textContent    = "Guardar Cambios";
  document.getElementById("cancelBtn").style.display = "inline-block";

  // Scroll al formulario
  document.querySelector(".form-section").scrollIntoView({ behavior: "smooth" });
}
