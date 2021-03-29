# Author: Michael Fuhrer
# Created: 2021-03-23   Last Updated: 2021-03-28
import spacy  # Main NPL interpreter
import sortedcontainers  # Used to organized desired tokens
from article_handler import NER_Article_Reader


class NER_Core:
    def __init__(self, language="en_core_web_sm", pos="PROPN"):
        self.nlp = spacy.load(language)
        self.desired_tokens = sortedcontainers.SortedSet() #Using sorted set to preserve uniqueness
        self.desired_POS = pos

    def read(self, text):
        doc = self.nlp(text)
        for token in doc:
            if token.pos_ == self.desired_POS:
                self.desired_tokens.add(token.text)
        return doc

    def printDesiredTokens(self):
        for token in self.desired_tokens:
            print(token)
