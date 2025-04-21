from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

class QuizTopicsScreen(Screen):
    def __init__(self, **kwargs):
        super(QuizTopicsScreen, self).__init__(**kwargs)
        # Main layout for the screen
        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=[50, 50])
        # Title label
        self.title_label = Label(text="Choose Topic", font_size=40, bold=True)
        self.layout.add_widget(self.title_label)
        # Differentiation topic button
        self.diff_button = Button(text="Differentiation")
        self.diff_button.bind(on_press=lambda x: self.go_to_quiz_screen("Differentiation"))
        self.layout.add_widget(self.diff_button)
        # Integration topic button
        self.int_button = Button(text="Integration")
        self.int_button.bind(on_press=lambda x: self.go_to_quiz_screen("Integration"))
        self.layout.add_widget(self.int_button)
        # Back button to return to the dashboard
        self.back_button = Button(text="Back", background_color=(1, 0, 0, 1))  # Red
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_button)
        self.add_widget(self.layout)

    def go_to_quiz_screen(self, topic):
        quiz_screen_screen = self.manager.get_screen('quiz_screen')
        quiz_screen_screen.start_quiz(topic)
        self.manager.current = 'quiz_screen'

    def go_back(self, instance):
        app = App.get_running_app()
        self.manager.current = 'student_dashboard'