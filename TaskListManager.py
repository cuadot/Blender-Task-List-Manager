bl_info = {
    "name": "Task list manager",
    "author": "cuadot.xyz",
    "version": (1, 1),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > Task List",
    "description": "A simple task list management tool integrated into Blender",
    "doc_url": "https://cuadot.notion.site/Doc-04dbace97df24ecd8445106875437feb",
    "category": "Productivity",
}

import bpy
from bpy.props import StringProperty, EnumProperty, CollectionProperty
from bpy.types import Panel, Operator, PropertyGroup
from datetime import datetime

# Estados de la tarea
# Task's states

TASK_STATES = [
    ('NONE', "Ninguno", ""),
    ('COMPLETED', "Completada", "")
]

# Clase para cada tarea
# Class for every task

class TaskItem(PropertyGroup):
    name: StringProperty(name="Task Name", default="Untitled Task")
    state: EnumProperty(name="State", items=TASK_STATES, default='NONE')
    creation_date: StringProperty(name="Creation Date")

# Operador para agregar tareas
# Add tasks Operator

class AddTask(Operator):
    bl_idname = "task_list.add_task"
    bl_label = "Add Task"
    bl_description = "Add a new task to the list"

    def execute(self, context):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        task = context.scene.task_list.add()
        task.name = "New Task"
        task.creation_date = current_time
        task.state = 'NONE'
        return {'FINISHED'}

# Operador para eliminar tareas
# Delete task operator 

class DeleteTask(Operator):
    bl_idname = "task_list.delete_task"
    bl_label = "Delete Task"
    bl_description = "Delete the selected task"
    task_index: bpy.props.IntProperty()

    def execute(self, context):
        task_list = context.scene.task_list
        task_list.remove(self.task_index)
        return {'FINISHED'}

# Operador para cambiar el estado de la tarea
# Change tasks states Operator

class ToggleTaskState(Operator):
    bl_idname = "task_list.toggle_task_state"
    bl_label = "Toggle Task State"
    bl_description = "Toggle the state of the task"
    task_index: bpy.props.IntProperty()

    def execute(self, context):
        task = context.scene.task_list[self.task_index]
        task.state = 'COMPLETED' if task.state == 'NONE' else 'NONE'
        return {'FINISHED'}

# Operador para mover una tarea hacia arriba en la lista
# Move up taks's Operator

class MoveTaskUp(Operator):
    bl_idname = "task_list.move_task_up"
    bl_label = "Move Task Up"
    bl_description = "Move the selected task up in the list"
    task_index: bpy.props.IntProperty()

    def execute(self, context):
        tasks = context.scene.task_list
        if self.task_index > 0:
            tasks.move(self.task_index, self.task_index - 1)
        return {'FINISHED'}

# Operador para mover una tarea hacia abajo en la lista
# Move down taks's Operator

class MoveTaskDown(Operator):
    bl_idname = "task_list.move_task_down"
    bl_label = "Move Task Down"
    bl_description = "Move the selected task down in the list"
    task_index: bpy.props.IntProperty()

    def execute(self, context):
        tasks = context.scene.task_list
        if self.task_index < len(tasks) - 1:
            tasks.move(self.task_index, self.task_index + 1)
        return {'FINISHED'}

# Panel para mostrar las tareas
# Show tasks panel 

class TaskListPanel(Panel):
    bl_label = "Task List"
    bl_idname = "TASK_LIST_PT_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Task List'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        
        
        # Botón para añadir tarea y botón para mostrar/ocultar fechas
	# add tasks, hide dates buttons

        row = layout.row(align=True)
        row.operator("task_list.add_task", text="Add Task")
        row.prop(scene, "show_creation_dates", icon='HIDE_OFF', text="")

        for index, task in enumerate(scene.task_list):
            box = layout.box()
            row = box.row()
            row.prop(task, "name", text="")

            if scene.show_creation_dates:
                row.label(text=f"Created: {task.creation_date}")
                
        # Botones eliminar, checkear y mover
	# Buttons delete, checkbox, move up down

            icon = 'CHECKMARK' if task.state == 'COMPLETED' else 'BLANK1'
            toggle = row.operator("task_list.toggle_task_state", text="", icon=icon)
            toggle.task_index = index

            move_up = row.operator("task_list.move_task_up", icon='TRIA_UP', text="")
            move_up.task_index = index
            move_down = row.operator("task_list.move_task_down", icon='TRIA_DOWN', text="")
            move_down.task_index = index

            row.operator("task_list.delete_task", icon='X', text="").task_index = index


# Registro de clases y propiedades
# classes and properties register

def register():
    bpy.types.Scene.show_creation_dates = bpy.props.BoolProperty(
        name="Show Creation Dates",
        description="Show or hide the creation dates of tasks",
        default=True
    )
    bpy.utils.register_class(TaskItem)
    bpy.utils.register_class(AddTask)
    bpy.utils.register_class(DeleteTask)
    bpy.utils.register_class(ToggleTaskState)
    bpy.utils.register_class(MoveTaskUp)
    bpy.utils.register_class(MoveTaskDown)
    bpy.utils.register_class(TaskListPanel)
    bpy.types.Scene.task_list = bpy.props.CollectionProperty(type=TaskItem)

def unregister():
    
    bpy.utils.unregister_class(TaskListPanel)
    bpy.utils.unregister_class(MoveTaskDown)
    bpy.utils.unregister_class(MoveTaskUp)
    bpy.utils.unregister_class(ToggleTaskState)
    bpy.utils.unregister_class(DeleteTask)
    bpy.utils.unregister_class(AddTask)
    bpy.utils.unregister_class(TaskItem)
    del bpy.types.Scene.task_list
    del bpy.types.Scene.show_creation_dates

if __name__ == "__main__":
    register()