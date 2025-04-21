from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.app import App

class StudentDashboardScreen(Screen):
    def __init__(self, **kwargs):
        # Initialize the student dashboard
        super(StudentDashboardScreen, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.create_layout()

    def create_layout(self):
        # Create the layout for the dashboard
        self.clear_widgets()
        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=[50, 50])
        # Title
        self.title_label = Label(
            text=f"Welcome back, {self.app.current_user}!", font_size=30, bold=True, color=(1, 1, 1, 1))
        self.layout.add_widget(self.title_label)
        # Quiz button
        self.quiz_button = Button(text="Start Quiz",size_hint_y=None,height=dp(100),background_color=(0.8, 0.8, 0.8, 1),
            color=(1, 1, 1, 1))
        self.quiz_button.bind(on_press=self.go_to_quiz_topics)
        self.layout.add_widget(self.quiz_button)
        # Progress button
        self.progress_button = Button(text="View My Progress",size_hint_y=None, height=dp(100),
                                    background_color=(0.8, 0.8, 0.8, 1),color=(1, 1, 1, 1))
        self.progress_button.bind(on_press=self.go_to_progress)
        self.layout.add_widget(self.progress_button)
        # Add feedback button
        self.feedback_button = Button(text="Ask for Help",size_hint_y=None,height=dp(100),
                                      background_color=(0.8, 0.8, 0.8, 1),color=(1, 1, 1, 1))
        self.feedback_button.bind(on_press=self.go_to_feedback)
        self.layout.add_widget(self.feedback_button)
        # Logout button
        self.logout_button = Button(text="Logout",size_hint_y=None,height=dp(100),background_color=(1, 0, 0, 1))
        self.logout_button.bind(on_press=self.logout)
        self.layout.add_widget(self.logout_button)

        self.add_widget(self.layout)

    def go_to_feedback(self, instance):
            self.manager.current = 'feedback'

    def go_to_quiz_topics(self, instance):
        self.manager.current = 'quiz_topics'

    def go_to_progress(self, instance):
        self.manager.current = 'progress'

    def logout(self, instance):
        app = App.get_running_app()
        app.current_user = None
        self.manager.current = 'login'

    def on_enter(self):
        if hasattr(self, 'title_label'):
            self.title_label.text = f"Welcome back, {self.app.current_user}!"