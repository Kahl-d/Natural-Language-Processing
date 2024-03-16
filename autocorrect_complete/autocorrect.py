import re
from collections import Counter
from Levenshtein import distance

##################################################
# Part 1

def main():

# specifying courpus path
# in this case : Web Text Corpus, Pirates of the Carribean, Dead Man's Chest Script

    file_path = 'webtext/pirates.txt'

# Open the file in read mode
    with open(file_path, 'r', errors='ignore') as file:

        vocabulary_content = file.read()


# checking content
#     print(vocabulary_content)

# converting to lower case
# for cases like The - the and Jack - jack
# to make the program be case sensitive

    vocabulary_content = vocabulary_content.lower()

    # print(vocabulary_content)


# Using regex to extract words from the corpus
# as all content is in lower case a-z
# for words like can't, dont regex function will include \'

    pattern = re.compile(r'\b[a-z\']+\b')


# getting all the words in the mathc object
    match = re.findall(pattern, vocabulary_content)

# The length of the match object gives the total number of Words in the corpus
    total_token = len(match)
    print('Total word Tokens: ', total_token)

##################################################
# Part 2

# finding unique words and their frequency
# using python counter on all token list


# Printing unique types
    types = Counter(match)
    print('Unique Types Count: ', len(types))


##################################################
# Part 3

# Calculating the likelihood of each word in the corpus
# The frequency of the word is divided by the toatl number of words
# This gives relative probability

    relative_freq = {}
    for word, freq in types.items():
        relative_freq[word] = (freq/total_token)

    # print(relative_freq)


##################################################
# Part 4

# taking user input
    w = input('Enter word: ')
    w = w.lower()
    relative_dist = {}

# checking if word is in our vocabulary
    try:
        # if found in vocabulary
        # print(relative_freq[w])
        print(f'{w} is a complete and correct word as per corpus: Pirates of the Carribean, Dead Mans Chest Script, and its probability is {relative_freq[w]}')
    except KeyError:
        # if not found

        # Calculate Levenshtein distance for the input word with each type in count
        for word, count in types.items():

            relative_dist[word] = (distance(w, word), relative_freq[word])

        # print(relative_dist)


###################################################
        # Getting Top Words
        # First the list of word with are sorted based on Levenshtein distance - in ascending order
        # Min distance first

        # Then in the same lev distance, the words are sorted based on their relative probability
        # Within the same lev distance, words are sorted in descending order of probability,
        # as with the same minimum edit distance, words with more realtive probability are more likely to occur


        sort = []
        i = 0

        # untill all words are sorted
        while len(sort) < len(types):
            # Getting words with same lev distance
            this_lev_dist = [(key, value) for key, value in relative_dist.items() if value[0] == i]

            # sorting them based on the relative probability
            sorted_sort = sorted(this_lev_dist, key=lambda item: -item[1][1])

            # appending sorted list to main array
            sort.extend(sorted_sort)

            # incrementing for the next lev distance
            i = i +1



        top_5 = sort[:5]

# printing top 5 words

        print('WORD', '\t', "L. Distance", '\t', 'Probability')
        for word, count in top_5:
            print(word, '\t', count[0], '\t\t', count[1])



if __name__ == '__main__':
    main()