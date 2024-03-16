# 2)trainingNB.py:
    # NB stands for Naive Bayes
    # this is using the training data to calculate the prior and likelihoods
    # Save the calculated probabilities, out model in model.csv

import pandas as pd
import numpy as np
import csv
import random

# nltk word tokenzier to tokenize the statemnts
from nltk.tokenize import word_tokenize

# Reading the trainging data set
training_data = pd.read_csv('train.csv')

# Lets do some preprcessing on the data
# Conver sentence to words
training_data['Text'] = training_data['Text'].apply(word_tokenize)

# Convert the words to lower case
training_data['Text'] = training_data['Text'].apply(lambda x: [word.lower() for word in x])
# print(training_data.head())

# Create a global vocab set
# this will be helpful incase of 0 probabilities
# we can add some smoothing to avoid zero probabilities
vocab = set()

# dict for prior and likelihoods
priors = {}
likelihoods = {}

# Lets calculate the prior and likelihoods
# Finding all the unique classes in the data
# Even when i know the classes, just so that the program remains more modular
all_classes = training_data['Category'].unique()
for c in all_classes:
    priors[c] = 0
    likelihoods[c] = {}

# Lets calculate the counts first
for text, category in zip(training_data['Text'], training_data['Category']):

    # for every instance of class found we increment the prior for that class
    priors[category] += 1

    # for every word in the text we increment the likelihood for that class
    for word in text:
        vocab.add(word)

        # if the word is not in the likelihoods dict, we add it
        if word not in likelihoods[category]:
            likelihoods[category][word] = 0

        # increment the count for the word in the likelihoods dict
        likelihoods[category][word] += 1

print(priors, likelihoods)


# Lets calculate the probabilities
# Prior
# P(c) = count(c) / count(all_classes)
for c in priors:
    priors[c] = priors[c] / len(training_data)

# Likelihood
# P(w|c) = count(w, c) / count(c)
# We will need total words in each class

total_words = {}
for class_name in priors.keys():
    count = 0
    for word in likelihoods[class_name]:
        count += likelihoods[class_name][word]
    total_words[class_name] = count


# # we can add some smoothing to avoid zero probabilities
# P(w|c) = (count(w, c) + 1) / (count(c) + |V|)

# for all classes in the priors
for word in vocab:
    for class_name in priors.keys():
        likelihoods[class_name][word] = (likelihoods[class_name].get(word, 0) + 1) / (total_words[class_name] + len(vocab))


print(priors, likelihoods)

model_csv = 'model.csv'

# Saving model to csv
with open(model_csv, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Category', 'Word', 'Likelihood', 'Prior'])

    # Iterate over each class to write its data
    for class_name in priors.keys():
        for word in vocab:
            # For each word, write a row with the class, word, word's likelihood, and class's prior
            # If the word is not in the likelihoods dict, we define its likelihood as 0 in that class
            # This way all the words in the vocab have probabilities assigned for both classes
            likelihood = likelihoods[class_name].get(word, 0)
            writer.writerow([class_name, word, likelihood, priors[class_name]])


# This will save the model to model.csv
