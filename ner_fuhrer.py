# Author: Michael Fuhrer
# Created: 2021-03-23   Last Updated: 2021-03-23
#
# Contains main function call for Grier-NER. Will handle and parse
# user input and accordingly operate ner_core to produce desired output.
import sys  # Used to retrieve arguments
from ner_core import NER_Core
from article_handler import NER_Article_Reader

lang_dict = {
    # English
    "english": "en_core_web_sm",
    "en": "en_core_web_sm",
    "en_core_web_sm": "en_core_web_sm",
    # German
    "german": "de_core_news_sm",
    "deutsch": "de_core_news_sm",
    "de": "de_core_news_sm",
    "de_core_news_sm": "de_core_news_sm",
    # French
    "french": "fr_core_news_sm",
    "francaise": "fr_core_news_sm",
    "fr": "fr_core_news_sm",
    "fr_core_news_sm": "fr_core_news_sm",
    # Italian
    "italian": "it_core_news_sm",
    "italiano": "it_core_news_sm",
    "it_core_news_sm": "it_core_news_sm"
    # Multi-Language [untested]
    # "multi-language": "xx",
    # "xx": "xx"
}

pos_dict = {
    # Adjective
    "adjective": "ADJ",
    "adj": "ADJ",
    # Adposition
    "adposition": "ADP",
    "adp": "ADP",
    # Adverb
    "adverb": "ADV",
    "adv": "ADV",
    # Auxiliary Verb
    "auxiliary verb": "AUX",
    "auxiliary_verb": "AUX",
    "auxiliary-verb": "AUX",
    "aux": "AUX",
    # Coordinating Conjunction
    "coordinating conjunction": "CONJ",
    "coordinating_conjunction": "CONJ",
    "coordinating-conjunction": "CONJ",
    "conj": "CONJ",
    # Determiner
    "determiner": "DET",
    "det": "DET",
    # Interjection
    "interjection": "INJ",
    "inj": "INJ",
    # Noun
    "noun": "NOUN",
    # Numeral
    "numeral": "NUM",
    "number": "NUM",
    "num": "NUM",
    # Particle
    "particle": "PART",
    "part": "PART",
    # Pronoun
    "pronoun": "PRON",
    "pron": "PRON",
    # Proper Noun
    "proper noun": "PROPN",
    "proper_noun": "PROPN",
    "proper-noun": "PROPN",
    "propn": "PROPN",
    # Punctuation
    "punctuation": "PUNCT",
    "punct": "PUNCT",
    # Subordinating Conjunction
    "subordinating conjunction": "SCONJ",
    "subordinating_conjunction": "SCONJ",
    "subordinating-conjunction": "SCONJ",
    "sconj": "SCONJ",
    # Symbol
    "symbol": "SYM",
    "sym": "SYM",
    # Verb
    "verb": "VERB",
    # Other
    "other": "X",
    "x": "X"

}


def displayHelp():
    print("--------------------------- Grier-NER ---------------------------")
    print("Grier-NER is a Python Named Entity Recognition (NER) project for")
    print("Grier Forensics 2021 Intern Software Engineer coding challenge.")
    print("")
    print("Author: Michael Fuhrer | mfuhrer@vt.edu")
    print("Last Updated: 2021-03-28")
    print("")
    print("Usage:")
    print("Place any text, contained within quotations, to have the NPL model")
    print("parse through and list proper pronouns or other specified part-of-")
    print("speech.")
    print("-f <filename> : has the program instead parse through a given file.")
    print("-p <pos> : flags a certain part-of-speech to be listed by the program.")
    print("           This is by default set to proper noun, as per the project")
    print("           description.")
    print("-l <lang> : sets the model's language. This is by default English.")
    print("-----------------------------------------------------------------")


if __name__ == '__main__':
    # Main function call
    input_ok = True
    file_read = False
    text_argument = ""
    part_of_speech = "PROPN"
    language = "en_core_web_sm"
    # ----- Start of Input Parsing -----
    if len(sys.argv) == 1:
        # No passed arguments, display syntax help
        displayHelp()
        input_ok = False
    else:
        # Passed arguments, parse through
        i = 1
        while i < len(sys.argv):
            arg = sys.argv[i]
            if arg[0] == '-':
                # Flag found, ensure there's an argument after
                if i == len(sys.argv):
                    # No argument after
                    print("No argument following flag \"" + arg + "\". Cannot interpret request.")
                    input_ok = False
                    break
                # Next argument found
                if arg == "-f":
                    # Specify file flag
                    file_read = True
                    text_argument = sys.argv[i + 1]
                elif arg == "-p":
                    # Specify part of speech flag
                    if sys.argv[i + 1].lower() in pos_dict:
                        # Valid part-of-speech entry
                        part_of_speech = pos_dict[sys.argv[i + 1].lower()]
                    else:
                        # Given argument was unrecognized
                        print("Unrecognized part-of-speech: \"" + sys.argv[i + 1] + "\". Cannot interpret request.")
                        input_ok = False
                        break
                elif arg == "-l":
                    # Specify language flag
                    if sys.argv[i + 1].lower() in lang_dict:
                        # Valid language entry
                        language = lang_dict[sys.argv[i + 1].lower()]
                    else:
                        # Given argument was unrecognized
                        print("Unrecognized language: \"" + sys.argv[i + 1] + "\". Cannot interpret request.")
                        input_ok = False
                        break
                else:
                    pass
                    # Unrecognized flag
                    print("Unrecognized flag \"" + arg + "\". Cannot interpret request.")
                    input_ok = False
                    break
                i += 1  # Increment i to skip over already handled argument
            else:
                # Text
                if file_read:
                    # User already wants to read from file, display error message
                    print("Cannot parse given text as a file has already been specified. Reading file...")
                    break
                text_argument = arg
            i += 1

    # ----- End of Input Parsing -----
    # ----- Start of NER Behavior -----
    if input_ok:
        core = NER_Core(language, part_of_speech)
        if file_read:
            # Read from file
            reader = NER_Article_Reader(text_argument)
            while True:
                next_line = reader.readNextChunk()
                if next_line == "":
                    # End of file
                    break
                core.read(next_line)
        else:
            # Read from argument text
            core.read(text_argument)

        core.printDesiredTokens()
    # ----- End of NER Behavior -----
