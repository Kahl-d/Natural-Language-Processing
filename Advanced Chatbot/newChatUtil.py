# Natural Language Toolkit: Chatbot Utilities
#
# Copyright (C) 2001-2023 NLTK Project
# Authors: Steven Bird <stevenbird1@gmail.com>
# URL: <https://www.nltk.org/>
# For license information, see LICENSE.TXT

# Based on an Eliza implementation by Joe Strout <joe@strout.net>,
# Jeff Epler <jepler@inetnebr.com> and Jez Higgins <jez@jezuk.co.uk>.

import random
import re


# Set the SSL certificate path
# ssl._create_default_https_context = ssl._create_unverified_context

# Download NLTK data
import nltk
from nltk.stem import PorterStemmer
from nltk import word_tokenize

reflections = {
    "i am": "you are",
    "i was": "you were",
    "i": "you",
    "i'm": "you are",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "my": "your",
    "you are": "I am",
    "you were": "I was",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine",
    "you": "me",
    "me": "you",
}


class Chat:
    def __init__(self, pairs, reflections={}):
        """
        Initialize the chatbot.  Pairs is a list of patterns and responses.  Each
        pattern is a regular expression matching the user's statement or question,
        e.g. r'I like (.*)'.  For each such pattern a list of possible responses
        is given, e.g. ['Why do you like %1', 'Did you ever dislike %1'].  Material
        which is matched by parenthesized sections of the patterns (e.g. .*) is mapped to
        the numbered positions in the responses, e.g. %1.

        :type pairs: list of tuple
        :param pairs: The patterns and responses
        :type reflections: dict
        :param reflections: A mapping between first and second person expressions
        :rtype: None
        """

        self._pairs = [(re.compile(x, re.IGNORECASE), y) for (x, y) in pairs]
        self._reflections = reflections
        self._regex = self._compile_reflections()

    ###################################################################################################

    # this is a custom function for CSC 820 Assignment 2
    # the function uses : nltk word_tokenizer
    # and Porter Stemmer
    def tokenizer_and_stemmer_function(self, response) -> str:
        # print(response)

        # creating instance of porter stemmer
        ps = PorterStemmer()

        # List of tokenized words
        words = word_tokenize(response)
        # print('Tokenized words')
        # print('NLTK tokenizer :')
        # print(words)


        stemmed_words = []

        # Stemming each token
        for word in words:
            stemmed_words.append(ps.stem(word))
            # print(ps.stem(word) , '\n')

        # Reforming the setnence from tokenized words
        retString = ' '.join(stemmed_words)

        print('Stemmed Sentence:', retString)

        # Passing stemmed string to inhouse Tokenizer
        # For Types and Token

        self.custom_regex_tokenizer(retString)

        # returning processed string to ELIZA program
        return retString


    def custom_regex_tokenizer(self, str):

        # print(str)
        regex_pattern = re.compile(r'\b[a-zA-Z0-9\']+\b')

        tokens = regex_pattern.findall(str)
        print('Tokens: ', len(tokens))
        print(tokens)

        # as all words are in lower case after stemming
        # creating a set would get the unique words for the types
        types = set(tokens)
        print('Types: ', len(types))
        print(types)

##########################################################################################

    def _compile_reflections(self):
        sorted_refl = sorted(self._reflections, key=len, reverse=True)
        return re.compile(
            r"\b({})\b".format("|".join(map(re.escape, sorted_refl))), re.IGNORECASE
        )

    def _substitute(self, str):
        """
        Substitute words in the string, according to the specified reflections,
        e.g. "I'm" -> "you are"

        :type str: str
        :param str: The string to be mapped
        :rtype: str
        """

        return self._regex.sub(
            lambda mo: self._reflections[mo.string[mo.start() : mo.end()]], str.lower()
        )

    def _wildcards(self, response, match):
        pos = response.find("%")
        while pos >= 0:
            num = int(response[pos + 1 : pos + 2])
            response = (
                response[:pos]
                + self._substitute(match.group(num))
                + response[pos + 2 :]
            )
            pos = response.find("%")
        return response

    def respond(self, str):

        #### Calling the stemmer function to get processed string

        processed_str = self.tokenizer_and_stemmer_function(str)


        # check each pattern
        for pattern, response in self._pairs:

            match = pattern.match(processed_str)

            # did the pattern match?
            if match:
                resp = random.choice(response)  # pick a random response
                resp = self._wildcards(resp, match)  # process wildcards

                # fix munged punctuation at the end
                if resp[-2:] == "?.":
                    resp = resp[:-2] + "."
                if resp[-2:] == "??":
                    resp = resp[:-2] + "?"
                return resp

    # Hold a conversation with a chatbot
    def converse(self, quit="quit"):
        user_input = ""
        while user_input != quit:
            user_input = quit
            try:
                user_input = input(">")
            except EOFError:
                print(user_input)
            if user_input:
                while user_input[-1] in "!.":
                    user_input = user_input[:-1]
                print(self.respond(user_input))