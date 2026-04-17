// ─── Guardar tarea (crear o editar) ───────────────────────────────────────
function saveTask() {
  const title       = document.getElementById("taskTitle").value.trim();
  const description = document.getElementById("taskDescription").value.trim();
  const dueDate     = document.getElementById("taskDueDate").value;
  const priority    = document.getElementById("taskPriority").value;
  const editIndex   = parseInt(document.getElementById("editIndex").value);
  const titleError  = document.getElementById("titleError");

  // Validación de título obligatorio
  if (title === "") {
    titleError.style.display = "block";
    return;
  }
  titleError.style.display = "none";

  const task = {
    title,
    description,
    dueDate,
    priority,
    completed: false,
  };

  if (editIndex === -1) {
    // CREAR nueva tarea
    tasks.push(task);
  } else {
    // ACTUALIZAR tarea existente (conservar estado completado)
    task.completed = tasks[editIndex].completed;
    tasks[editIndex] = task;
  }

  saveTasks();
  cancelEdit();
  renderTasks();
}
