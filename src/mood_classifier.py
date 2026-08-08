import re


class MoodClassifier:

    def __init__(self):

        self.mood_keywords = {

            "happy": [
                "happy",
                "joy",
                "great",
                "excited",
                "exciting",
                "fun",
                "funny",
                "cheerful",
                "awesome",
                "smile",
                "celebrate",
                "party",
                "laugh",
                "hilarious"
            ],

            "sad": [
                "sad",
                "sadness",
                "cry",
                "depressed",
                "heartbroken",
                "upset",
                "lonely",
                "grief",
                "miserable",
                "tear"
            ],

            "romantic": [
                "love",
                "loved",
                "romantic",
                "date",
                "partner",
                "relationship",
                "miss",
                "crush",
                "kiss",
                "valentine"
            ],

            "motivated": [
                "motivation",
                "success",
                "goal",
                "winner",
                "career",
                "inspire",
                "achieve",
                "ambition",
                "drive"
            ],

            "relaxed": [
                "stress",
                "stressful",
                "stressed",
                "tired",
                "calm",
                "peace",
                "relax",
                "sleep",
                "lazy",
                "chill",
                "bored"
            ],

            "scared": [
                "fear",
                "ghost",
                "scary",
                "horror",
                "afraid",
                "terrified",
                "creepy",
                "haunted"
            ],

            "thoughtful": [
                "think",
                "life",
                "future",
                "philosophy",
                "deep",
                "reflect",
                "meaning",
                "existential"
            ],

            "excited": [
                "action",
                "thrill",
                "adventure",
                "adrenaline",
                "intense",
                "fast"
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

                # Use word boundary matching to avoid partial word matches
                # e.g., "fun" should not match "funny", "sad" should not match "saddle"
                pattern = r"\b" + re.escape(word) + r"\b"

                if re.search(pattern, text):

                    scores[mood] += 1

        predicted = max(scores, key=scores.get)

        if scores[predicted] == 0:
            return "relaxed"

        return {
            "mood": predicted,
            "confidence": scores[predicted] / sum(scores.values())
        }
