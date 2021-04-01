# Grier-NER
Grier-NER is a Python Named Entity Recognition (NER) project for 
Grier Forensics 2021 Intern Software Engineer coding challenge.
### Project Info
Author: Michael Fuhrer, mfuhrer@vt.edu  
Created: March 23, 2021 | Deadline: April 2, 2021
## Dependencies
All dependencies used for this project are included in **requirements.txt**. Please install them prior use by using:
>pip install -r requirements.txt
#### <u>spaCy</u>
Grier-NER uses spaCy, an open-source natural language processing
library created by Matthew Honnibal. spaCy was selected to use
in this project because it best matches expectations and criteria laid out in
problem description; it's open-source, can operate offline, and is relatively
easy to implement. Additionally, spaCy better fits this project when compared to
other libraries, like NLTK and PyTorch; as spaCy has multi-language support and
 has the most abstracted implementation. The only downside to using spaCy when compared 
to other libraries is that each language model must be downloaded and installed before use. 
  
You may download additional language pipelines detailed here: https://spacy.io/usage/models  
Some of my unittests also use the German pipeline, de_core_news_sm. The console interface will notify users when and 
how to install new language pipelines. Below is an example of how to install a new pipeline:
>python -m spacy download de_core_news_sm
>
  
#### <u>requests</u>
HTTP library used by webscraping feature to access a given URL.  
#### <u>BeautifulSoup</u>  
Used by webscraping feature to retrieve text from a website's HTML file and format it into a plain text file.  
#### <u>sortedcontainers</u>  
Used for its SortedSet class, which is used to uniquely catalog and alphabetically organize
the tokens of the desired part-of-speech within the given text.

## Usage
Call the main console interface by using:  
>python ner_fuhrer.py
> 
This alone, without any arguments will display similar usage instructions as below. To get the named entities within a  
few sentences of text, enter the text in quotations at the end of the declaration:
>python ner_fuhrer.py "Lorem ipsum dolor sit amet."
> 
Alternatively, a file can be read using the "-f" flag, followed by a file name.  
>python ner_fuhrer.py -f new-york-times.txt
>
Below is a comprehensive list of all the different flags and their function.  
> **-f [filename]:**  
> Specifies a file to read from. Takes in one argument, the name of the file. Incompatible with the "-web" flag and 
> suppresses any normal text inputs.  
>   
> **-web [url] [filename]:**  
> Has the program scrape text from the provided URL and save the text into the specified file. Program will then use the 
> file for parsing. Incompatible with the "-f" flag and suppresses any normal text inputs.  
>   
> **-p [part-of-speech]:**  
> Specifies what part-of-speech the NLP will look for. This is by default proper nouns, i.e. named entities.  
>   
> **-l [language]:**  
> Specifies what language the NLP pipeline is in. This is by default English. Currently English, French, German, and 
> Italian are supported, but more can be added by updating lang_dict in *ner_core.py*.
>   
> **-w [filename]:**  
> Echoes the console output to the given file.  
> 
> **-a:**  
> Sets the program to use the more accurate, but more computationally intensive NLP pipeline. Currently untested.
> 
## Process Log
Contains a chronological list of steps and decisions taken while developing this project.  
  
<u>2021-03-23</u>: Project start. Did general research on NER and NLP, found an open-source NLP
libraries that closely matched project requirements and criteria. Created rough skeleton
of project code and started formatting files. Compared different NLP libraries, NLTK, spaCy, and PyTorch,
to figure out which would work best for the project. Concluded spaCy would work the best, despite its initial 
installation overhead, because of its multi-language support and abstracted behavior. Began following spaCy tutorial @ 
https://spacy.io/usage/spacy-101 to better understand how to use library.    

<u>2021-03-28</u>: Experimented with parsing text files using spaCy, as the NLP model has a limit 
on the size of text it can accept. Developed a system to subdivide text into lines, so that NLP 
isn't overwhelmed by large texts and should reduce memory usage. This may, however, pose a slow-down 
in processing speed as the model is called on every line; will investigate further.  
  
Ran a timing test on a large text file (Moby Dick from gutenberg.org) to compare how quickly 
the model runs on each line vs. on chucks of lines, and my suspicions were confirmed; the 
line-by-line approach took about 127 seconds, whereas using chunks of up to 1024 bytes took only 
44 seconds, and using chucks up to 4092 bytes took 42 seconds - a ~3x increase from line-by-line. This
approach also better preserves sentence structure better than line-by-line, as it will crop the 
chunk to the nearest sentence if possible, then prepend the cropped section onto the next chunk.  
  
Created a working python console callable function in *ner_mfuhrer.py*. Function is able to take 
in arguments call the NER_Core according to given flags and text. For example, the console call:
>python ner_fuhrer.py -f ./tests/test-1.txt
>   
Will tell the program to display all proper nouns within the text file *test-1.txt*. Need to implement
dictionaries to convert human readable arguments, like "English" into more spaCy friendly arguments, 
like "en_core_web_sm".  
  
