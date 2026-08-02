import re
import string


class TextPreprocessor:
    """
    Handles basic preprocessing of message text.
    """

    def __init__(self):
        pass

    def clean_text(self, text):
        """
        Clean message text.
        """

        if text is None:
            return ""

        text = str(text)

        # Lowercase
        text = text.lower()

        # Remove URLs
        text = re.sub(r"http\S+|www\S+", "", text)

        # Remove extra spaces
        text = re.sub(r"\s+", " ", text).strip()

        # Remove punctuation
        text = text.translate(str.maketrans("", "", string.punctuation))

        return text

    def tokenize(self, text):
        """
        Split text into words.
        """

        cleaned = self.clean_text(text)

        return cleaned.split()

    def word_count(self, text):
        """
        Count number of words and words.
        """

        return len(self.tokenize(text))