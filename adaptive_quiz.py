from random import choice
from functions import load_data

class AdaptiveQuiz:
    def __init__(self, json_file="PythonProject2/quiz.json"):
        # Initialize the quiz settings
        self.json_file = json_file
        self.question_bank = self.load_questions()
        self.current_level = 1
        self.correct_in_level = 0
        self.incorrect_in_level = 0
        self.total_questions_asked = 0
        self.max_questions = 10
        self.levels = [1, 2, 3]

        # Track progress for each level
        self.progress = {
            1: {"answered": 0, "correct": 0},
            2: {"answered": 0, "correct": 0},
            3: {"answered": 0, "correct": 0},
        }
    def load_questions(self):
        # Loads the questions from the file
        questions = load_data(self.json_file)
        if "topics" not in questions:
            print("Error: No topics found!")
            return {}
        else:
            return questions["topics"]

    def get_questions_for_level(self, topic, level):
        # Gets questions for a level
        questions = self.question_bank.get(topic, {}).get(f"Level {level}", [])
        return questions

    def get_question(self, topic):
        # Fetch a random question
        if self.total_questions_asked >= self.max_questions:
            return None
        questions = self.get_questions_for_level(topic, self.current_level)
        if len(questions) == 0:
            return None
        return choice(questions)

    def record_performance(self, correct):
        # Records if the answer was correct
        self.total_questions_asked += 1
        self.progress[self.current_level]["answered"] += 1

        if correct:
            self.correct_in_level += 1
            self.progress[self.current_level]["correct"] += 1
        else:
            self.incorrect_in_level += 1

        if self.correct_in_level == 2:
            self.increase_level()
        elif self.incorrect_in_level == 2:
            self.decrease_level()

    def increase_level(self):
        # Move up a level
        if self.current_level < 3:
            self.current_level += 1
        self.reset_level_progress()

    def decrease_level(self):
        # Move down a level
        if self.current_level > 1:
            self.current_level -= 1
        self.reset_level_progress()

    def reset_level_progress(self):
        # Resets progress for the current level
        self.correct_in_level = 0
        self.incorrect_in_level = 0

    def calculate_progress(self):
        # Calculates progress for each level
        progress = {}
        for level in self.levels:
            if self.progress[level]["answered"] > 0:
                correct = self.progress[level]["correct"]
                answered = self.progress[level]["answered"]
                progress[level] = (correct / answered) * 100
            else:
                progress[level] = 0
        return progress

    def reset_quiz(self):
        # Reset everything for a new quiz
        self.__init__(self.json_file)
        print("Quiz reset complete.")