from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.metrics import dp
import json
import os
from kivy.app import App

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.create_layout()

    def create_layout(self):
        # Create the login layout
        self.clear_widgets()
        self.layout = BoxLayout(orientation='vertical', padding=[50, 50], spacing=20)
        # Title
        self.layout.add_widget(Label(text="Welcome to Exponential", font_size=30, bold=True))
        # Username field
        self.username = TextInput(hint_text="Username", multiline=False, size_hint_y=None, height=dp(50))
        self.layout.add_widget(self.username)
        # Password field
        self.password = TextInput(hint_text="Password", password=True, multiline=False, size_hint_y=None, height=dp(50))
        self.layout.add_widget(self.password)
        # Login button
        login_btn = Button(text="Login", size_hint_y=None, height=dp(50))
        login_btn.bind(on_press=self.attempt_login)
        self.layout.add_widget(login_btn)
        # Signup link
        signup_btn = Button(text="Don't have an account? Sign up", size_hint_y=None, height=dp(40))
        signup_btn.bind(on_press=self.go_to_signup)
        self.layout.add_widget(signup_btn)
        # Exit button
        self.exit_button = Button(text="Exit", size_hint_y=None, height=dp(50), background_color=(1, 0, 0, 1))
        self.exit_button.bind(on_press=self.exit_app)
        self.layout.add_widget(self.exit_button)

        self.add_widget(self.layout)

    def attempt_login(self, instance):
        # Attempt to log in
        username = self.username.text.strip()
        password = self.password.text.strip()

        if not username or not password:
            self.show_error("Please enter both username and password")
            return

        user_data = self.load_user_data()

        if username in user_data:
            if user_data[username]['password'] == password:
                app = App.get_running_app()
                app.current_user = username
                app.is_teacher = user_data[username].get('is_teacher', False)

                # Navigate to the correct dashboard
                if app.is_teacher:
                    self.manager.current = 'teacher_dashboard'
                else:
                    self.manager.current = 'student_dashboard'
            else:
                self.show_error("Incorrect password")
        else:
            self.show_error("Username not found")

    def load_user_data(self):
        if os.path.exists('users.json'):
            with open('users.json', 'r') as f:
                return json.load(f)
        return {}

    def show_error(self, message):
        content = BoxLayout(orientation='vertical', spacing=10)
        content.add_widget(Label(text=message))
        popup = Popup(title='Login Error', content=content, size_hint=(0.7, 0.3))
        ok_btn = Button(text='OK', size_hint_y=None, height=dp(40))
        content.add_widget(ok_btn)
        ok_btn.bind(on_press=popup.dismiss)
        popup.open()

    def exit_app(self, instance):
        App.get_running_app().stop()

    def go_to_signup(self, instance):
        self.manager.current = 'signup'