Added dictionaries, implemented flag behavior, and implemented a more comprehensive accuracy test, *test_accuracy*.  
  
<u>2021-03-29</u>: Created a simple test to test spaCy's German model against a German version of test-simple.txt, 
test-simple-german.txt. Model works remarkable well; it's able to discern proper nouns from common nouns through 
sentence context. It was able to correctly classify "Mauern" -> "walls" as a common noun and "Mauer" as a proper noun
because "Mauer" was preceded by "Herr" -> "Mr.", indicating that it was a name.  
  
Implemented a basic webscraping script within *article-handler.py* and tested it by pulling the Great Gatsby from
gutenberg.org. File was successfully saved, however there appear to be artifacts within the text file, namely too many
newlines (\n) between lines in the text. Whether these will affect the NLP's ability to parse the text will be
investigated.  
  
Looked into webscraping artifacts further. The artifacts seem to a result of how gutenberg.org formats their html text. 
Scraping another sample website like the one found here: https://www.york.ac.uk/teaching/cws/wws/webpage1.html result in
reasonably formatted text file. However, the artifacts found from scraping from gutenberg.org do pose a noticeable
in how the NLP processes the text. See *test_webscrape_against_file* for more details.  
  
<u>2021-03-31</u>: Completely overhauled input parsing behavior to clean up the rather ugly if-else nest in main 
function call. Flag parsing is now abstracting behind smaller functions that can be called used a dictionary + 
function pointers. This also means that new flags can be added much easier. After main console interface was 
rewritten, I created a comprehensive test document to test the base and edge cases of the user interface, outlined in 
*ner_fuhrer Interface Tests* report.  
  
Further cleaned up code and documentation for delivery. Currently encountering an error when trying to download the 
accurate, _trf pipelines from spaCy. The error seems to be a result of a missing *caffe2* package in my python 
interpreter. Investigating ways to resolve the error, but the -a flag will have to be untested until it is resolved.
## Test Log
### Unit Tests  
Note: scaPy tends to cause unittests to raise ResourceWarnings; these do not hamper the tests' accuracy 
and my be ignored for this project's purposes.  
#### test_simple_text  
<u>Overview</u>:  
Performs a simple test with prewritten sentences testing spaPy's model's ability to parse and detect
proper nouns. The sentences are designed so that not all capitalized nouns are proper nouns, so the
model must be able to distinguish these as a baseline.  
<u>Results</u>:  
Model's returned list matched the expected list.  
<u>Conclusion</u>:  
scaPy model should be sufficiently accurate to use for this project. Further accuracy testing will be
conducted, though.
#### test_simple_german_text
<u>Overview</u>:  
Performs a simple test similar to that of *test_simple_text* that evaluates the spaCy German NLP model's
ability to parse through and identify proper nouns within a German text. German was selected for this
multi-language evaluation test because German is my most familiar non-English language and because all German nouns
(except for pronouns) are capitalized. This means the the model must classify based on sentence context
alone.  
<u>Results</u>:  
Model's returned list matched the expected list. It's noteworthy that the model was able to correctly classify "Mauern"
as a common noun and "Mauer", which in the context of the sentence is a name, as a proper noun.  
<u>Conclusion</u>:  
spaCy's German model performed exceptionally against a test set designed to trick it and despite German's inherit
complexity when trying to classify proper nouns.
#### test_accuracy
<u>Overview</u>:  
Performs a more rigorous accuracy test, using a larger text and longer list of expected proper nouns. Text
parsed is the Emancipation Proclamation, as it contains a large set of proper nouns. Expected list of proper nouns
was compiled by myself, so to accommodate for the possibility of error - both human and by the NLP model - this test
evaluates and accuracy score and lists which tokens were expected, but not found, and which were found, but not expected.  
<u>Results</u>:  
Model-against-human accuracy of **93%**
> Expected tokens that were not identified by NER:  
> Commander-in-Chief  
> LINCOLN  
> Found tokens that were not expected:  
> Chief  
> A  
> Whereas  

