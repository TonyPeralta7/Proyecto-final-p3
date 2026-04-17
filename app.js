// ─── Estado global ─────────────────────────────────────────────────────────
let tasks = JSON.parse(localStorage.getItem("tasks")) || [];
let currentFilter = "all";

// ─── Persistencia ──────────────────────────────────────────────────────────
function saveTasks() {
  localStorage.setItem("tasks", JSON.stringify(tasks));
}

// ─── Filtro ────────────────────────────────────────────────────────────────
function setFilter(filter) {
  currentFilter = filter;

  document.querySelectorAll(".filter-btn").forEach(btn => btn.classList.remove("active"));
  document.getElementById("filter-" + filter).classList.add("active");

  renderTasks();
}

// ─── Render ────────────────────────────────────────────────────────────────
function renderTasks() {
  const list = document.getElementById("taskList");
  const emptyMsg = document.getElementById("emptyMsg");
  const taskCount = document.getElementById("taskCount");

  list.innerHTML = "";

  let filtered = tasks.filter(task => {
    if (currentFilter === "pending")   return !task.completed;
    if (currentFilter === "completed") return task.completed;
    return true;
  });

  taskCount.textContent = filtered.length + " tarea(s)";

  if (filtered.length === 0) {
    emptyMsg.style.display = "block";
    return;
  }
  emptyMsg.style.display = "none";

  filtered.forEach((task) => {
    const realIndex = tasks.indexOf(task);
    const priorityClass = "priority-" + task.priority.toLowerCase();

    const li = document.createElement("li");
    li.className = "task-item" + (task.completed ? " completed" : "");
    li.setAttribute("data-index", realIndex);

    li.innerHTML = `
      <div class="task-header">
        <span class="task-title">${task.title}</span>
        <span class="badge ${priorityClass}">${task.priority}</span>
      </div>
      ${task.description ? `<p class="task-desc">${task.description}</p>` : ""}
      ${task.dueDate ? `<p class="task-date">📅 ${task.dueDate}</p>` : ""}
      <div class="task-actions">
        <button class="btn-complete" onclick="toggleComplete(${realIndex})">
          ${task.completed ? "Reactivar" : "Completar"}
        </button>
        <button class="btn-edit" onclick="editTask(${realIndex})">Editar</button>
        <button class="btn-delete" onclick="deleteTask(${realIndex})">Eliminar</button>
      </div>
    `;
    list.appendChild(li);
  });
}

// ─── Marcar como completada / reactivar ───────────────────────────────────
function toggleComplete(index) {
  tasks[index].completed = !tasks[index].completed;
  saveTasks();
  renderTasks();
}

// ─── Cancelar edición ─────────────────────────────────────────────────────
function cancelEdit() {
  document.getElementById("editIndex").value = "-1";
  document.getElementById("taskTitle").value = "";
  document.getElementById("taskDescription").value = "";
  document.getElementById("taskDueDate").value = "";
  document.getElementById("taskPriority").value = "Media";
  document.getElementById("formTitle").textContent = "Nueva Tarea";
  document.getElementById("saveBtn").textContent = "Agregar Tarea";
  document.getElementById("cancelBtn").style.display = "none";
  document.getElementById("titleError").style.display = "none";
}

// ─── Inicializar ──────────────────────────────────────────────────────────
window.onload = function () {
  renderTasks();
};
