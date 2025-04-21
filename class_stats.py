from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy_garden.matplotlib import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from functions import load_student_data

def calculate_percentage(correct, total):
    if total == 0:
        return 0
    return (correct / total) * 100

class ClassStatsScreen(Screen):
    def __init__(self, **kwargs):
        # Initialize the progress analytics screen
        super(ClassStatsScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=[20, 20])
        # Title
        self.title_label = Label(
            text="Class Statistics",font_size=30,bold=True,size_hint_y=None,height=dp(50))
        self.layout.add_widget(self.title_label)
        # Grade Legend
        legend_layout = BoxLayout(size_hint_y=None, height=dp(30))
        grade_info = [("A* (85%+)", "00aa00"),
                      ("A (70-84%)", "55cc55"),
                      ("B (60-69%)", "ffff00"),
                      ("C (50-59%)", "ffaa00"),
                      ("D (40-49%)", "ff5500"),
                      ("F (<40%)", "ff0000")]

        for text, color in grade_info:
            legend_layout.add_widget(Label(text=f"[color={color}]■[/color] {text}",markup=True,halign='center'))
        self.layout.add_widget(legend_layout)
        # Graph container
        self.graph_container = BoxLayout(size_hint=(1, 0.8))
        self.layout.add_widget(self.graph_container)
        # Back button
        self.back_btn = Button(text="Back to Dashboard",size_hint_y=None,height=dp(50),  background_color=(1, 0, 0, 1))
        self.back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_btn)

        self.add_widget(self.layout)

    def on_pre_enter(self, *args):
        # Show the progress graph when entering
        self.show_student_progress()

    def show_student_progress(self):
        # Display student progress in a graph
        students = load_student_data()

        if not students:
            self.graph_container.clear_widgets()
            self.graph_container.add_widget(Label(
                text="No student data available", font_size=20, color=(1, 0, 0, 1)))
            return None

        plt.close('all')
        fig, ax = plt.subplots(figsize=(12, 6))
        # Prepare data
        usernames = []
        averages = []
        grade_colors = []
        # Loop through all students
        for student in sorted(students, key=lambda x: x['username']):
            scores = []
            for topic, levels in student.get('scores', {}).items():
                for level, data in levels.items():
                    if isinstance(data, int):
                        scores.append(data)
            if len(scores) > 0:
                avg = sum(scores) / len(scores)
            else:
                avg = 0
            usernames.append(student['username'])
            averages.append(avg)
            # Assign colors based on the grade
            if avg >= 85:
                grade_colors.append('#00aa00')  # A*
            elif avg >= 70:
                grade_colors.append('#55cc55')  # A
            elif avg >= 60:
                grade_colors.append('#ffff00')  # B
            elif avg >= 50:
                grade_colors.append('#ffaa00')  # C
            elif avg >= 40:
                grade_colors.append('#ff5500')  # D
            else:
                grade_colors.append('#ff0000')  # F

        # Create bar chart
        bars = ax.bar(usernames, averages, color=grade_colors)

        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    f'{height:.1f}%',
                    ha='center', va='bottom')

        ax.set_title("Student Performance with Grade Boundaries")
        ax.set_xlabel("Students")
        ax.set_ylabel("Average Score (%)")
        ax.set_yticks(range(0, 101, 10))
        ax.set_ylim(0, 100)
        ax.grid(True, axis='y', linestyle='--', alpha=0.7)
        plt.xticks(rotation=45)
        plt.tight_layout()
        # Display the graph
        self.graph_container.clear_widgets()
        self.graph_container.add_widget(FigureCanvasKivyAgg(fig))

    def go_back(self, instance):
        # Go back to the dashboard
        self.manager.current = 'teacher_dashboard'