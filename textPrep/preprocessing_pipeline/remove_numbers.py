import re


class RemoveNumbers:

    def __init__(self):
        self.r = r'\d'

    def remove_numbers(self, d):
        new_d = []
        for w in d:
            w = re.sub(self.r, "", w)
            if len(w) > 0:
                new_d.append(w)
        return new_d

    def batch_remove_numbers(self, D):
        return [self.remove_numbers(d) for d in D]

    def __str__(self):
        return 'Numbers'
