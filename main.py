from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import OneLineAvatarIconListItem, IconRightWidget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.screenmanager import ScreenManager
import sqlite3

DB_NAME = "tasks.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT)")
    conn.commit()
    conn.close()

def add_task_db(text):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO tasks (title) VALUES (?)", (text,))
    conn.commit()
    conn.close()

def get_tasks_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, title FROM tasks")
    data = c.fetchall()
    conn.close()
    return data

def delete_task_db(task_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

class TasksScreen(MDScreen):
    def on_enter(self):
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=10)

        self.input = MDTextField(hint_text="Add new task")

        add_btn = MDRaisedButton(text="ADD TASK")
        add_btn.bind(on_release=self.add_task)

        self.task_list = MDBoxLayout(orientation='vertical', size_hint_y=None)
        self.task_list.bind(minimum_height=self.task_list.setter('height'))

        scroll = MDScrollView()
        scroll.add_widget(self.task_list)

        layout.add_widget(self.input)
        layout.add_widget(add_btn)
        layout.add_widget(scroll)

        self.add_widget(layout)
        self.refresh()

    def refresh(self):
        self.task_list.clear_widgets()
        for task_id, title in get_tasks_db():
            item = OneLineAvatarIconListItem(text=title)
            delete_icon = IconRightWidget(icon="delete")
            delete_icon.bind(on_release=lambda x, t=task_id: self.delete_task(t))
            item.add_widget(delete_icon)
            self.task_list.add_widget(item)

    def add_task(self, instance):
        text = self.input.text.strip()
        if text:
            add_task_db(text)
            self.input.text = ""
            self.refresh()

    def delete_task(self, task_id):
        delete_task_db(task_id)
        self.refresh()

class ClickFlowApp(MDApp):
    def build(self):
        self.title = "ClickFlow Pro Max"
        self.theme_cls.primary_palette = "Blue"
        init_db()
        sm = ScreenManager()
        sm.add_widget(TasksScreen(name="tasks"))
        return sm

ClickFlowApp().run()
