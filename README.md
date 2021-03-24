# Grier-NER
Grier-NER is a Python Named Entity Recognition (NER) project for 
Grier Forensics 2021 Intern Software Engineer coding challenge.
### Project Info
Author: Michael Fuhrer, mfuhrer@vt.edu  
Created: March 23, 2021 | Deadline: April 2, 2021
## Dependencies
####<u>spaCy</u>
Grier-NER uses spaCy, an open-source natural language processing
library created by Matthew Honnibal. spaCy was selected to use
in this project because it matches expectations and criteria laid out in
problem description; it's open-source, can operate offline, and is
easy to implement. Before running Grier-NER please install the spaCy python library using:
>pip install spacy
>
More detailed installation instructions may be found here: https://spacy.io/usage.
Once spaCy is installed, please also download its core english pipeline:
>python -m spacy download en_core_web_sm
> 
You may download additional language pipelines detailed here: https://spacy.io/usage/models  
I plan ([TODO]) to include tests that also use the German pipeline, de_core_news_sm.
## Usage
[TODO]
## Process Log
Contains a chronological list of steps and decisions taken while developing this project.  
  
<u>2021-03-23:</u> Project start. Did general research on NER and NPL, found an open-source NPL
library (spaCy) that closely matched project requirements and criteria. Created rough skeleton
of project code and started formatting files. Began following spaCy tutorial @ 
https://spacy.io/usage/spacy-101 to better understand how to use library.