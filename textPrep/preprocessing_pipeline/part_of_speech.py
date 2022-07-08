from nltk.tag import pos_tag
import spacy


class PartOfSpeech:
    def __init__(self, is_english=True, spacy_language_pipeline=None):
        self.nlp = None
        if not is_english and spacy_language_pipeline:
            try:
                self.nlp = spacy.load(spacy_language_pipeline, exclude=[
                                      "parser", "lemmatizer", "senter", "ner"])
            except:
                print(
                    f"Could not load SpaCy pipeline '{spacy_language_pipeline}'.")
                self.nlp = None

    def tag_document(self, d):
        return pos_tag(d)

    def tag_document_multilingual(self, d):
        tokens = self.nlp(" ".join(d))
        return [(token.text, token.pos_) for token in tokens]

    def is_pos(self, term_tuple, pos='NNP'):
        '''
        :param term:
        :param pos (http://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html):
        :return:
        '''
        if term_tuple[1] == pos:
            return True
        return False

    def keep_pos(self, d, pos=('',)):
        new_d = []
        temp_d = []
        for w in d:
            if len(w) > 0:
                temp_d.append(w)
        tagged_d = None
        if not self.nlp:
            tagged_d = self.tag_document(temp_d)
        else:
            tagged_d = self.tag_document_multilingual(temp_d)
        for i in range(0, len(tagged_d)):
            w_tup = tagged_d[i]
            if w_tup[1] in pos:
                new_d.append(temp_d[i])
        return new_d

    def batch_keep_pos(self, D, pos=('',)):
        return [self.keep_pos(d, pos) for d in D]

    def __str__(self):
        return 'PoS'
