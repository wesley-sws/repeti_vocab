from nltk.corpus import wordnet as wn

def get_word_details(word):
    synsets = wn.synsets(word)
    details = []

    for syn in synsets:
        part_of_speech = syn.pos()
        definition = syn.definition()
        examples = syn.examples()
        
        # Synonyms
        synonyms = set()
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
        
        # Antonyms
        antonyms = set()
        for lemma in syn.lemmas():
            for antonym in lemma.antonyms():
                antonyms.add(antonym.name())

        details.append({
            "part_of_speech": part_of_speech,
            "definition": definition,
            "examples": examples,
            "synonyms": list(synonyms),
            "antonyms": list(antonyms)
        })
    
    return details

# Example usage
# word_details = get_word_details("test")
# for i in word_details:
#     print(i)
for synset in wn.synsets('kill'):
    print(synset.definition())
    print("Hypernyms:", synset.hypernyms())
    for i in synset.hypernyms():
        print(i.definition())
    print("Hyponyms:", synset.hyponyms())
    for i in synset.hyponyms():
        print(i.definition())
    print("Done")