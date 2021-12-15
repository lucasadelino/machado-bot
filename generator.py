from pathlib import Path
from tokenizer import tokenize
from ngram import ngram_prob, generate_sentence
import re

# Matches punctuation marks
punctuation_regex = re.compile(r"\s([.,;!?])")

# Matches en dashes surrounded by spaces. Useful for PT-BR parsing
travessao_regex = re.compile(r'\s(-)\s')

# This governs the order of the n-grams we generate
N = 5

# This governs how many sentences we want to generate
AMOUNT = 100

def generate():
    """
    Generates a pretty n-gram sentence.
    """
    with open(Path.cwd() / 'machado.txt', 'r', encoding='utf-8') as file:
        text = file.read()
        probs = ngram_prob(N, tokenize(text, punctuation=True))
        sentence = generate_sentence(probs)
        while len(sentence) > 280:
            sentence = generate_sentence(probs)

    # Prettify the sentence we just generated: capitalize, remove start & end 
    # markers and spaces around punctuation marks
    sentence = sentence.lstrip("<s> ").rstrip(' </s>').capitalize()
    sentence = travessao_regex.sub(r'\1', sentence)
    sentence = punctuation_regex.sub(r'\1', sentence)

    return sentence

with open(Path.cwd() / 'sentencequeue.txt', 'a') as file:
    sentences = ''
    for _ in range(100):
        sentences += generate() + '\n'
    file.write(sentences)
