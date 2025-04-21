from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.app import App

class TeacherDashboardScreen(Screen):
    def __init__(self, **kwargs):
        # Initialize the teacher dashboard
        super(TeacherDashboardScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=[20, 20])
        # Title
        self.title_label = Label(text="",font_size=30,bold=True,size_hint_y=None,height=dp(100))
        self.layout.add_widget(self.title_label)
        # Progress Analytics button
        self.progress_btn = Button(text="Class Analytics",size_hint_y=None,height=dp(100))
        self.progress_btn.bind(on_press=self.view_progress)
        self.layout.add_widget(self.progress_btn)
        # Class Statistics button
        self.stats_btn = Button(
            text="Class Statistics",size_hint_y=None,height=dp(100))
        self.stats_btn.bind(on_press=self.view_stats)
        self.layout.add_widget(self.stats_btn)
        # Add feedback button
        self.feedback_btn = Button(text="Student Feedback", size_hint_y=None, height=dp(100))
        self.feedback_btn.bind(on_press=self.view_feedback)
        self.layout.add_widget(self.feedback_btn)
        # Logout button
        self.logout_btn = Button(text="Logout",size_hint_y=None,height=dp(100),background_color=(1, 0, 0, 1))
        self.logout_btn.bind(on_press=self.logout)
        self.layout.add_widget(self.logout_btn)
        self.add_widget(self.layout)

    def view_feedback(self, instance):
            self.manager.current = 'feedback'

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        self.title_label.text = f"Teacher Dashboard - {app.current_user}"

    def view_progress(self, instance):
        self.manager.current = 'class_analytics'

    def view_stats(self, instance):
        self.manager.current = 'class_stats'

    def logout(self, instance):
        app = App.get_running_app()
        app.current_user = None
        self.manager.current = 'login'