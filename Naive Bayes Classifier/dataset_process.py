# Description: This file is used to process the dataset and convert it into a format that can be used by the model.

# Importing the required libraries
import pandas as pd
import numpy as np
import csv
import random


# A dataset of 50 sentences, each labeled as either a fact or an opinion:
# Each item in the data set is a tuple with two elements:
    # The first element is a sentence
    # The second element is the label for that sentence

dataset = [
    ("The Eiffel Tower is located in Paris.", "fact"),
    ("Chocolate is the best ice cream flavor.", "opinion"),
    ("Water boils at 100 degrees Celsius at sea level.", "fact"),
    ("Summer is better than winter.", "opinion"),
    ("The heart pumps blood through the body.", "fact"),
    ("Cats make better pets than dogs.", "opinion"),
    ("The Pacific Ocean is the largest ocean on Earth.", "fact"),
    ("Reading books is more enjoyable than watching movies.", "opinion"),
    ("Light travels faster than sound.", "fact"),
    ("Pizza is a healthier food option than salads.", "opinion"),
    ("Mount Everest is the highest mountain in the world.", "fact"),
    ("Video games are a waste of time.", "opinion"),
    ("Photosynthesis is the process by which plants make their food.", "fact"),
    ("Nothing beats a beach vacation.", "opinion"),
    ("The human skeleton is made up of less than 206 bones.", "fact"),
    ("Social media platforms improve personal relationships.", "opinion"),
    ("The Great Wall of China is visible from space.", "fact"),
    ("Life is too short to learn German.", "opinion"),
    ("The speed of light in a vacuum is 299,792 kilometers per second.", "fact"),
    ("Tea is more refreshing than coffee.", "opinion"),
    ("Venus is the second planet from the Sun.", "fact"),
    ("All natural disasters are preventable.", "opinion"),
    ("Alexander Hamilton was the first U.S. Secretary of the Treasury.", "fact"),
    ("You can't be happy without money.", "opinion"),
    ("The human body has four blood types: A, B, AB, and O.", "fact"),
    ("Real art requires real talent.", "opinion"),
    ("Sharks are older than trees in terms of species history.", "fact"),
    ("Traveling by plane is more dangerous than by car.", "opinion"),
    ("Bees can recognize human faces.", "fact"),
    ("The Internet has only made people more isolated.", "opinion"),
    ("Pluto is still considered a planet in our solar system.", "fact"),
    ("Modern art isn’t real art.", "opinion"),
    ("The Amazon rainforest produces 20% of the world's oxygen.", "fact"),
    ("A college degree guarantees a successful career.", "opinion"),
    ("The Great Pyramid of Giza was built by slaves.", "fact"),
    ("True love lasts forever.", "opinion"),
    ("Bats are blind.", "fact"),
    ("Autumn is the most beautiful season.", "opinion"),
    ("DNA is the blueprint for every living thing.", "fact"),
    ("Age is just a number in relationships.", "opinion"),
    ("There are more cells of bacteria in your body than human cells.", "fact"),
    ("Money can buy happiness.", "opinion"),
    ("Antarctica is the driest continent on Earth.", "fact"),
    ("Beauty is in the eye of the beholder.", "opinion"),
    ("The universe is constantly expanding.", "fact"),
    ("Children learn better through play than strict education.", "opinion"),
    ("Oxygen is the most abundant element in the Earth's crust.", "fact"),
    ("People can change if they really want to.", "opinion"),
    ("Viruses can be treated with antibiotics.", "fact"),
    ("Wisdom comes only with age.", "opinion")
]


# Picking random samples from the dataset to create the test and train data
random.seed(112)
dataset_size = len(dataset)
test_size = int(dataset_size * 0.2)

test_data = random.sample(dataset, test_size)

# The remaining data will be used as training data
# Filter out test_data samples to create the train_data
train_data = [item for item in dataset if item not in test_data]

# CSV files will be created from the test and train data
test_csv = 'test.csv'
train_csv = 'train.csv'


# Saving in to CSV files
with open(test_csv, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)

        # adding columns for the data frame
        writer.writerow(["Text", "Category"])
        writer.writerows(test_data)

with open(train_csv, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerow(["Text", "Category"])
        writer.writerows(train_data)


# Checking if the CSV files are working
# Read the test CSV file
test_df = pd.read_csv('test.csv')
print("Test CSV:")
print(test_df)

# Read the train CSV file
train_df = pd.read_csv('train.csv')
print("Train CSV:")
print(train_df)
