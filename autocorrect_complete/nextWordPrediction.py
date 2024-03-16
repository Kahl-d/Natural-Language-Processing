import nltk
from nltk import bigrams
from nltk.probability import FreqDist, MLEProbDist
import re

from collections import Counter

file_path = 'webtext/pirates.txt'

# Open the file in read mode
with open(file_path, 'r', errors='ignore') as file:
    corpus = file.read()

sample_text = "I don't live in San Francisco live are city of California live in."
sample_text = sample_text.lower()

pattern = re.compile(r'\b[a-z\']+\b')


# getting all the words in the mathc object
match = re.findall(pattern, sample_text)

# The length of the match object gives the total number of Words in the corpus
total_token = len(match)
print('Total word Tokens: ', total_token)

array = list(match)
print(array)


bigram_pairs = list(bigrams(array))
unique_bigrams = list(set(bigram_pairs))

# for word in bigram_pairs:
#     print(word)

bi_freq = FreqDist(bigram_pairs)

# print(bi_freq[bigram_pairs[2]])

bigram_probabilities = MLEProbDist(bi_freq)

inW = input("Enter the word")

possible_pairs = [bigram for bigram in unique_bigrams if bigram[0] == inW]

# print(possible_pairs) 


most_likely = sorted(possible_pairs, key=lambda x: bigram_probabilities.prob(x), reverse=True)


for pair in most_likely:
    print(pair[1], bigram_probabilities.prob(pair))


