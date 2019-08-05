# Import the English language class and create the nlp object
from spacy.lang.en import English
from spacy.lang.th import Thai
import spacy

'''
nlp = English()

# Process the text
doc = nlp("I like tree kangaroos and narwhals.")

# Select the first token
first_token = doc[2]

# Print the first token's text
print(first_token.text)

# Process the text
doc = nlp("In 1990, more than 60% of people in East Asia were in extreme poverty. Now less than 4% are.")

# Iterate over the tokens in the doc
for token in doc:
    # Check if the token resembles a number
    if token.like_num:
        # Get the next token in the document
        next_token = doc[token.i + 1]
        # Check if the next token's text equals '%'
        if next_token.text == '%':
          print('Percentage found:', token.text)


# Load the small English model – spaCy is already imported
nlp = spacy.load('en_core_web_sm')

text = "It’s official: Apple is the first U.S. public company to reach a $1 trillion market value"

# Process the text
doc = nlp(text)

for token in doc:
    # Get the token text, part-of-speech tag and dependency label
    token_text = token.text
    token_pos = token.pos_
    token_dep = token.dep_
    # This is for formatting only
    print('{:<12}{:<10}{:<10}'.format(token_text, token_pos, token_dep))
'''
nlp=Thai()

#th_nlp = spacy.load('th')
text="คุณรักผมไหม"
a=nlp(text)
#a= th_nlp(text)
# Select the first token
first_token = a[2]
print(first_token.text)
# Print the first token's text
print(a.text)