# Machado Bot

A twitter bot that generates random sentences in the style of the Brazilian author Machado de Assis.

# How does the bot work?

The bot uses an [n-gram language model](https://web.stanford.edu/~jurafsky/slp3/3.pdf) to generate sentences. The model was trained on [the Machado de Assis Digital Corpus Project](http://machado.byu.edu/) from Brigham Young University. To make sentences easier to read, proper nouns are capitalized by a human reader.