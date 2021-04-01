# Author: Michael Fuhrer
# Created: 2021-03-23   Last Updated: 2021-04-01
#
# Used by ner_core to open file/website based on user query.
import requests
from bs4 import BeautifulSoup


class NER_Article_Reader:
    def __init__(self, file_name="", size_limit=8184):
        # Parameterized constructor that automatically opens file (if valid) and sets size_limit.
        if file_name != "":
            self.open_file(file_name)
        self.chunk_size_limit = size_limit  # Bytes/Characters
        self.carry_over_text = ""

    def readNextChunk(self):
        # Returns the next 'chunk' within the opened text file. This chunk will crop out the any incomplete sentence
        # at the end of the chunk, as to preserve the sentence structure to improve NPL parsing behavior down the line.
        read_str = self.carry_over_text  # Copy over any cropped text from previous chunk
        # Read new chunk
        read_str += self.text_file.read(self.chunk_size_limit - len(self.carry_over_text))
        # Find crop location.
        sentence_end_loc = max([read_str.rfind("."), read_str.rfind("?"), read_str.rfind("!")])
        word_end_loc = max([read_str.rfind(" "), read_str.rfind("\n"), read_str.rfind("\t")])
        if sentence_end_loc > 0:
            # Sentence end found, crop incomplete sentence and return
            self.carry_over_text = read_str[sentence_end_loc + 1:]
            return read_str[:sentence_end_loc + 1]
        elif word_end_loc > 0:
            # No sentence end found, but we can separate a word out. Crop and return.
            self.carry_over_text = read_str[word_end_loc + 1:]
            return read_str[:word_end_loc]
        else:
            # Unable to crop the chunk meaningfully. Just return the entire chunk.
            self.carry_over_text = ""
            return read_str

    def open_file(self, file_name):
        # Opens the given file.
        self.text_file = open(file_name, "r", encoding='utf-8')

    def close(self):
        # Closes the open text file.
        self.text_file.close()

    def webscape(self, url, save_file_name):
        # Uses requests and Beautiful Soup to scape text of the html file of a given website and save it into the
        # designated file. Reader will then reopen the file to be read for NER parsing.
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        # Saving webpage text to file
        save_file = open(save_file_name, "w", encoding='utf-8')
        save_file.write(soup.text)
        save_file.close()
        # Reopen file in read-only to NER parsing
        self.open_file(save_file_name)