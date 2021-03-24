# Author: Michael Fuhrer
# Created: 2021-03-23   Last Updated: 2021-03-23
import spacy


class NER_Core:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def read(self, text):
        return self.nlp(text)


if __name__ == "__main__":
    core = NER_Core()
    doc = core.read("Hello world. How are y'all today?")

    for token in doc:
        print(token.text, token.pos_, token.dep_)
