# Author: Michael Fuhrer
# Created: 2021-03-23   Last Updated: 2021-04-01
# Primary NER tool. Contains input parsing logic to set up NLP model as well as functions to initialize and operate
# article reader and NLP model according to input instructions.
import spacy  # Main NPL interpreter
import sortedcontainers  # Used to organized desired tokens
from article_handler import NER_Article_Reader

lang_dict = {
    # English
    "english": "en_core_web",
    "en": "en_core_web",
    "en_core_web_sm": "en_core_web",
    # German
    "german": "de_core_news",
    "deutsch": "de_core_news",
    "de": "de_core_news",
    "de_core_news_sm": "de_core_news",
    # French
    "french": "fr_core_news",
    "francaise": "fr_core_news",
    "fr": "fr_core_news",
    "fr_core_news_sm": "fr_core_news",
    # Italian
    "italian": "it_core_news",
    "italiano": "it_core_news",
    "it_core_news_sm": "it_core_news"
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
    # Proper Noun / Named Entity
    "proper noun": "PROPN",
    "proper_noun": "PROPN",
    "proper-noun": "PROPN",
    "named entity": "PROPN",
    "named_entity": "PROPN",
    "named-entity": "PROPN",
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


# ---------------------------------- NER Core Class ----------------------------------

class NER_Core:

    # ---------------------------------- Input flag handling functions ----------------------------------
    # Each function handles their respective flag behavior. Every function has the same input, a list
    # of string arguments, and same output, a tuple indicating whether the flag could be set successfully
    # and a new, cropped list of arguments.
    #
    # These functions are then put into a dictionary to be easily accessed in ner_core.parse() function.

    def file_flag(self, arguments):
        # Handles "-f" flag behavior, which specifies a file to be read by the core. Requires one argument.
        if len(arguments) > 0 and arguments[0][0] != '-' and self.website == "" and self.read_file == "":
            # Valid input
            self.read_file = arguments[0]
            return [True, arguments[1:]]
        else:
            # Invalid input
            if len(arguments) == 0 or (len(arguments) > 0 and arguments[0][0] == '-'):
                # Flag needs one argument, none were given.
                print("Parse error: \"-f\" needs one argument; none were given.")
            elif self.website != "":
                # Already specified a website to scrape from
                print("Parse error: \"-f\" cannot read file. Already specified a website to read from.")
            else:
                # Already specified a file to read from
                print("Parse error: Multiple instances of \"-f\"")
            return [False, arguments]

    def pos_flag(self, arguments):
        # Handles "-p" flag behavior, which specifies the desired part-of-speech. Requires one argument.
        if len(arguments) > 0 and (arguments[0].lower() in pos_dict):
            # Valid input
            self.desired_POS = pos_dict[arguments[0].lower()]
            return [True, arguments[1:]]
        else:
            # Invalid input
            if len(arguments) == 0:
                # Flag needs one argument, none were given
                print("Parse error: \"-p\" needs one argument; none were given.")
            else:
                # Dictionary could not find inputted value
                print("Parse error: Given part-of-speech was not recognized.")
            return [False, arguments]

    def lang_flag(self, arguments):
        # Handles "-l" flag behavior, which specifies the language the NLP model will operate under. Requires one
        # argument.
        if len(arguments) > 0 and (arguments[0].lower() in lang_dict):
            # Valid input
            self.lang = lang_dict[arguments[0].lower()]
            return [True, arguments[1:]]
        else:
            # Invalid input
            if len(arguments) == 0:
                # Flag needs one argument, none were given
                print("Parse error: \"-l\" needs one argument; none were given.")
            else:
                # Dictionary could not find inputted value
                print("Parse error: Given language was not recognized.")
            return [False, arguments]

    def web_flag(self, arguments):
        # Handles "-web" flag behavior, which specifies the website the reader will scrape from and which file to save
        # the text into. Requires two arguments.
        if len(arguments) > 1 and arguments[0][0] != '-' and arguments[1][0] != '-' and self.read_file == "" and self.website == "":
            # Valid input
            self.website = arguments[0]
            self.read_file = arguments[1]
            return [True, arguments[2:]]
        else:
            # Invalid Input
            if len(arguments) < 2 or (len(arguments) > 1 and (arguments[0][0] == '-' or arguments[1][0] == '-')):
                # Flag needs two arguments, not enough were given
                print("Parse error: \"-web\" needs two arguments: website and filename.")
            elif self.website != "":
                # Already specified a website to scrape from
                print("Parse error: Multiple instances of \"-web\"")
            else:
                # Already specified a file to read from
                print("Parse error: \"-web\" cannot read site. Already specified a file to read from.")
            return [False, arguments]

    def acc_flag(self, arguments):
        # Handles "-a" flag behavior, which selects the more accurate, but less efficient NLP model. Doesn't require
        # any arguments.
        self.suffix = "_trf"
        return [True, arguments]

    def file_write_flag(self, arguments):
        # Handles "-w" flag behavior, which specifies a file to be written to by the core. Requires one argument.
        if len(arguments) > 0 and arguments[0][0] != '-' and self.save_file == "":
            # Valid input
            self.save_file = arguments[0]
            return [True, arguments[1:]]
        else:
            # Invalid input
            if len(arguments) == 0 or (len(arguments) > 0 and arguments[0][0] == '-'):
                # Flag needs one argument, none were given.
                print("Parse error: \"-w\" needs one argument; none were given.")
            else:
                # Already specified a file to save to
                print("Parse error: Multiple instances of \"-w\"")
            return [False, arguments]

    # ---------------------------------- NER Core Class Functions ----------------------------------
    def __init__(self):
        # Default constructor
        self.read_file = ""
        self.website = ""
        self.save_file = ""
        self.text_arg = ""
        self.lang = "en_core_web"
        self.suffix = "_sm"
        self.desired_POS = "PROPN"
        self.reader = NER_Article_Reader()
        self.desired_tokens = sortedcontainers.SortedSet()  # Using sorted set to preserve uniqueness
        self.nlp = None
        self.flag_dict = {
            "-f": self.file_flag,
            "-p": self.pos_flag,
            "-l": self.lang_flag,
            "-web": self.web_flag,
            "-a": self.acc_flag,
            "-w": self.file_write_flag
        }

    def initialize_nlp(self):
        # Tries to load the spaCy pipeline. If it fails, function will notify user how to install the pipeline.
        success = True
        try:
            self.nlp = spacy.load(self.lang + self.suffix)
        except:
            # Could not load model
            success = False
            print("Run Error: Failed to load \"" + self.lang + self.suffix + "\" spaCy pipeline.")
            print("Please make sure the pipeline is installed by using: ", end='')
            print("python -m spacy download " + self.lang + self.suffix)
        return success

    def read_text(self, text):
        # Passes the given text through the NLP model and saves any returned tokens that match the set
        # desired part-of-speech into the desired tokens set.
        doc = self.nlp(text)
        for token in doc:
            if token.pos_ == self.desired_POS:
                self.desired_tokens.add(token.text)
        return doc

    def read_from_file(self):
        # Reads given file, chunk by chunk, and passes chunks through NLP model and save any relevant tokens to
        # desired set.
        next_chunk = self.reader.readNextChunk()
        while next_chunk != "":
            self.read_text(next_chunk)
            next_chunk = self.reader.readNextChunk()

    def echo_to_file(self):
        save_file = open(self.save_file, "w")
        for token in self.desired_tokens:
            save_file.write(token + "\n")
        save_file.close()

    def printDesiredTokens(self):
        # Prints each entry in the desired tokens set in the console.
        print("---------- " + self.desired_POS + " Tokens Found in Text ----------")
        for token in self.desired_tokens:
            print(token)

        if self.save_file != "":
            # Save file specified as well, echo
            self.echo_to_file()

    def run(self):
        # Comprehensive run operation. Will adjust inputs to NLP based on settings established during parsing, ex. if
        # a file was set to read, the article handler will feed text from file into NLP; if just text was given, it will
        # be directly given to the NLP; etc.
        initialized = self.initialize_nlp()
        if not initialized:
            # Couldn't initialize pipeline
            return []
        # Reading text
        if self.read_file != "":
            # File and website behavior
            if self.website != "":
                # Website specified
                self.reader.webscape(self.website, self.read_file)
            else:
                # File specified
                self.reader.open_file(self.read_file)
            self.read_from_file()
            self.reader.close()
        elif self.text_arg != "":
            # Text from argument
            self.read_text(self.text_arg)
        else:
            # No text to read
            print("Run error: No text was specified.")
            return []

        # Output
        self.printDesiredTokens()
        return self.desired_tokens

    def parseArguments(self, arguments):
        # Parses console input to adjust core behavior. Checks for flags and handles unexpected behavior. Returns a
        # boolean indicating whether the arguments could be successfully interpreted.
        input_ok = True
        while len(arguments) > 0 and input_ok:
            if arguments[0][0] == '-':
                # Flag argument
                if arguments[0] in self.flag_dict:
                    # Valid flag
                    [input_ok, arguments] = self.flag_dict[arguments[0]](arguments[1:])
                else:
                    # Invalid flag
                    print("Parse error: unrecognized flag.")
                    input_ok = False
            else:
                # Text argument
                if self.read_file == "":
                    # No read file or website has been specified, accept text argument
                    self.text_arg = arguments[0]
                    if len(arguments) > 1:
                        # Arguments exist after text. Ignore them, but notify user.
                        print("Parse warning: arguments after read text have been ignored.")
                else:
                    # A read file or website have been specified, ignore text and notify user.
                    print("Parse warning: cannot parse text and file/website. Ignoring text and any arguments after.")
                arguments = []

        return input_ok
