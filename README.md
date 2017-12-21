# Part-of-Speech-Tagger

## Summary
This English Part of Speech Tagger is based on Viterbi Hidden Markov Model. The program takes a corpus that is preformatted with tokenized sentences. Each word and its corresponding part of speech are on one line. After that, the model will take another preformatted corpus of tokenized sentences, with each word being on its own line. The system will then use Viterbi Hidden Markov Model chains to find the part of speech of each word. To run the system, it needs three arguements, the first is the training corpus in a text file, the second is the corpus being worked on in a text file, and the third is an empty file the system will write to. The system deals with unknown words by using phonological rules. The system does not use any outstanding libraries. 
