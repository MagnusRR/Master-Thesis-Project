from nltk.corpus import wordnet
import spacy

class Lemmatize:
    def __init__(self, is_english=True, spacy_language_pipeline=None):
        self.nlp = None
        if not is_english and spacy_language_pipeline:
            try:
                self.nlp = spacy.load(spacy_language_pipeline, exclude=["parser", "senter", "ner"])
            except:
                print(f"Could not load SpaCy pipeline '{spacy_language_pipeline}'.")
                self.nlp = None

    def lemmatize(self, word, ing=True):
        '''
        Return lemmatized noun or verb, else return None
        '''
        lemmas = wordnet._morphy(word, 'n')
        if lemmas:
            return min(lemmas, key=len)
        lemmas = wordnet._morphy(word, 'a')
        if lemmas:
            return min(lemmas, key=len)
        lemmas = wordnet._morphy(word, 'v', )
        if lemmas:
            return min(lemmas, key=len)
        if ing and word.endswith('in'):
            word += 'g'
            lemmas = wordnet._morphy(word, 'v')
            if lemmas:
                return min(lemmas, key=len)
        return None
    
    def lemmatize_document_multilingual(self, d):
        tokens = self.nlp(" ".join(d))
        return [token.lemma_ for token in tokens]

    def lemmatize_document(self, d, strict=False):
        new_d = []
        if not self.nlp:
            for i in range(0, len(d)):
                word = d[i]
                lemmatized_word = self.lemmatize(word)
                if lemmatized_word is not None:
                    new_d.append(lemmatized_word)
                elif not strict:
                    new_d.append(d[i])
        else:
            new_d = self.lemmatize_document_multilingual(d)
        return new_d

    def batch_lemmatize(self, D, strict=False):
        return [self.lemmatize_document(d, strict) for d in D]

    def __str__(self):
        return 'Lemmatization'
