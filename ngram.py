# Contains functions to build ngram language models

import re
from tokenizer import tokenize
from random import choices
from math import log, exp 
from pathlib import Path
from copy import deepcopy

# Matches sentence end markers
endmarker_regex = re.compile(r'</s>')

def add_markers(n, token_list):
    """
    Adds n-1 sentence start <s> and end </s> markers to each sentence for 
    ngram processing.
    """    
    if n > 1:
        token_list = deepcopy(token_list)
        for i, sentence in enumerate(token_list):
            token_list[i] = (['<s>'] * (n-1)) + sentence + (['</s>'] * (n-1))
    
    return token_list

def ngram_count(n, token_list, markers=True):
    """
    Counts the ngrams in a list of tokens. Returns a dictionary in which 
    key-value pairs are, respectively, each ngram and how many times it appears
    in the list. The 'markers' parameter adds n-1 sentence start and end 
    markers to token_list (defaults to True)
    """

    if markers == True:
        token_list = add_markers(n, token_list)

    ngram_dict = {}

    for sentence in token_list:
        for i in range((n - 1), len(sentence)):
            # Look at last (i - m) words for concatenation
            pointer = i - (n - 1)
            # Form an ngram by concatenating last (i - (n-1)) words, up to i
            ngram = ''
            while pointer <= i: 
                ngram += sentence[pointer] + ' '
                pointer += 1
            # Strip trailing whitespace and add ngram to dict
            ngram = ngram.rstrip()
            ngram_dict.setdefault(ngram, 0)
            ngram_dict[ngram] += 1
    
    return ngram_dict

def get_vocab_size(token_list):
    """
    Returns the vocabulary size (number of unique words) of a token list
    """
    return len(ngram_count(1, token_list))

def get_token_count(token_list):
    """
    Returns the total number of tokens of a token list
    """
    token_count = 0
    for value in ngram_count(1, token_list).values():
        token_count += value

    return token_count

def ngram_prob(n, token_list):
    """
    Generates Maximum Likelihood Estimation probabilities of the ngrams present
    in a list of tokens. Returns a dictionary in which key-value pairs are,
    respectively, each ngram and its probability
    """    
    # This will contain the ngrams and their probabilities
    ngram_prob = {}

    # Add <s> and </s> markers
    token_list = add_markers(n, token_list)

    # Get the counts of ngrams of the same n passed as argument
    ngrams =  ngram_count(n, token_list, markers=False)
    # Get the count of lower-order ngram OR total number of tokens if n == 1
    if n > 1:
        lower_ngrams =  ngram_count(n - 1, token_list, markers=False)
    elif n == 1:
        lower_ngram_count = get_token_count(token_list)

    for key, count in ngrams.items():
        if n > 1:
            # Lower order ngram = current ngram minus its last word
            lower_ngram_key = key.rsplit(' ', 1)[0]
            lower_ngram_count = lower_ngrams[lower_ngram_key]
        ngram_prob.update({key: (count / lower_ngram_count)})
    
    return ngram_prob

def generate_unigrams(length, ngram_probs):
    """
    Genrates unigrams based on a dictionary of ngram probabilities.
    Length determines how many unigrams to generate"""
    sentence = ''
    next_unigram = ''

    keys = list(ngram_probs.keys())
    
    for _ in range(length):
        next_unigram = choices(keys, weights=ngram_probs.values())[0]
        sentence += next_unigram + ' '

    return sentence

def generate_sentence(ngram_probs):
    """
    Generates a sentence based on a dictionary of ngram probabilities.
    """
    # Look at keys in ngram_probs to figure out what's the order of our ngrams
    n = len(list(ngram_probs.keys())[0].split(' '))

    if n == 1:
        print('Please use generate_unigrams() to generate unigrams')

    # Look for 1st ngram. Consider only ngrams that start with n-1 <s> markers
    next_keys = []
    next_values = []
    for k, v in ngram_probs.items():
        if k.startswith(('<s> ' * (n - 1)).rstrip()):
            next_keys.append(k)
            next_values.append(v)
    # Choose ngram according to its probability
    sentence = choices(next_keys, weights=next_values)[0]
    # Next ngram must start with the last word of this ngram
    last_word = sentence.rsplit(' ', 1)[1]
    
    # Keep generating sentences until we get an n-gram with an </s> end marker 
    # Loop stops after the first </s>; we'll add the remaining markers later 
    while '</s>' not in last_word:
        # Look for next ngram.
        next_keys = []
        next_values = []
        for k, v in ngram_probs.items():
            if k.startswith(last_word):
                next_keys.append(k)
                next_values.append(v)
        
        # Choose ngram. Don't add first word since it's already in the sentence
        next_ngram = choices(next_keys, weights=next_values)[0]
        sentence += ' ' + next_ngram.split(' ', 1)[1]
        last_word = next_ngram.rsplit(' ', 1)[1]

    # Add missing sentence end markers
    sentence +=  ' </s>' * ((n - 1) - len(endmarker_regex.findall(sentence)))

    return sentence