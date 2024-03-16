# 3)  testingNB.py:
    # We will use the model.csv file to test the model
    # All the remainining setnences will be tested against the model
    # The class with the highest probability will be the class of the sentence


# Import the necessary libraries
import pandas as pd
import numpy as np
import csv
import random

# nltk word tokenzier to tokenize the statemnts
from nltk.tokenize import word_tokenize


# Load the model
model = pd.read_csv('model.csv')
# print(model.head())

# Read the test.csv file
test_data = pd.read_csv('test.csv')


# get all class names from the model
all_classes = model['Category'].unique()


# Function to calculate the probability of a given class
# given a text, model and class name
def calc_prob_given_class(model, text, class_name):
    # Tokenize text
    words = word_tokenize(text.lower())

    # Initialize probability
    prob = 1
    row = model[(model['Category'] == class_name)]

    # Multiply the prior probability, P(c)
    prob = prob * row["Prior"].iloc[0]
    # Calculate the condiprobability

    # # check if the word exisst in our vocab
    for word in words:
        try:
        # if word is in the vocab, we can use the likelihood
        # we retrieve the row that corresponds the the particular class and word
        # and multiply the likelihood with the prior
        # we do this for all the words in the text
            row = model[(model['Category'] == class_name) & (model['Word'] == word)]
            prob = prob * row["Likelihood"].iloc[0]

    # if the word is not in the vocab, we can use a constant value
    # A small massaging to avoid zero probabilities for the sentence
    # This remains constant against all classes and unkonwn words
        except:
            prob = prob * 0.0001

    return prob



# Adding probability columns for each class to test_data
for c in all_classes:
    test_data[f'prob_{c}'] = np.nan

# Adding a column for predicted class to test_data
test_data['Predicted Class'] = ''

# Iterate over the test data to calculate probabilities to determine the predicted class
for index, row in test_data.iterrows():
    text = row['Text']
    max_prob = 0
    max_class = ''

   # for every sentence we caluclaute its probailty for all the classes in our nkowledge
    for c in all_classes:
        # get probabliilty using the get prob function
        prob = calc_prob_given_class(model, text, c)
        test_data.at[index, f'prob_{c}'] = prob

        # Decide the class with the highest probability
        # This will be the predicted class
        if prob > max_prob:
            max_prob = prob
            max_class = c

            #saving the predicted values
    test_data.at[index, 'Predicted Class'] = max_class  # Set the predicted class

# Now, let's print the DataFrame to verify
print(test_data)

# Save the updated DataFrame to a new CSV file
# This will be the final output
# The preicted results
predicted_csv_path = 'test_predicted.csv'
test_data.to_csv(predicted_csv_path, index=False)
