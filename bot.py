from pathlib import Path
import tweepy
import keys

def get_sentence():
    """
    Returns and dequeues the next sentence in the sentence queue.
    """
    with open(Path.cwd() / 'sentencequeue.txt', 'r') as file:
        contents = file.readlines()
        sentence = contents.pop(0)

    with open(Path.cwd() / 'sentencequeue.txt', 'w') as file:
        file.writelines(contents)

    return sentence

auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)
auth.set_access_token(keys.access_token, keys.access_token_secret)

api = tweepy.API(auth)
    
api.update_status(get_sentence())