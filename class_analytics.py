from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.matplotlib import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from functions import load_student_data
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.button import Button

def calculate_percentage(correct, total):
    if total == 0:
        return 0
    return (correct / total) * 100

class ClasAnalyticsScreen(Screen):
    def __init__(self, **kwargs):
        # Initialize the class stats screen
        super(ClasAnalyticsScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=[20, 20])
        # Title
        self.title_label = Label(
            text="Class Analytics", font_size=30, bold=True, size_hint_y=None, height=dp(50))
        self.layout.add_widget(self.title_label)
        # Graph container
        self.graph_container = BoxLayout(size_hint=(1, 0.8))
        self.layout.add_widget(self.graph_container)
        # Back button
        self.back_btn = Button(
            text="Back to Dashboard", size_hint_y=None, height=dp(50), background_color=(1, 0, 0, 1))
        self.back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_btn)
        self.add_widget(self.layout)

    def on_pre_enter(self, *args):
        # Show class stats when entering the screen
        self.show_class_stats()

    def show_class_stats(self):
        # Display class stats in a graph
        students = load_student_data()

        if not students:
            self.graph_container.clear_widgets()
            self.graph_container.add_widget(Label(
                text="No student data available", font_size=20, color=(1, 0, 0, 1)))
            return None

        plt.close('all')
        fig, ax = plt.subplots(figsize=(16, 8))

        # Prepare data
        topics_levels = set()
        student_performance = {}
        topic_level_avg_scores = {}

        for student in students:
            username = student["username"]
            student_performance[username] = {}

            for topic, levels in student.get("scores", {}).items():
                for level in ["Level 1", "Level 2", "Level 3"]:
                    topic_level = f"{topic} - {level}"
                    topics_levels.add(topic_level)

                    score = levels.get(level, 0)
                    student_performance[username][topic_level] = score
                    # Add to average calculation
                    if topic_level not in topic_level_avg_scores:
                        topic_level_avg_scores[topic_level] = []
                    topic_level_avg_scores[topic_level].append(score)

        # Calculate class average per topic-level
        class_avg = {topic_level: sum(scores) / len(scores) for topic_level, scores in topic_level_avg_scores.items()}

        topics_levels = sorted(topics_levels)
        usernames = sorted(student_performance.keys())

        # Plot each student's performance
        for username in usernames:
            scores = [student_performance[username].get(topic_level, 0) for topic_level in topics_levels]
            ax.plot(topics_levels, scores, label=username, marker='o', alpha=0.7)
        # Plot class average
        avg_scores = [class_avg.get(topic_level, 0) for topic_level in topics_levels]
        ax.plot(topics_levels, avg_scores, label='Class Average', color='black', linestyle='--', linewidth=2)

        ax.set_title("Class Performance by Topic and Level")
        ax.set_xlabel("Topics and Levels")
        ax.set_ylabel("Average Percentage (%)")
        ax.set_ylim(-5, 105)
        ax.set_xticks(range(len(topics_levels)))
        ax.set_xticklabels(topics_levels, rotation=45, ha="right")
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, linestyle='--', alpha=0.3)

        plt.tight_layout()
        # Display the graph
        self.graph_container.clear_widgets()
        graph_widget = FigureCanvasKivyAgg(fig)
        self.graph_container.add_widget(graph_widget)

    def go_back(self, instance):
        # Go back to the dashboard
        self.manager.current = 'teacher_dashboard'