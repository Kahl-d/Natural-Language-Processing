import nltk

# Ensure punkt is downloaded, which is a dependency for webtext
nltk.download('punkt')

# Import webtext
from nltk.corpus import webtext

# Access the raw text of "pirates.txt"
pirates_text = webtext.raw('pirates.txt')

# Example usage
print(pirates_text[:500])  # Print the first 500 characters of the script
