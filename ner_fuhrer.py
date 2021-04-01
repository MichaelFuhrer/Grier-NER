# Author: Michael Fuhrer
# Created: 2021-03-23   Last Updated: 2021-03-31
#
# Contains main function call for Grier-NER. Creates an instance of NER Core to handle system arguments.
import sys  # Used to retrieve arguments
from ner_core import NER_Core


def displayHelp():
    print("--------------------------- Grier-NER ---------------------------")
    print("Grier-NER is a Python Named Entity Recognition (NER) project for")
    print("Grier Forensics 2021 Intern Software Engineer coding challenge.")
    print("")
    print("Author: Michael Fuhrer | mfuhrer@vt.edu")
    print("Last Updated: 2021-03-31")
    print("")
    print("Usage:")
    print("Place any text, contained within quotations, to have the NPL model")
    print("parse through and list Named Entities or other specified part-of-")
    print("speech. Alternatively, using the \"-f\" or \"-web\" flags, specify")
    print("text to have the program parse through automatically.")
    print("")
    print("-f <filename> : has the program parse through text of a given file.")
    print("-web <website> <filename> : webscrapes text from the specified")
    print("                website and saves the text to the given file before")
    print("                parsing through it.")
    print("-p <pos>      : flags a certain part-of-speech to be listed by the ")
    print("                program. This is by default set to proper nouns, i.e.")
    print("                named entities")
    print("-l <lang>     : sets the model's language. This is by default ")
    print("                English.")
    print("-w <filename> : specifies a file to write/echo console output to.")
    print("-a            : flag to select the more accurate, but less efficient")
    print("                NLP model. These spaCy models use the _trf suffix.")
    print("-----------------------------------------------------------------")


if __name__ == '__main__':
    # Main function call
    if len(sys.argv) == 1:
        displayHelp()
    else:
        core = NER_Core()
        input_ok = core.parseArguments(sys.argv[1:])
        if input_ok:
            core.run()
