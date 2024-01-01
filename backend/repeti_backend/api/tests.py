from django.test import TestCase
from nltk.corpus import wordnet
from nltk.corpus.reader.wordnet import WordNetError
import time

# Create your tests here.

def get_word_details(word):
    try:
        synsets = wordnet.synsets('askjdh')
    except WordNetError:
        return "Testing"
    details = []

    for syn in synsets:
        details.append({
            'synset_id' : syn.name(),
            'part_of_speech': syn.pos(),
            'definition': syn.definition(),
            'examples': syn.examples()
        })
    return details

start_time = time.time()
# print(get_word_details("dog"), get_word_details("cat"), get_word_details("cup"), get_word_details("book"), get_word_details("lotion"), get_word_details("whatsapp"), get_word_details("lid"), get_word_details("laptop"), get_word_details("retainer"), get_word_details("pill"), get_word_details("cartoon"), get_word_details("earphone"), get_word_details("watch"), get_word_details("rope"), get_word_details("window"), get_word_details("building"), get_word_details("apartment"), get_word_details("camera"), get_word_details("book"), get_word_details("liver"))
print(get_word_details('dog'))
end_time = time.time()
duration = end_time - start_time
print(f"The function took {duration} seconds to execute.")