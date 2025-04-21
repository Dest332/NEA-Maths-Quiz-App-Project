from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.graphics import Color, Rectangle
from login import LoginScreen
from studentdashboard import StudentDashboardScreen
from teacherdashboard import TeacherDashboardScreen
from quiztopics import QuizTopicsScreen
from quiz_screen import QuizScreen
from progress import ProgressScreen
from signup import SignupScreen
from class_stats import ClassStatsScreen
from class_analytics import ClasAnalyticsScreen
from feedback import FeedbackScreen

class ExponentialScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(ExponentialScreenManager, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0., 0.7, 1, 1)  # Light blue background
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = self.size
        self.rect.pos = self.pos

class ExponentialApp(App):
    def __init__(self):
        super(ExponentialApp, self).__init__()
        self.current_user = None
        self.is_teacher = False
        self.quiz_results = {}

    def build(self):
        # Build the app screens
        sm = ExponentialScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(SignupScreen(name='signup'))
        sm.add_widget(StudentDashboardScreen(name='student_dashboard'))
        sm.add_widget(TeacherDashboardScreen(name='teacher_dashboard'))
        sm.add_widget(QuizTopicsScreen(name='quiz_topics'))
        sm.add_widget(QuizScreen(name='quiz_screen'))
        sm.add_widget(ProgressScreen(name='progress'))
        sm.add_widget(ClassStatsScreen(name='class_stats'))
        sm.add_widget(ClasAnalyticsScreen(name='class_analytics'),
        sm.add_widget(FeedbackScreen(name='feedback')))
        sm.current = 'login'  # Start with login screen
        return sm

    def set_user_role(self, is_teacher):
        self.root.current = 'teacher_dashboard' if is_teacher else 'student_dashboard'

    def logout(self):
        self.root.current = 'login'

if __name__ == "__main__":
    ExponentialApp().run()