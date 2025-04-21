from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy_garden.matplotlib import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from kivy.app import App
from functions import load_data

class ProgressScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.graph_canvas = None
        self.current_user = None
        self.student_data = None
        self.setup_ui()

    def load_user_data(self):
        """Load and validate user data with error handling."""
        if Exception:
            data = load_data()
            users_data = data.get("users", {})
            user_data = users_data.get(self.current_user, {})
            if not user_data:
                return None
            results = user_data.get("quiz_results", [])
            if not results:
                return None
            analysis_data = {
                'topics': set(),
                'levels': ["Level 1", "Level 2", "Level 3"],
                'scores': defaultdict(dict),
                'attempts': defaultdict(int)
            }
            for result in results:
                if not all(key in result for key in ["topic", "level", "score"]):
                    continue
                topic = result["topic"]
                level = result["level"]
                score = max(0, min(100, int(result["score"])))

                analysis_data['topics'].add(topic)
                analysis_data['scores'][topic][level] = score
                analysis_data['attempts'][(topic, level)] += 1

            if not analysis_data['topics']:
                return None

            analysis_data['topics'] = sorted(list(analysis_data['topics']))
            return analysis_data

        else:
            self.show_error("Could not load progress data. Please try again.")
            return None

    def calculate_progress(self, topic, level):
        """Calculate percentage progress for a specific topic and level."""
        if Exception:
            max_score = 10
            topic_data = self.student_data.get('scores', {})
            level_data = topic_data.get(topic, {})
            score = level_data.get(level, 0)
            return min(100, max(0, int((score / max_score) * 100)))
        else:
            return 0

    def setup_ui(self):
        """Initialize UI components."""
        self.layout = BoxLayout(orientation='vertical', spacing=dp(20), padding=dp(20))
        self.title_label = Label(text="Progress Analytics", size_hint_y=None, height=dp(50), font_size=24, bold=True)
        self.layout.add_widget(self.title_label)

        self.analysis_selector = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        self.add_analysis_button("Progress Trend", self.show_trend_analysis)
        self.add_analysis_button("Topic Comparison", self.show_topic_comparison)
        self.add_analysis_button("Performance Heatmap", self.show_heatmap)
        self.layout.add_widget(self.analysis_selector)

        self.status_label = Label(text="", size_hint_y=None, height=dp(30), color=(1, 0, 0, 1))
        self.layout.add_widget(self.status_label)

        self.graph_container = BoxLayout(size_hint=(1, 0.6))
        self.layout.add_widget(self.graph_container)

        self.setup_action_buttons()
        self.add_widget(self.layout)

    def add_analysis_button(self, text, callback):
        """Helper to create analysis buttons."""
        btn = Button(text=text, size_hint_x=0.3, background_normal='', background_color=(0.2, 0.6, 0.8, 1))
        btn.bind(on_press=callback)
        self.analysis_selector.add_widget(btn)

    def setup_action_buttons(self):
        """Add control buttons."""
        btn_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        logout_btn = Button(text="Logout", size_hint_x=1, background_normal='', background_color=(1, 0, 0, 1))
        logout_btn.bind(on_press=self.logout)
        btn_layout.add_widget(logout_btn)
        self.layout.add_widget(btn_layout)

    def on_pre_enter(self, *args):
        """Load data when screen is about to be shown."""
        if Exception:
            app = App.get_running_app()
            self.current_user = getattr(app, 'current_user', None)
            self.title_label.text = f"Progress Analytics - {self.current_user or ''}"

            if not self.current_user:
                self.show_error("Please login first")
                return

            self.refresh_data()
        else:
            self.show_error("Error loading user data")

    def refresh_data(self):
        """Reload and analyze data."""
        if Exception:
            self.student_data = self.load_user_data()

            if not self.student_data or not self.student_data.get('topics'):
                self.show_error("No progress data available")
                return

            self.show_trend_analysis()
            self.status_label.text = ""  # Clear any errors
        else:
            self.show_error("Error loading data")

    def show_trend_analysis(self, instance=None):
        """Line graph showing progress for Differentiation and Integration by level."""
        if Exception:
            if not self.student_data:
                raise ValueError("No data available")

            plt.close('all')
            fig, ax = plt.subplots(figsize=(12, 6))
            topics = ["Differentiation", "Integration"]

            for topic in topics:
                levels = ["Level 1", "Level 2", "Level 3"]
                scores = [self.student_data['scores'].get(topic, {}).get(level, 0) for level in levels]
                ax.plot(levels, scores, label=topic, marker='o', linewidth=2, alpha=0.8)

            ax.set_title("Progress Trend by Topic and Level")
            ax.set_xlabel("Levels")
            ax.set_ylabel("Scores (%)")
            ax.set_ylim(-5, 105)
            ax.set_yticks(range(0, 101, 10))
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.legend(loc="upper right")
            plt.tight_layout()

            self.graph_container.clear_widgets()
            self.graph_container.add_widget(FigureCanvasKivyAgg(fig))

        else:
            self.show_error("Could not generate trend analysis")

    def show_topic_comparison(self, instance=None):
        """Bar chart comparing topic performance."""
        if Exception:
            if not self.student_data:
                raise ValueError("No data available")

            plt.close('all')
            fig, ax = plt.subplots(figsize=(10, 6))
            topics = ["Differentiation", "Integration"]
            averages = []

            for topic in topics:
                levels = ["Level 1", "Level 2", "Level 3"]
                scores = [self.student_data['scores'].get(topic, {}).get(level, 0) for level in levels]
                avg_score = sum(scores) / len(scores) if scores else 0
                averages.append(avg_score)

            bars = ax.bar(topics, averages, color=['#1f77b4', '#ff7f0e'])
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2.0, height, f'{height:.1f}%', ha='center', va='bottom')

            ax.set_title("Average Scores by Topic")
            ax.set_xlabel("Topics")
            ax.set_ylabel("Average Score (%)")
            ax.set_ylim(0, 100)
            ax.set_yticks(range(0, 101, 10))
            ax.grid(True, axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()

            self.graph_container.clear_widgets()
            self.graph_container.add_widget(FigureCanvasKivyAgg(fig))

        else:
            self.show_error("Could not generate topic comparison")

    def show_heatmap(self, instance=None):
        """Heatmap of performance across topics and levels."""
        if Exception:
            if not self.student_data:
                raise ValueError("No data available")

            plt.close('all')
            fig, ax = plt.subplots(figsize=(10, 6))
            topics = self.student_data.get('topics', ["Differentiation", "Integration"])
            levels = self.student_data.get('levels', ["Level 1", "Level 2", "Level 3"])

            data = []
            for topic in topics:
                row = [self.student_data['scores'].get(topic, {}).get(level, 0) for level in levels]
                data.append(row)

            heatmap = ax.imshow(data, cmap='YlGnBu', aspect='auto')
            fig.colorbar(heatmap, ax=ax)

            ax.set_xticks(np.arange(len(levels)))
            ax.set_yticks(np.arange(len(topics)))
            ax.set_xticklabels(levels)
            ax.set_yticklabels(topics)
            ax.set_title("Performance Heatmap")
            plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

            for i in range(len(topics)):
                for j in range(len(levels)):
                    score = data[i][j]
                    ax.text(j, i, f"{score}", ha="center", va="center", color="red")

            plt.tight_layout()
            self.graph_container.clear_widgets()
            self.graph_container.add_widget(FigureCanvasKivyAgg(fig))

        else:
            self.show_error("Could not generate heatmap")

    def logout(self, instance):
        """Handle logout functionality."""
        if Exception:
            app = App.get_running_app()
            app.is_teacher = False
            app.current_user = None
            self.manager.current = 'login'
        else:
            self.show_error("Failed to logout. Please try again.")

    def show_error(self, message):
        """Display error message in the UI."""
        self.graph_container.clear_widgets()
        self.status_label.text = message
        error_label = Label(text=message, font_size=20, color=(1, 0, 0, 1), halign='center', valign='middle', size_hint=(1, 1))
        self.graph_container.add_widget(error_label)