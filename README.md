# Grier-NER
Grier-NER is a Python Named Entity Recognition (NER) project for 
Grier Forensics 2021 Intern Software Engineer coding challenge.
### Project Info
Author: Michael Fuhrer, mfuhrer@vt.edu  
Created: March 23, 2021 | Deadline: April 2, 2021
## Dependencies
#### <u>spaCy</u>
Grier-NER uses spaCy, an open-source natural language processing
library created by Matthew Honnibal. spaCy was selected to use
in this project because it matches expectations and criteria laid out in
problem description; it's open-source, can operate offline, and is relatively
easy to implement. Before running Grier-NER please install the spaCy python library using:
>pip install spacy
>
More detailed installation instructions may be found here: https://spacy.io/usage.
Once spaCy is installed, please also download its core english pipeline:
>python -m spacy download en_core_web_sm
> 
You may download additional language pipelines detailed here: https://spacy.io/usage/models  
I plan ([TODO]) to include tests that also use the German pipeline, de_core_news_sm.  
#### <u>sortedcontainers</u>  
Used for its SortedSet class, which is used to uniquely catalog and alphabetically organize
the tokens of the desired part-of-speech within the given text.
>pip install sortedcontainers
> 

## Usage
[TODO]
## Process Log
Contains a chronological list of steps and decisions taken while developing this project.  
  
<u>2021-03-23:</u> Project start. Did general research on NER and NPL, found an open-source NPL
library (spaCy) that closely matched project requirements and criteria. Created rough skeleton
of project code and started formatting files. Began following spaCy tutorial @ 
https://spacy.io/usage/spacy-101 to better understand how to use library.    

<u>2021-03-28</u>: Experimented with parsing text files using spaCy, as the NPL model has a limit 
on the size of text it can accept. Developed a system to subdivide text into lines, so that NPL 
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
## Test Log  
Note: scaPy tends to cause unittests to raise ResourceWarnings; these do not hamper the tests' accuracy 
and my be ignored for this project's purposes.  
#### test_simple_text  
<u>Overview</u>  
Performs a simple test with prewritten sentences testing spaPy's model's ability to parse and detect
proper nouns. The sentences are designed so that not all capitalized nouns are proper nouns, so the
model must be able to distinguish these as a baseline.  
<u>Results</u>  
Model's returned list matched the expected list.  
<u>Conclusion</u>  
scaPy model should be sufficiently accurate to use for this project. Further accuracy testing will be
conducted, though.
#### test_accuracy
<u>Overview</u>  
Performs a more rigorous accuracy test, using a larger text and longer list of expected proper nouns. Text
parsed is the Emancipation Proclamation, as it contains a large set of proper nouns. Expected list of proper nouns
was compiled by myself, so to accodate for the possibility of error - both human and by the NPL model - this test
evaluates and accuracy score and lists which tokens were expected, but not found, and which were found, but not expected.  
<u>Results</u>  
Model-against-human accuracy of **93%**
> Expected tokens that were not identified by NER:  
> Commander-in-Chief  
> LINCOLN  
> Found tokens that were not expected:  
> Chief  
> A  
> Whereas  

<u>Conclusion</u>  
Model is sufficiently accurate for this project. Some notable areas of struggle are with hyphenated titles, in this
example "Commander-in-Chief". This means that spaCy divides these tokens up into separate tokens, ex.
"Commander", "in", "Chief". The model also incorrectly labeled "A" and "Whereas" as proper nouns. This likely suggests
that the model struggles with handling the formatting of document titles and with less casual speech respectively.
#### test_parse_timing
<u>Overview</u>  
Compares the time it takes for the model to parse through a large text, Moby Dick, between different 
text retrieval methods. These methods are, in order: line-by-line, 1024B chunk, and 4092B chunk.  
<u>Results</u>  
Line-by-Line:~127 seconds || 1024B Chunk: ~44 seconds || 4092B Chunk: ~42 seconds  
<u>Conclusion</u>  
Using chunk-based approach is significantly faster in parsing large texts than line-by-line.
## Future Changes  
- ~~Implement dictionaries within *ner_fuhrer*, so user doesn't have to know spaCy specific syntax like 
"en_core_web_sm" or "PROPN".~~ ✓
- ~~Do more rigorous testing on spaCy. Get a rough estimate for how accurately its models can identify
proper nouns.~~ ✓
- ~~Implement language and part-of-speech flags within *ner_fuhrer*.~~ ✓
- Add German language core and test against a example German text.
- Add website scraping capabilites to convert a website into a readable text file.
- Investigate cython and see if it's possible to compile Grier-NER into an executable with dependencies baked in.