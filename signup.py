from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.metrics import dp
import json
import os
from kivy.app import App

class SignupScreen(Screen):
    def __init__(self, **kwargs):
        # Initialize the signup screen
        super(SignupScreen, self).__init__(**kwargs)
        self.create_layout()

    def create_layout(self):
        # Create the signup layout
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=[50, 50], spacing=20)
        # Title
        layout.add_widget(Label(text="Create New Account", font_size=30, bold=True))
        # Username field
        self.username = TextInput(hint_text="Username", multiline=False, size_hint_y=None, height=dp(50))
        layout.add_widget(self.username)
        # Password field
        self.password = TextInput(hint_text="Password", password=True, multiline=False, size_hint_y=None, height=dp(50))
        layout.add_widget(self.password)
        # Confirm password field
        self.confirm_password = TextInput(hint_text="Confirm Password", password=True, multiline=False,
                                          size_hint_y=None, height=dp(50))
        layout.add_widget(self.confirm_password)
        # Role selection
        role_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=dp(50))
        role_layout.add_widget(Label(text="Account Type:"))
        self.role_student = ToggleButton(text='Student', group='role', state='down')
        self.role_teacher = ToggleButton(text='Teacher', group='role')
        role_layout.add_widget(self.role_student)
        role_layout.add_widget(self.role_teacher)
        layout.add_widget(role_layout)
        # Signup button
        signup_btn = Button(text="Create Account", size_hint_y=None, height=dp(50))
        signup_btn.bind(on_press=self.attempt_signup)
        layout.add_widget(signup_btn)
        # Login link
        login_btn = Button(text="Already have an account? Login", size_hint_y=None, height=dp(40))
        login_btn.bind(on_press=self.go_to_login)
        layout.add_widget(login_btn)

        self.add_widget(layout)

    def attempt_signup(self, instance):
        # Attempt to create a new account
        username = self.username.text.strip()
        password = self.password.text.strip()
        confirm_password = self.confirm_password.text.strip()
        is_teacher = self.role_teacher.state == 'down'

        if not username or not password:
            self.show_error("Please enter both username and password")
            return

        if password != confirm_password:
            self.show_error("Passwords don't match")
            return

        if len(password) < 6:
            self.show_error("Password must be at least 6 characters")
            return

        # Check if username exists
        user_data = self.load_user_data()

        if username in user_data:
            self.show_error("Username already exists")
            return

        # Save new user
        user_data[username] = {
            'password': password,
            'is_teacher': is_teacher
        }
        self.save_user_data(user_data)
        self.show_success("Account created successfully!")

        # Auto-login
        app = App.get_running_app()
        app.current_user = username
        app.is_teacher = is_teacher

        if is_teacher:
            self.manager.current = 'teacher_dashboard'
        else:
            self.manager.current = 'student_dashboard'

    def load_user_data(self):
        if os.path.exists('users.json'):
            with open('users.json', 'r') as f:
                return json.load(f)
        return {}

    def save_user_data(self, data):
        with open('users.json', 'w') as f:
            json.dump(data, f)

    def show_error(self, message):
        # Show an error message in a popup
        content = BoxLayout(orientation='vertical', spacing=10)
        content.add_widget(Label(text=message))
        popup = Popup(title='Signup Error', content=content, size_hint=(0.7, 0.3))
        ok_btn = Button(text='OK', size_hint_y=None, height=dp(40))
        content.add_widget(ok_btn)
        ok_btn.bind(on_press=popup.dismiss)
        popup.open()

    def show_success(self, message):
        content = BoxLayout(orientation='vertical', spacing=10)
        content.add_widget(Label(text=message))
        popup = Popup(title='Success', content=content, size_hint=(0.7, 0.3))
        ok_btn = Button(text='OK', size_hint_y=None, height=dp(40))
        content.add_widget(ok_btn)
        ok_btn.bind(on_press=popup.dismiss)
        popup.open()

    def go_to_login(self, instance):
        self.manager.current = 'login'