CSC 820 Natural Language Processing
HW #6 Implementing Naive Bayes Classifier

Khalid Mehtab Khan
SFSU ID: 923673423
date: 03/13/2024

Fact Checking with Naive Bayes
A statement can be classified into two categories, facts and opinions.
Based on the words used when someone is speaking, we can determine if the statement is a fact or an opinion.
In this homework, I have implemented a Naive Bayes classifier to classify statements as facts or opinions.
We will use the 50 sampled facts and opinions labeled dataset to train and test our classifier.

Files:
(The files are in order of their use in the program)
To run the program from the start.
delete all CSV files.
Run the Python files in the following order.
1) dataset_process.py
2) trainingNB.py
3) testingNB.py

Once completed these will be the list of files on the directory.

1) data_process.py:
    - This file contains the raw data of 50 data points.
    - This also contains the code to sample random data and split it into training and testing data.
    - After sampling, 20% of the data is used for testing and 80% is used for training.
    - The file saves the training and testing data in two separate files called "train.csv" and "test.csv".

2) train.csv:
    - This file contains the training data and category labels.
    - It contains 40 data points.

3) trainingNB.py:
    - This file contains the code to train the Naive Bayes classifier.
    - It also contains the code to calculate the prior and conditional probabilities.
    - Once all the probabilities are calculated, it saves the probabilities in a file called "model.csv".

4) model.csv:
    - This file contains the prior and conditional probabilities of the words in the training data.

5) test.csv:
    - This file contains the testing data and category labels.
    - It contains 10 data points.

6) testingNB.py:
    - The file contains the code to test the Naive Bayes classifier.
    - The file reads all the statements from the test data,
    - calculates the probability of each statement being a fact or an opinion,
    - and then classifies the statement as a fact or an opinion.
    - The files save the results in a file called "test_predicted.csv".

7) test_predicted.csv:
    - This file contains the test data and the predicted category labels.
    - It contains the true value and the predicted value for each statement in the test data.
    - It contains how much probability each class had for the given sentence.
