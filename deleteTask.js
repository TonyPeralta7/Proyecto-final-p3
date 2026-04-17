// ─── Eliminar tarea con confirmación ─────────────────────────────────────
function deleteTask(index) {
  const confirmed = confirm(`¿Estás seguro de que deseas eliminar la tarea "${tasks[index].title}"?`);
  if (!confirmed) return;

  tasks.splice(index, 1);
  saveTasks();
  renderTasks();
}
