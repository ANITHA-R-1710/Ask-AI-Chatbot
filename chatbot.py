
import json
import re
from pathlib import Path
from difflib import SequenceMatcher


class StudentChatbot:

    def __init__(self):
        self.faq_data = self.load_faq()

    # LOAD FAQ DATA
    def load_faq(self):

        file_path = Path(__file__).parent / "faq_data.json"

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                print("FAQ loading error: JSON must contain a list.")
                return []

            return data

        except FileNotFoundError:
            print("FAQ file not found:", file_path)
            return []

        except json.JSONDecodeError as error:
            print("Invalid FAQ JSON:", error)
            return []

        except Exception as error:
            print("FAQ loading error:", error)
            return []

    # CLEAN TEXT
    def clean_text(self, text):

        text = str(text).lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()

        return text

    # HANDLE GREETINGS AND COMMON MESSAGES
    def handle_common_messages(self, question):

        cleaned = self.clean_text(question)

        greetings = [
            "hi",
            "hii",
            "hiii",
            "hello",
            "hey",
            "good morning",
            "good afternoon",
            "good evening"
        ]

        thanks = [
            "thanks",
            "thank you",
            "thank u",
            "thanks a lot"
        ]

        goodbyes = [
            "bye",
            "goodbye",
            "see you",
            "see you later"
        ]

        if cleaned in greetings:
            return (
                "Hello! 👋 Welcome to Ask AI!\n\n"
                "I'm here to help you learn about programming, "
                "Artificial Intelligence, Machine Learning, "
                "Data Science and academic topics.\n\n"
                "What would you like to learn today?"
            )

        if cleaned in thanks:
            return (
                "You're welcome! 😊 "
                "Feel free to ask me another question."
            )

        if cleaned in goodbyes:
            return (
                "Goodbye! 👋 Keep learning and have a great day!"
            )

        return None

    # FIND BEST MATCHING FAQ
    def find_relevant_faq(self, question):

        stop_words = {
            "what", "is", "are", "the", "a", "an",
            "of", "in", "on", "for", "to", "and",
            "how", "why", "can", "you", "explain",
            "tell", "me", "about", "please", "define",
            "do", "does", "this", "that", "it",
            "with", "give", "show", "describe",
            "meaning", "which", "who", "when"
        }

        question_clean = self.clean_text(question)
        question_words = set(question_clean.split()) - stop_words

        if not question_words:
            return None

        best_match = None
        highest_score = 0

        for item in self.faq_data:

            if not isinstance(item, dict):
                continue

            faq_question = item.get("question", "")
            faq_answer = item.get("answer", "")

            if not faq_question or not faq_answer:
                continue

            faq_clean = self.clean_text(faq_question)
            faq_words = set(faq_clean.split()) - stop_words

            if not faq_words:
                continue

            # Calculate common words
            common_words = question_words.intersection(faq_words)

            # Calculate query word matching percentage
            coverage_score = len(common_words) / len(question_words)

            # Calculate overall similarity
            similarity_score = SequenceMatcher(
                None,
                question_clean,
                faq_clean
            ).ratio()

            # Give more importance to matching keywords
            score = (coverage_score * 0.75) + (similarity_score * 0.25)

            if score > highest_score:
                highest_score = score
                best_match = item

        # Return the best sufficiently matching FAQ
        if highest_score >= 0.40:
            return best_match

        return None

    # GENERATE RESPONSE
    def get_response(self, question, history=None):

        if not question or not question.strip():
            return "Please enter a question."

        # Check common messages first
        common_response = self.handle_common_messages(question)

        if common_response:
            return common_response

        # Check FAQ availability
        if not self.faq_data:
            return (
                "Sorry! I couldn't load my FAQ knowledge base. "
                "Please check your faq_data.json file."
            )

        # Search for matching FAQ
        matched_faq = self.find_relevant_faq(question)

        if matched_faq:
            return matched_faq["answer"]

        # No matching FAQ
        return (
            "Sorry! I don't have an answer to this question "
            "in my current FAQ knowledge base yet. "
            "Please try asking about another topic."
        )
