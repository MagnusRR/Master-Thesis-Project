import re


class RemoveSubtitleMetadata:

    def __init__(self, remove_line_breaks=True, remove_alignment_tags=True, remove_simultaneous_subtitling_line=True):
        self.r = r'^$'

        if remove_line_breaks:
            self.r += r'|(\\r)?\\n'
        if remove_alignment_tags:
            self.r += r'|\{\\an\d+\}'
        if remove_simultaneous_subtitling_line:
            self.r += r'|(O|o)pptak av simultanteksting'

    def remove_subtitle_metadata(self, d):
        return re.sub(self.r, " ", " ".join(d)).split(" ")

    def batch_remove_subtitle_metadata(self, D):
        return [self.remove_metadata(d) for d in D]

    def __str__(self):
        return 'RemoveSubtitleMetadata'
