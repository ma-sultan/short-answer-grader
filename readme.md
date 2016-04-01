# A Short Answer Grader

This is an automatic short answer grading system written in Python. Given a question, a correct reference answer and a student response, it computes a real-valued score for the student response based on its semantic similarity with the correct answer. This is the grader reported in the NAACL 2016 short paper **Fast and Easy Short Answer Grading with High Accuracy** (except the term weighting-based features). The directory contains a pretrained grader (pretrainedGrader.py) as well as source code for training a new one (trainAndApplyGrader.py). Each source file contains an actual example of grading a student response.

## Requirements

1) NLTK
2) Scikit-learn
3) The [Python wrapper for Stanford CoreNLP](https://github.com/dasmith/stanford-corenlp-python)

## Installation and Usage
1) Make sure the requirements are installed.
2) Change the statement "rel, left, right = map(lambda x: remove_id(x), split_entry)" in **corenlp.py** to "rel, left, right = split_entry".
3) Download the grader:  

	  git clone https://github.com/ma-sultan/short-answer-grader
4) Download the word embeddings by Baroni, Dinu, and Kruszewski from [this link](http://clic.cimec.unitn.it/composes/semantic-vectors.html) (the "Best predict vectors") and put the file in the Resources directory.
5) Run the **corenlp.py** script to launch the server:  

	  python corenlp.py
6) To run the pretrained grader, run **pretrainedGrader.py**.
7) To train a new grader and apply to a test item, run **trainAndApplyGrader.py**.
