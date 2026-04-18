"""
Pruebas automatizadas con Selenium WebDriver
Sistema: Task Manager CRUD
Autor: Tony Manuel Peralta De Luna (2024-1808)
Herramienta: Selenium + pytest + ChromeDriver

Instalación:
    pip install selenium pytest pytest-html

Uso:
    pytest test_task_manager.py --html=report.html --self-contained-html
"""

import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


# ─── Configuración ────────────────────────────────────────────────────────────
BASE_URL = "file:///C:/Users/Tony Peralta/Desktop/Proyecto final/index.html"  # Cambiar a la URL real o ruta local
WAIT = 5  # segundos de espera máxima


@pytest.fixture(scope="module")
def driver():
    """Inicializa y cierra el navegador para todos los tests del módulo."""
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Descomentar para correr sin ventana
    d = webdriver.Chrome(options=options)
    d.maximize_window()
    d.get(BASE_URL)
    time.sleep(1)
    yield d
    d.quit()


def wait_for(driver, by, selector, timeout=WAIT):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, selector))
    )


# ─── CP-01: Crear tarea con todos los campos ─────────────────────────────────
def test_CP01_crear_tarea_completa(driver):
    """CP-01 | US-01: Crear una tarea con todos los campos completos."""
    driver.find_element(By.ID, "taskTitle").clear()
    driver.find_element(By.ID, "taskTitle").send_keys("Tarea de prueba automatizada")
    driver.find_element(By.ID, "taskDescription").send_keys("Descripción generada por Selenium")
    driver.find_element(By.ID, "taskDueDate").send_keys("2026-05-01")
    Select(driver.find_element(By.ID, "taskPriority")).select_by_visible_text("Alta")
    driver.find_element(By.ID, "saveBtn").click()
    time.sleep(0.5)

    items = driver.find_elements(By.CLASS_NAME, "task-item")
    assert len(items) > 0, "No se creó ninguna tarea"
    titles = [i.find_element(By.CLASS_NAME, "task-title").text for i in items]
    assert "Tarea de prueba automatizada" in titles, "La tarea no aparece en la lista"
    print("CP-01 PASS: Tarea creada correctamente")


# ─── CP-02: Crear tarea sin título (validación) ───────────────────────────────
def test_CP02_crear_tarea_sin_titulo(driver):
    """CP-02 | US-01: El sistema debe rechazar una tarea sin título."""
    driver.find_element(By.ID, "taskTitle").clear()
    driver.find_element(By.ID, "saveBtn").click()
    time.sleep(0.3)

    error = driver.find_element(By.ID, "titleError")
    assert error.is_displayed(), "El mensaje de error no se mostró"
    print("CP-02 PASS: Validación de título obligatorio funciona correctamente")


# ─── CP-03: Editar una tarea ──────────────────────────────────────────────────
def test_CP03_editar_tarea(driver):
    """CP-03 | US-03: Editar el título de una tarea existente."""
    items = driver.find_elements(By.CLASS_NAME, "task-item")
    assert len(items) > 0, "No hay tareas para editar"

    items[0].find_element(By.CLASS_NAME, "btn-edit").click()
    time.sleep(0.5)

    title_input = driver.find_element(By.ID, "taskTitle")
    title_input.clear()
    title_input.send_keys("Tarea editada por Selenium")
    driver.find_element(By.ID, "saveBtn").click()
    time.sleep(0.5)

    items_after = driver.find_elements(By.CLASS_NAME, "task-item")
    titles = [i.find_element(By.CLASS_NAME, "task-title").text for i in items_after]
    assert "Tarea editada por Selenium" in titles, "El título no se actualizó"
    print("CP-03 PASS: Tarea editada correctamente")


# ─── CP-05: Marcar tarea como completada ─────────────────────────────────────
def test_CP05_marcar_completada(driver):
    """CP-05 | US-05: Marcar una tarea como completada."""
    items = driver.find_elements(By.CLASS_NAME, "task-item")
    first = items[0]
    btn_complete = first.find_element(By.CLASS_NAME, "btn-complete")
    assert btn_complete.text == "Completar", "El botón debería decir 'Completar'"
    btn_complete.click()
    time.sleep(0.5)

    items_after = driver.find_elements(By.CLASS_NAME, "task-item")
    first_after = items_after[0]
    assert "completed" in first_after.get_attribute("class"), "La tarea no tiene clase 'completed'"
    btn_after = first_after.find_element(By.CLASS_NAME, "btn-complete")
    assert btn_after.text == "Reactivar", "El botón debería decir 'Reactivar'"
    print("CP-05 PASS: Tarea marcada como completada")


# ─── CP-06: Filtrar por estado ────────────────────────────────────────────────
def test_CP06_filtrar_pendientes(driver):
    """CP-06 | US-06: Filtrar tareas por estado 'Pendientes'."""
    driver.find_element(By.ID, "filter-pending").click()
    time.sleep(0.5)

    items = driver.find_elements(By.CLASS_NAME, "task-item")
    for item in items:
        assert "completed" not in item.get_attribute("class"), \
            "Se muestra una tarea completada en el filtro Pendientes"

    driver.find_element(By.ID, "filter-all").click()
    time.sleep(0.3)
    print("CP-06 PASS: Filtro de tareas pendientes funciona correctamente")


# ─── CP-04: Eliminar tarea – cancelar confirmación ───────────────────────────
def test_CP04_eliminar_cancelar(driver):
    """CP-04 | US-04: Cancelar la eliminación de una tarea."""
    items_before = driver.find_elements(By.CLASS_NAME, "task-item")
    count_before = len(items_before)

    items_before[0].find_element(By.CLASS_NAME, "btn-delete").click()
    time.sleep(0.3)

    alert = Alert(driver)
    alert.dismiss()  # Cancelar
    time.sleep(0.3)

    items_after = driver.find_elements(By.CLASS_NAME, "task-item")
    assert len(items_after) == count_before, "La tarea fue eliminada a pesar de cancelar"
    print("CP-04a PASS: Cancelar eliminación funciona correctamente")


# ─── CP-04b: Eliminar tarea – confirmar ──────────────────────────────────────
def test_CP04b_eliminar_confirmar(driver):
    """CP-04b | US-04: Confirmar la eliminación de una tarea."""
    items_before = driver.find_elements(By.CLASS_NAME, "task-item")
    count_before = len(items_before)

    items_before[0].find_element(By.CLASS_NAME, "btn-delete").click()
    time.sleep(0.3)

    alert = Alert(driver)
    alert.accept()  # Confirmar
    time.sleep(0.5)

    items_after = driver.find_elements(By.CLASS_NAME, "task-item")
    assert len(items_after) == count_before - 1, "La tarea no fue eliminada"
    print("CP-04b PASS: Tarea eliminada correctamente")


# ─── CP-07: Persistencia con LocalStorage ─────────────────────────────────────
def test_CP07_persistencia_localStorage(driver):
    """CP-07 | US-09: Los datos persisten al recargar la página."""
    items_before = driver.find_elements(By.CLASS_NAME, "task-item")
    count_before = len(items_before)

    driver.refresh()
    time.sleep(1)

    items_after = driver.find_elements(By.CLASS_NAME, "task-item")
    assert len(items_after) == count_before, \
        f"Se perdieron tareas al recargar: antes={count_before}, después={len(items_after)}"
    print("CP-07 PASS: Datos persisten correctamente en LocalStorage")
