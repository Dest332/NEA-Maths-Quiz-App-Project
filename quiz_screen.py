from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from adaptive_quiz import AdaptiveQuiz
from functions import update_student_results, calculate_score

class QuizScreen(Screen):
    def __init__(self, **kwargs):
        super(QuizScreen, self).__init__(**kwargs)
        # Initialize AdaptiveQuiz instance
        self.adaptive_quiz = AdaptiveQuiz(json_file=r"C:\Users\chazz\PycharmProjects\PythonProject2\quiz.json")
        # Main layout
        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=40)
        # Title label
        self.title_label = Label(text="", font_size=32, bold=True,  size_hint_y=None, height=60)
        self.layout.add_widget(self.title_label)
        # Question label
        self.question_label = Label(
            text="", font_size=28, size_hint_y=None, height=120,  halign='center', valign='middle')
        self.layout.add_widget(self.question_label)
        # Options container
        options_layout = BoxLayout(
            orientation='vertical', spacing=15, size_hint_y=0.7)
        self.option_buttons = []
        for i in range(4):
            btn = Button(text="", font_size=24, size_hint_y=None, height=80, background_color=(0.2, 0.2, 0.2, 1),
                color=(1, 1, 1, 1),background_normal="")
            btn.bind(on_press=self.check_answer)
            self.option_buttons.append(btn)
            options_layout.add_widget(btn)
        self.layout.add_widget(options_layout)
        # Back button
        back_button = Button(
            text="Back to Topics",font_size=24,size_hint_y=None,height=60, background_color=(0.8, 0, 0, 1),  # Red
            color=(1, 1, 1, 1)
        )
        back_button.bind(on_press=self.go_back)
        self.layout.add_widget(back_button)
        self.add_widget(self.layout)
        # Quiz variables
        self.current_question = None
        self.level_scores = {1: {"correct": 0, "total": 0}, 2: {"correct": 0, "total": 0}, 3: {"correct": 0, "total": 0}}
        self.topic = None
        self.start_time = None

    def start_quiz(self, topic):
        """Initialize quiz and reset variables"""
        self.topic = topic
        self.adaptive_quiz.reset_quiz()  # Reset quiz state here
        self.level_scores = {1: {"correct": 0, "total": 0}, 2: {"correct": 0, "total": 0}, 3: {"correct": 0, "total": 0}}
        self.show_question()

    def save_results(self):
        # Only save results if the user has answered at least one question
        if any(level["total"] > 0 for level in self.level_scores.values()):
            # Convert raw scores to percentages
            percentages = {
                level: calculate_score(data["correct"], data["total"])
                for level, data in self.level_scores.items()
            }
            quiz_data = {
                "topic": self.topic,
                "level_scores": percentages,  # Store percentages
            }
            update_student_results(App.get_running_app().current_user, quiz_data)
        else:
            print("No results to save")

    def show_question(self):
        """Fetch and display a question"""
        if not self.topic:
            raise ValueError("Topic must be set before starting the quiz.")

        self.current_question = self.adaptive_quiz.get_question(self.topic)
        print(f"DEBUG: Current question fetched: {self.current_question}")

        if self.current_question:
            # Update UI for current question
            self.title_label.text = f"{self.topic} - Level {self.adaptive_quiz.current_level}"
            self.question_label.text = self.current_question["question"]
            # Set options to buttons
            for i, option in enumerate(self.current_question["options"]):
                self.option_buttons[i].text = option
                self.option_buttons[i].background_color = (0.2, 0.2, 0.2, 1)
                self.option_buttons[i].disabled = False
            for i in range(len(self.current_question["options"]), len(self.option_buttons)):
                self.option_buttons[i].text = ""
                self.option_buttons[i].disabled = True
        else:
            # No more questions available
            print("No more questions available for the current level.")
            self.title_label.text = "Quiz Completed!"
            self.question_label.text = f"Final Scores: {self.level_scores}"
            for btn in self.option_buttons:
                btn.text = ""
                btn.disabled = True

            self.save_results()
            self.show_completion_popup()

    def check_answer(self, instance):
        """Check if the selected answer is correct"""
        correct_answer = self.current_question["answer"]
        # Highlight buttons
        for btn in self.option_buttons:
            btn.background_color = (0.2, 0.2, 0.2, 1)  # Reset color
        instance.background_color = (0, 0.7, 0, 1) if instance.text == correct_answer else (0.8, 0, 0, 1)
        # Record performance
        correct = instance.text == correct_answer
        level_data = self.level_scores[self.adaptive_quiz.current_level]
        level_data["correct"] += int(correct)
        level_data["total"] += 1
        self.adaptive_quiz.record_performance(correct)
        # Load next question
        Clock.schedule_once(self.next_question, 1.0)

    def next_question(self, dt):
        self.show_question()

    def show_completion_popup(self):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text=f"Quiz Completed!\nScores: {self.level_scores}", font_size=24, halign='center'))
        close_btn = Button(text="OK", size_hint_y=None, height=50)
        content.add_widget(close_btn)
        popup = Popup(title="Quiz Results", content=content, size_hint=(0.8, 0.5))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def go_back(self, instance):
        self.manager.current = "quiz_topics"