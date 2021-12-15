# A very crude sengence segementer and tokenizer. 

import re

# Matches everything before a period, question mark, or exclamation mark. 
sentence_regex = re.compile(r'(\S(?:.+?)[\.\?!]+)')

# Matches either a sequence of word characters or a punctuation mark
token_regex = re.compile(r'(\w+|[“”":;\'-\.\?!,]+)', re.UNICODE)

# Matches a sequence of alphabetic characters
word_regex = re.compile(r'(\w+)', re.UNICODE)

def sentence_segment(text):
    """Returns a list containing the argument text broken up into sentences. 
    Uses sentence_regex to look for sentences.
    """
    return list(sentence_regex.findall(text))

def tokenize(text, punctuation = True):
    """Returns a list of tokens for each sentence in the 
    text passed as argument. Punctuation marks are considered tokens if 
    punctuation == True, or deleted if False. At present, this tokenizer 
    doesn't take named entities into account or employ any normalization other 
    than case folding."""

    sentence_list = sentence_segment(text)

    # This will contain a list for each sentence to be tokenized
    token_list = []
    
    for sentence in sentence_list:
        if punctuation == True:
            token_list.append(token_regex.findall(sentence))
        else:
            token_list.append(word_regex.findall(sentence))
    
    # Case fold all words to lowercase
    for each_list in token_list:
        for i, word in enumerate(each_list):
            if word.isupper() or word.istitle():
                each_list[i] = word.lower()

    return token_list
