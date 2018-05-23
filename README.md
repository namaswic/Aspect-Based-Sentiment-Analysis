# Aspect-Based-Sentimental-Analysis
#CS583 DATA MINING AND TEXT MINING  
#Authors-Namaswi Chandarana(nchand22@uic.edu),Vanisre Jaiswal(vjaisw2@uic.edu)  
Our Task: Given an aspect term (also called opinion target) in a sentence, predict the sentiment label for the aspect term in the sentence. 

The description of each column is as fellows:
Column A: review sentence id
Column B: review sentence
Column C: aspect term in the sentence
Column D: aspect term location
Column E: sentiment label

Typical Workflow:  
1. Pre-process the data files  to normalize the data.
2. Build classifier model.
3. Evaluate the performance of the classifier model and report results.

Evaluation:
1. Results are generated via 10-fold cross validation. 
2. Computed following metrics by taking average over 10 folds-
Accuracy and avg. precision, avg. recall and avg. F1 scores for each of the three classes- { positive, negative, neutral } and for each of the two training dataset {data_1, data_2}.

 


 
