from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.popup import Popup
import json

class FeedbackScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Main layout
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.add_widget(self.layout)
        # Title
        self.title_label = Label(text="Feedback and Questions", font_size=24, size_hint_y=None, height=50)
        self.layout.add_widget(self.title_label)
        # Feedback list container
        self.feedback_list = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.feedback_list.bind(minimum_height=self.feedback_list.setter('height'))
        self.layout.add_widget(self.feedback_list)
        # Input for students
        self.input_container = BoxLayout(size_hint_y=None, height=150, spacing=10)
        self.message_input = TextInput(hint_text="Enter your question or feedback...", multiline=True)
        self.send_button = Button(text="Send", size_hint_x=0.3, font_size=18, height=60, background_color=(0.2, 0.6, 0.8, 1))
        self.send_button.bind(on_press=self.send_feedback)
        self.input_container.add_widget(self.message_input)
        self.input_container.add_widget(self.send_button)
        self.layout.add_widget(self.input_container)
        # Logout button
        self.logout_button = Button(
            text="Back to Dashboard", size_hint_y=None, height=60, font_size=18, background_color=(1, 0, 0, 1))
        self.logout_button.bind(on_press=self.go_back_to_dashboard)
        self.layout.add_widget(self.logout_button)

    def on_pre_enter(self):
        # Load feedback when entering the screen
        self.load_feedback()
        # Show or hide the input for students based on user role
        app = App.get_running_app()
        if app.is_teacher:
            self.input_container.opacity = 0
            self.input_container.size_hint_y = 0
        else:
            self.input_container.opacity = 1
            self.input_container.size_hint_y = None

    def load_feedback(self):
        # Load feedback data
        try:
            with open('feedback.json', 'r') as file:
                feedback_data = json.load(file).get("feedback", [])
        except FileNotFoundError:
            feedback_data = []
        # Clear the feedback list
        self.feedback_list.clear_widgets()
        # Add feedback items to the list
        app = App.get_running_app()

        for feedback in feedback_data:
            if app.is_teacher or feedback['from'] == app.current_user:
                feedback_box = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=150)
                feedback_box.add_widget(Label(text=f"From: {feedback['from']}", size_hint_y=None, height=30))
                feedback_box.add_widget(Label(text=f"Message: {feedback['message']}", size_hint_y=None, height=50))

                if feedback.get("response"):
                    feedback_box.add_widget(Label(text=f"Response: {feedback['response']}", size_hint_y=None, height=40))

                if app.is_teacher and not feedback.get("response"):
                    response_input = TextInput(hint_text="Write a response...", size_hint_y=None, height=50)
                    send_response_btn = Button(
                        text="Respond", size_hint_y=None, height=50, font_size=16, background_color=(0.2, 0.8, 0.2, 1)
                    )
                    send_response_btn.bind(
                        on_press=lambda instance, f=feedback, r=response_input: self.respond_to_feedback(f, r)
                    )
                    feedback_box.add_widget(response_input)
                    feedback_box.add_widget(send_response_btn)

                self.feedback_list.add_widget(feedback_box)

    def send_feedback(self, instance):
        # Send feedback (for students)
        feedback_message = self.message_input.text.strip()
        if feedback_message == "":
            self.show_popup("Error", "Feedback message cannot be empty.")
            return None

        try:
            with open('feedback.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {"feedback": []}

        feedback_list = data.get('feedback', [])
        feedback_list.append({
            "from": App.get_running_app().current_user,
            "to": "Teacher",
            "message": feedback_message,
            "response": "",
            "status": "pending"
        })
        data['feedback'] = feedback_list

        with open('feedback.json', 'w') as file:
            json.dump(data, file)

        self.message_input.text = ""
        self.show_popup("Success", "Your feedback has been sent.")
        self.load_feedback()

    def respond_to_feedback(self, feedback, response_input):
        # Respond to feedback (for teachers)
        response_message = response_input.text.strip()
        if response_message == "":
            self.show_popup("Error", "Response cannot be empty.")
            return

        try:
            with open('feedback.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            self.show_popup("Error", "No feedback data found.")
            return

        for fb in data["feedback"]:
            if fb["message"] == feedback["message"]:
                fb["response"] = response_message
                fb["status"] = "resolved"
                break

        with open('feedback.json', 'w') as file:
            json.dump(data, file)

        self.show_popup("Success", "Response has been sent.")
        self.load_feedback()

    def go_back_to_dashboard(self, instance):
        app = App.get_running_app()
        if app.is_teacher:
            self.manager.current = 'teacher_dashboard'
        else:
            self.manager.current = 'student_dashboard'

    def show_popup(self, title, message):
        popup_content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        popup_content.add_widget(Label(text=message))
        close_btn = Button(text="Close", size_hint_y=None, height=40)
        popup_content.add_widget(close_btn)
        popup = Popup(title=title, content=popup_content, size_hint=(0.8, 0.4))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()