import logging


logger = logging.getLogger(__name__)


class TextService(object):
    """Contains helpful functions related to working with text"""

    def __init__(self):
        logger.debug("Creating the TextService")

    @staticmethod
    def word_count(text):
        text = text.lower()
        tokens = text.split()
        text_dict = {}

        # count how many times a word occurs
        for token in tokens:
            if text_dict.get(token):
                text_dict[token] += 1
            else:
                text_dict[token] = 1

        return text_dict

    @staticmethod
    def translate_to_UTF8(s):
        return s.encode('utf-8', 'ignore')

    @staticmethod
    def translate_to_ascii(s):
        return s.encode('ascii', 'ignore')
