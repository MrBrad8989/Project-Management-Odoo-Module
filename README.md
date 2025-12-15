# 📂 Módulo: Sistema de Gestión de Proyectos

Este módulo para Odoo ofrece una solución integral para la planificación, ejecución y seguimiento de proyectos. Su estructura jerárquica permite dividir grandes objetivos en unidades de trabajo manejables y tareas específicas, garantizando el control de tiempos, responsables y el progreso automático.

---

## 🏗️ Estructura del Sistema

El sistema se organiza en tres niveles jerárquicos para un control granular:

1.  **🏆 Proyectos (`project.proyecto`)**: El nivel superior que define el objetivo global.
2.  **📋 Trabajos (`project.trabajo`)**: Divisiones funcionales o fases del proyecto.
3.  **✅ Actividades (`project.actividad`)**: Tareas unitarias asignadas a usuarios específicos.

---

## 🚀 Funcionalidades Principales

### 1. Gestión de Proyectos
Es el contenedor principal. Define el alcance temporal y el equipo responsable.

* **Estados del Ciclo de Vida**:
    * ⚪ *Borrador*
    * 🔵 *En Planificación*
    * 🟣 *En Ejecución*
    * 🟢 *Finalizado*
    * ⚫ *Cancelado*
* **Cálculo de Avance Automático**: El porcentaje de "Avance (%)" se calcula automáticamente promediando el progreso de todos sus **Trabajos** asociados.
* **Validaciones de Seguridad**:
    * **Fechas**: Impide guardar si la *Fecha de Finalización* es anterior a la *Fecha de Inicio*.
    * **Borrado Seguro**: No se puede eliminar un proyecto que ya tiene trabajos asociados (salvo que esté en estado "Borrador") para asegurar la integridad de los datos.

### 2. Gestión de Trabajos (Fases)
Representa un bloque de trabajo dentro del proyecto principal.

* **Priorización**: Clasificación visual de la urgencia de las actividades (⭐ Baja, Media, Alta, Urgente).
* **Cálculo de Avance**: Su progreso es el promedio del avance de sus **Actividades** hijas.
* **Automatización de Cierre**: Si todas las actividades de un trabajo se marcan como "Finalizadas", el Trabajo puede actualizar su estado a finalizado automáticamente.

### 3. Gestión de Actividades (Tareas)
La unidad mínima de gestión para el trabajo diario.

* **Planificación Visual**: Incluye una vista de **Calendario** para visualizar las entregas (*Fin planificado*) por usuario.
* **Detalle**: Campo de texto libre para describir extensamente la tarea.
* **Estados de Tarea**: Pendiente, En Curso, En Revisión, Finalizada, Cancelada.

---

## 🔒 Reglas de Negocio y Restricciones
El sistema incorpora "candados" lógicos para asegurar el flujo correcto de trabajo:

### 🛡️ Integridad del Proyecto
* **Proyecto Finalizado (Modo Solo Lectura)**:
    * No se pueden crear nuevos **Trabajos** si el Proyecto padre está *Finalizado*.
    * No se pueden añadir nuevas **Actividades** si el Proyecto padre está *Finalizado*.
    * No se pueden modificar **Trabajos** existentes si el Proyecto está *Finalizado*.

### 🛡️ Integridad del Trabajo
* **Bloqueo por Revisión/Finalización**:
    * No se pueden editar **Trabajos** que estén en estado *En revisión* o *Finalizado* (se debe cambiar el estado a "En progreso" primero).
    * No se pueden crear ni modificar **Actividades** si su Trabajo padre está en *Revisión* o *Finalizado*.
* **Cierre en Cascada**: Al finalizar un Trabajo manualmente, el sistema busca actividades abiertas y las cierra automáticamente.

---

## 💻 Aspectos Técnicos

* **Nombre Técnico**: `project_management`
* **Dependencias**: `base`
* **Menú Principal**: Gestión Proyectos
    * *Submenús:* Operaciones -> Proyectos / Trabajos / Actividades
* **Vistas Incluidas**:
    * Listas (Tree)
    * Formularios (Form)
    * Calendario (para Actividades)
    * Búsqueda y Filtros avanzados
