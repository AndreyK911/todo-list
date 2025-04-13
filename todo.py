import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

# Подключение к базе данных SQLite
conn = sqlite3.connect('todo_list.db')
cursor = conn.cursor()

# Создание таблицы задач, если она еще не существует
cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_name TEXT,
    description TEXT,
    status TEXT,
    date_added TEXT
)
''')
conn.commit()

# Функция для добавления задачи
def add_task():
    task_name = task_name_entry.get()
    description = description_entry.get()
    if task_name and description:
        date_added = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
                       INSERT INTO tasks (task_name, description, status, date_added)
                       VALUES (?, ?, 'pending', ?)
                       ''', (task_name, description, date_added))
        conn.commit()
        task_name_entry.delete(0, tk.END)
        description_entry.delete(0, tk.END)
        view_tasks()
    else:
        messagebox.showwarning("Input Error", "Please fill in both task name and description")

# Функция для отображения задач
def view_tasks():
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    task_list.delete(0, tk.END)  # Очистить текущий список в Listbox
    if tasks:
        for task in tasks:
            # Отображение задачи с названием, статусом, описанием и датой
            task_list.insert(tk.END, f"Task: {task[1]}, Status: {task[3]}, Description: {task[2]}, Added: {task[4]}")
    else:
        task_list.insert(tk.END, "No tasks found.")

# Функция для обновления статуса задачи
def update_task_status():
    try:
        task_id = int(task_id_entry.get())
        new_status = status_entry.get()
        valid_statuses = ['pending', 'in-progress', 'complete']
        if new_status in valid_statuses:
            cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', (new_status, task_id))
            conn.commit()
            view_tasks()
        else:
            messagebox.showwarning("Invalid Status", "Please choose a valid status: pending, in-progress, complete")
    except ValueError:
        messagebox.showwarning("Input Error", "Please enter a valid task ID")

# Функция для удаления задачи
def delete_task():
    try:
        task_id = int(task_id_entry.get())
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        view_tasks()
    except ValueError:
        messagebox.showwarning("Input Error", "Please enter a valid task ID")

# Создание графического интерфейса
root = tk.Tk()
root.title("To-Do List")

# Виджеты для ввода данных
task_name_label = tk.Label(root, text="Task Name")
task_name_label.pack()
task_name_entry = tk.Entry(root)
task_name_entry.pack()

description_label = tk.Label(root, text="Description")
description_label.pack()
description_entry = tk.Entry(root)
description_entry.pack()

add_task_button = tk.Button(root, text="Add Task", command=add_task)
add_task_button.pack()

# Виджеты для управления задачами
task_id_label = tk.Label(root, text="Task ID (for update/delete)")
task_id_label.pack()
task_id_entry = tk.Entry(root)
task_id_entry.pack()

status_label = tk.Label(root, text="New Status (pending, in-progress, complete)")
status_label.pack()
status_entry = tk.Entry(root)
status_entry.pack()

update_status_button = tk.Button(root, text="Update Status", command=update_task_status)
update_status_button.pack()

delete_task_button = tk.Button(root, text="Delete Task", command=delete_task)
delete_task_button.pack()

# Виджет для отображения списка задач
task_list = tk.Listbox(root, width=50, height=10)
task_list.pack()

view_tasks_button = tk.Button(root, text="View Tasks", command=view_tasks)
view_tasks_button.pack()

# Запуск приложения
root.mainloop()

# Закрытие соединения с базой данных при выходе
conn.close()