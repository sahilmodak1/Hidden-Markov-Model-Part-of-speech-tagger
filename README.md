# Hidden-Markov-Model-Part-of-speech-tagger

This repository consists of python code implementation of Hidden Markov Model part-of-speech tagger for Catalan. The training data is tokenized and tagged and the test data is tokenized. This tagger will add the appropriate tags to the test data.


Data: There are 3 data files:

(1) A file with tagged training data in the word/TAG format, with words separated by spaces and each sentence on a new line. (catalan_corpus_train_tagged.txt)

(2) A file with untagged development data, with words separated by spaces and each sentence on a new line. (catalan_corpus_dev_raw.txt)

(3) A file with tagged development data in the word/TAG format, with words separated by spaces and each sentence on a new line, to serve as an answer key. (catalan_corpus_dev_tagged.txt)


Programs: There are 2 programs:

(1) hmmlearn.py will learn a hidden Markov model from the training data and write the model parameters to a file called hmmmodel.txt.

(2) hmmdecode.py will use the model to tag new data; the program will read the parameters of a hidden Markov model from the file hmmmodel.txt, tag each word in the test data, and write the results to a text file called hmmoutput.txt in the same format as the training data.

