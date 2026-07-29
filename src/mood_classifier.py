import re

class MoodClassifier:

    def __init__(self):

        self.mood_keywords = {

            "happy": [
                "happy",
                "joy",
                "great",
                "excited",
                "fun",
                "cheerful",
                "awesome",
                "smile"
            ],

            "sad": [
                "sad",
                "cry",
                "depressed",
                "heartbroken",
                "upset",
                "lonely"
            ],

            "romantic": [
                "love",
                "romantic",
                "date",
                "partner",
                "relationship"
            ],

            "motivated": [
                "motivation",
                "success",
                "goal",
                "winner",
                "career",
                "inspire"
            ],

            "relaxed": [
                "stress",
                "stressed",
                "tired",
                "calm",
                "peace",
                "relax",
                "sleep"
            ],

            "scared": [
                "fear",
                "ghost",
                "scary",
                "horror",
                "afraid"
            ],

            "thoughtful": [
                "think",
                "life",
                "future",
                "philosophy",
                "deep"
            ],

            "excited": [
                "action",
                "thrill",
                "adventure",
                "adrenaline"
            ]
        }

    def preprocess(self, text):

        text = text.lower()

        text = re.sub(r"[^a-zA-Z ]", "", text)

        return text

    def predict(self, text):

        text = self.preprocess(text)

        scores = {}

        for mood, words in self.mood_keywords.items():

            scores[mood] = 0

            for word in words:

                if word in text:

                    scores[mood] += 1

        predicted = max(scores, key=scores.get)

        if scores[predicted] == 0:
            return "neutral"

        return predicted