<u>Conclusion</u>:  
Model is sufficiently accurate for this project. Some notable areas of struggle are with hyphenated titles, in this
example "Commander-in-Chief". This means that spaCy divides these tokens up into separate tokens, ex.
"Commander", "in", "Chief". The model also incorrectly labeled "A" and "Whereas" as proper nouns. This likely suggests
that the model struggles with handling the formatting of document titles and with less casual speech respectively.  
#### test_parse_behavior  
<u>Overview:</u>  
Ensures the 'chunking' behavior in *article_handler.py* operates as expected and preserves sentences/words in the 
chunks. Reads for a test text file, test-parse-behavior.txt which contains sentences/words that are smaller than the 
chunk size, thus requiring some of the next chunk/word to be cropped and moved to the next word.  
<u>Results:</u>  
Returned chunks successfully preserved sentence structure and matched expected output.  
<u>Conclusion:</u>  
This method of breaking up text files into more managable chunks successfully preserves sentence structure and thus 
should not interfere with NLP parsing behavior.
#### test_parse_timing
<u>Overview</u>:  
Compares the time it takes for the model to parse through a large text, Moby Dick, between different 
text retrieval methods. These methods are, in order: line-by-line, 1024B chunk, and 4092B chunk.  
<u>Results</u>:  
Line-by-Line:~127 seconds || 1024B Chunk: ~44 seconds || 4092B Chunk: ~42 seconds  
<u>Conclusion</u>:  
Using chunk-based approach is significantly faster in parsing large texts than line-by-line.
#### test_webscraper  
<u>Overview</u>:  
Tests if using requests+BeautifulSoup libraries can sufficiently pull text from a given website. Decided to scrape from 
a almost purely text website, gutenberg.org's Great Gatsby webpage.  
<u>Results</u>:  
Webscraping libraries successfully extracted html file it's text from the given url. However, the text document contains 
artifacts that are a result of how gutenberg.org structures their sites. Specifically, these artifacts are unusual line 
spacing that isn't apparant on the site.  
  
Text from *great-gatsby.txt* - Webscraped from gutenberg.org | Note: line numbers were added for clarity.  
>Line #>  
> ...  
>6812> VIII  
>6813>   
>6814>  
>6815> I couldn’t sleep all night; a foghorn was groaning incessantly on the Sound,...  
>6816>  
>6817>  
>6818>  
>6819>  
>6820> Crossing his lawn, I saw that his front door was still open and he was leaning...  
>6821>  
>6822>  
>...  
> 
Text as it roughly appears on gutenberg.org  
>VIII  
> 
>I couldn’t sleep all night; a foghorn was groaning incessantly on the Sound, and I tossed half-sick between grotesque 
>reality and savage, frightening dreams. Toward dawn I heard a taxi go up Gatsby’s drive, and immediately I jumped out 
>of bed and began to dress—I felt that I had something to tell him, something to warn him about, and morning would be
> too late.   
>Crossing his lawn, I saw that his front door was still open and he was leaning against a table in the hall, heavy with
>dejection or sleep. 
> 
<u>Conclusion</u>:  
Webscraping did successfully pull text from website, and running the test on similar websites did not yield the same 
line spacing artifacts. However, as seen in *tests_webparsing_against_file* these artifacts do somewhat impact the NLP's 
ability to parse the test file. This can likely be resolved by developing a way to go through webscraped text and remove 
any excessive line spacing, however if this problem is unique to gutenberg.org and only causes a 5% inconsistency 
against text files without the artifacts, then it should not be a priority.  
#### test_webscraper_against_file  
<u>Overview</u>:  
Test to address concerns whether the artifacts found from scraping text from gutenberg.org in *test_webscraping* would 
impact NLP performance in anyway. Test compares how NLP performs on a webscraped version that contains line-spacing
artifacts against a file that was copy and pasted from the website and does not contain spacing artifacts. Differences 
in the Named Entities both classify are counted and scored to evaluate how different/accurate the version with artifacts 
is against the one without. An arbitrary accuracy goal of 95% was set.  
<u>Results</u>:  
Test failed. Accuracy was just below the threshold with a score of 94.89%. Interestingly most of the named entities that 
are exlusive to one version or the other aren't proper nouns. Tokens like "ye,'-he" and "down-"What" were inconsistently 
labeled as Named Entities. It seems that these uncommon punctuations in tandem with the unusual line-spacing is creating the 
inconsistent results between versions.  
<u>Conclusion</u>:  
This means that the line-spacing artifacts do, to a degree, impact the performance of the NLP model. Since most of the 
inconsistently labeled Named Entities are also incorrectly labeled  Named Entities, perhaps using (or giving the user 
the option to use) the more accurate, but less efficient NLP models, like "en_core_web_trf", may be worthwhile and 
merits investigation.  
## Future Changes  
- ~~Implement dictionaries within *ner_fuhrer*, so user doesn't have to know spaCy specific syntax like 
"en_core_web_sm" or "PROPN".~~ ✓
- ~~Do more rigorous testing on spaCy. Get a rough estimate for how accurately its models can identify
proper nouns.~~ ✓
- ~~Implement language and part-of-speech flags within *ner_fuhrer*.~~ ✓
- ~~Add German language core and test against a example German text.~~ ✓
- ~~Add website scraping capabilites to convert a website into a readable text file.~~ ✓
- ~~Investigate cython and see if it's possible to compile Grier-NER into an executable with dependencies baked in. -OR- 
  Investigate setuptools Python library to create a dependency install script.~~ ✓
- ~~Add a flag that will allow the user to save the console output to a file.~~ ✓
- ~~Add a flag that will allow the user to specify whether they wish to use the efficient or accurate version of each
  langauge model.~~ ✓
- Replace SortedList with a custom sorted list that uses binary search/insert to remove dependency on sortedcontainers
and likely improve computation time. (Low priority)
- ~~Clean up input parsing behavior in *ner_fuhrer.py* for readability.~~