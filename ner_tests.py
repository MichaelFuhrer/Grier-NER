"""
# Author: Michael Fuhrer | mfuhrer@vt.edu
# Created: 2021-03-28   Last Updated: 2021-04-01
#
# Used by ner_fuhrer to open file/website based on user query.
"""
import unittest  # Main testing framework
import time  # Used to test computation time for some tests
from ner_core import NER_Core
from article_handler import NER_Article_Reader


def NER_article_read(file_name, byte_count=4092, display=False, lang="en_core_web_sm"):
    # Runs the given file through an NER core. Text chunk size, language, and whether output should be displayed are
    # customizable depending on test case.
    core = NER_Core()
    core.lang = lang
    core.suffix = ""
    core.initialize_nlp()
    core.reader = NER_Article_Reader(file_name, byte_count)
    core.read_from_file()
    if display:
        core.printDesiredTokens()
    return core.desired_tokens


class NER_Tester(unittest.TestCase):

    def test_simple_text(self):
        # Testing spaCy's ability to discern proper nouns from rest of test using a few simple sentences.
        # Some sentences contain capitalized nouns that are not proper, so the NPL model should avoid flagging these
        # as proper nouns.
        file_name = "tests/test-simple.txt"
        expected_tokens = ["Apple", "Dave", "Mr.", "Noel", "Wall"]
        found_tokens = NER_article_read(file_name)
        assert expected_tokens == found_tokens._list

    def test_german_simple_text(self):
        # Testing spaCy's multi-language support using a sample text similar to test-simple.txt, just in German.
        # German should be especially tricky for the model to classify, as all nouns (except pronouns) in German are
        # capitalized. This means that the model will have to rely on sentence context and an internal dictionary to
        # determine which nouns are proper.
        # Note: titles, like "Herr", in German are not considered proper nouns, see:
        # https://wiki.uni-due.de/orthoundgrafshowroom/index.php/Gro%C3%9F-_und_Kleinschreibung:_Eigennamen_(%C2%A7_59_-_%C2%A7_62)
        # Unlike English, where titles like "Mr." are considered proper nouns.
        file_name = "tests/test-german-simple.txt"
        expected_tokens = ["Apple", "Dave", "Mauer", "Noel"]
        found_tokens = NER_article_read(file_name, lang="de_core_news_sm", display=True)
        assert expected_tokens == found_tokens._list

    def test_accuracy(self):
        # More comprehensive test of spaCy's accuracy. Example text to be parsed is the Emancipation Proclamation, as it
        # contains a lot of proper nouns. The model's classification will be compared against a precompiled list of
        # pronouns I could pull from the same text. Because of the possibility of error - either human or computational
        # - accuracy will be done via a score system.
        file_name = "tests/emancipation-proclamation.txt"
        expected_file_name = "tests/emancipation-proclamation-propn.txt"
        found_tokens = set(NER_article_read(file_name)._list)
        expected_file = open(expected_file_name)
        expected_tokens = set([line[:-1] for line in expected_file])
        expected_but_not_found = expected_tokens.difference(found_tokens)
        found_but_not_expected = found_tokens.difference(expected_tokens)
        print("Expected tokens that were not identified by NER:")
        for token in expected_but_not_found:
            print(token)
        print("Found tokens that were not expected:")
        for token in found_but_not_expected:
            print(token)
        accuracy = (len(expected_tokens)-(len(expected_but_not_found) + len(found_but_not_expected))) / len(expected_tokens)
        print("Approximate accuracy: %.2f" % accuracy)
        assert accuracy >= 0.8

    def test_parse_behavior(self):
        # Test to ensure article reader preserves words and sentences when 'chunking' them. Reading from a custom text
        # file, test-parse-behavior.txt which contained sentences/words of certain length that will require the cropping
        # behavior of article reader to preserve.
        reader = NER_Article_Reader("./tests/test-parse-behavior.txt", size_limit=16)
        # Get each chunk from file, we should expect seven preserved sentences/words with variable length
        expected_chunks = ["one two three.", "four five six?", "seven eight!", "nine ten.", "onetwothreefour",
                           "fivesixseven", "nineteneleven"]
        read_chunks = []
        chunk = reader.readNextChunk()
        while chunk != "":
            read_chunks.append(chunk.strip(" \n"))
            chunk = reader.readNextChunk()
        assert read_chunks == expected_chunks


    def test_parse_timing(self):
        # Test used to compare the computation time of different methods of parsing through a text file. Compares
        # line-by-line reading, <=1024 byte chunk reading, and <=4092 byte chunk reading.
        file_name = "tests/moby-dick.txt"
        # Line-by-line reading
        print("------   Line-by-Line Reading...   ------")
        t0_start = time.time()
        core = NER_Core()
        with open(file_name, "rb") as read_file:
            for line in read_file:
                core.read(line.decode('utf-8'))
        read_file.close()
        t0_end = time.time()
        t0_total = t0_end - t0_start
        print("Elapsed Time: %.3f" % t0_total)

        def timed_read(byte_count):
            print("------   %dB Chunk Reading...   ------" % byte_count)
            t_start = time.time()
            NER_article_read(file_name, byte_count)
            t_end = time.time()
            t_total = t_end - t_start
            print("Elapsed Time: %.3f" % t_total)

        # Chunk (1024 Bytes) reading
        timed_read(1024)
        # Chunk (4096 Bytes) reading
        timed_read(4092)

    def test_webscrape(self):
        # Tests webscraping behavior by pulling text from gutenberg.org and saving it in test folder.
        url = "https://www.gutenberg.org/files/64317/64317-h/64317-h.htm"
        save_name = "tests/great-gatsby.txt"
        reader = NER_Article_Reader()
        reader.webscape(url, save_name)
        core = NER_Core()
        while True:
            next_line = reader.readNextChunk()
            if next_line == "":
                break
            core.read(next_line)
        core.printDesiredTokens()
        reader.close()

    def test_webscape_against_file(self):
        # Tests webscraping behavior by pulling text from gutenberg.org and saving it in test folder.
        url = "https://www.gutenberg.org/files/2701/2701-0.txt"
        web_name = "tests/moby-dick-webscraped.txt"
        file_name = "tests/moby-dick.txt" # Result of copy+pasting from the website
        reader = NER_Article_Reader()
        # Webscraping
        reader.webscape(url, web_name)
        core = NER_Core()
        while True:
            next_line = reader.readNextChunk()
            if next_line == "":
                break
            core.read(next_line)
        webscraped_tokens = set(core.desired_tokens)
        reader.close()
        # Read from file
        reader.open_file(file_name)
        core = NER_Core() # Reset core
        while True:
            next_line = reader.readNextChunk()
            if next_line == "":
                break
            core.read(next_line)
        file_tokens = set(core.desired_tokens)
        # Comparing Results
        tokens_only_in_web = webscraped_tokens.difference(file_tokens)
        print("Named Entities exclusively found in webscraped version:")
        for token in tokens_only_in_web:
            print(token)
        tokens_only_in_file = file_tokens.difference(webscraped_tokens)
        print("\nNamed Entities exclusively found in copy+paste file version:")
        for token in tokens_only_in_file:
            print(token)
        accuracy = (len(file_tokens)-(len(tokens_only_in_file) + len(tokens_only_in_web))) / len(file_tokens)
        reader.close()
        print("\nAccuracy: %.2f" % (accuracy*100))
        assert accuracy >= 0.95


if __name__ == "__main__":
    unittest.main()
