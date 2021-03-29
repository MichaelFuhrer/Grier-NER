"""
# Author: Michael Fuhrer | mfuhrer@vt.edu
# Created: 2021-03-28   Last Updated: 2021-03-28
#
# Used by ner_fuhrer to open file/website based on user query.
"""
import unittest  # Main testing framework
import time  # Used to test computation time for some tests
from ner_core import NER_Core
from article_handler import NER_Article_Reader


def NER_article_read(file_name, byte_count=4092, display=False, lang="en_core_web_sm"):
    core = NER_Core(language=lang)
    article_reader = NER_Article_Reader(file_name, byte_count)
    while True:
        next_line = article_reader.readNextChunk()
        if next_line == "":
            break
        core.read(next_line)
    if display:
        core.printDesiredTokens()
    article_reader.close()
    return core.desired_tokens


class NER_Tester(unittest.TestCase):

    def test_simple_text(self):
        # Testing spaCy's ability to discern proper nouns from rest of test using a few simple sentences.
        # Some sentences contain capitalized nouns that are not proper, so the NPL model should avoid flagging these
        # as proper nouns.
        file_name = "tests/test-simple.txt"
        expected_tokens = ["Apple", "Dave", "Julie", "Mr.", "Wall"]
        found_tokens = NER_article_read(file_name)
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

    def test_parse_timing(self):
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


if __name__ == "__main__":
    unittest.main()
