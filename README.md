# Machado Bot

A twitter bot ([@assisbot](https://twitter.com/assis_bot))that generates random sentences in the style of the Brazilian author Machado de Assis.

# How does the bot work?

Here's the gist of it: the bot uses an [n-gram language model](https://web.stanford.edu/~jurafsky/slp3/3.pdf) to generate sentences. The model was trained on [the Machado de Assis Digital Corpus Project](http://machado.byu.edu/) from Brigham Young University. To make sentences easier to read, proper nouns are capitalized by a human reader.

Now here's what each file in this repo does:

- [ngram.py](https://github.com/lucasadelino/machado-bot/blob/main/ngram.py) contains the language model that makes sentence generation possible. [tokenizer.py](https://github.com/lucasadelino/machado-bot/blob/main/tokenizer.py) contains helper functions to segment and tokenize sentences. 
- [generator.py](https://github.com/lucasadelino/machado-bot/blob/main/generator.py) uses the language model to generate several sentences and append those sentences to a text file ([sentencequeue.txt](https://github.com/lucasadelino/machado-bot/blob/main/sentencequeue.txt)).
- [bot.py](https://github.com/lucasadelino/machado-bot/blob/main/bot.py) reads the first sentence from sentencequeue.txt, tweets it, and deletes it. 

The primary reason for using a sentence queue is so make the bot output easier to read. It allows a human reader to manually capitalize given nouns and remove gibberish sentences (such as inconsistent punctuation marks).

This bot is deployed using [Python Anywhere](https://www.pythonanywhere.com).
