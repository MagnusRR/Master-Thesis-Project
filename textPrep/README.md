# textPrep
a text preprocessing library for topic models

### Requirements
to install relevant requirements:
> pip install -r requirements.txt

Additional NLTK packages needed:
> stopwords
> 
> wordnet
> 
> averaged_perceptron_tagger

To install NLTK packages:
> python
```python
import nltk 
nltk.download()
```

Choose just the required packages (the whole set of additional NLTK data is massive)

### Using textPrep

#### Creating a pipeline and preprocessing
```python
from preprocessing_pipeline import (Preprocess, RemovePunctuation, Capitalization, RemoveStopWords, RemoveShortWords, TwitterCleaner, RemoveUrls)

# initialize the pipeline
pipeline = Preprocess()

# initialize the rules you want to use
rp = RemovePunctuation(keep_hashtags=False)
ru = RemoveUrls()
cap = Capitalization()

# include extra data in a rule if necessary
from nltk.corpus import stopwords
stopwords_list = stopwords.words('english')
stopwords_list.append(['rt', 'amp'])

rsw = RemoveStopWords(extra_sw=stopwords_list)

# add rules to the pipeline (the stringified rule makes it easy to save the pipeline details)
pipeline.document_methods = [(ru.remove_urls, str(ru),),
                             (rp.remove_punctuation, str(rp),),
                             (cap.lowercase, str(cap),),
                             (rsw.remove_stopwords, str(rsw),)
                             ]
```

You can load your data however you want, so long as it ends up as a list of lists. We provide methods for loading CSV files with and without dates.
```python
# load the data
def load_dataset_with_dates(path):
    dataset = []
    try:
        with open(path, 'r') as f:
            for line in f:
                dataset.append(line.strip().split('\t')[1].split(' '))
        return dataset
    except FileNotFoundError:
        print('The path provided for your dataset does not exist: {}'.format(path))
        import sys
        sys.exit()

dataset = load_dataset_with_dates('data/sample_tweets.csv')
# dataset[i] = ['list', 'of', 'words', 'in', 'document_i']

# initialize the pipeline runner
from preprocessing_pipeline.NextGen import NextGen

runner = NextGen()

# preprocess the data, with some extra ngrams thrown in to ensure they are considered regardless of frequency
processed_dataset = runner.full_preprocess(dataset, pipeline, ngram_min_freq=10, extra_bigrams=None, extra_ngrams=['donald$trump', 'joe$biden', 'new$york$city'])

# assess data quality quickly and easily
from evaluation_metrics.dataset_stats import get_data_stats
print(get_data_stats(processed_dataset))
```

You can do some extra filtering after preprocessing, like TF-IDF filtering
```python
from settings.common import word_tf_df

freq = {}
freq = word_tf_df(freq, processed_dataset)
filtered_dataset = runner.filter_by_tfidf(dataset=processed_dataset, freq=freq, threshold=0.25)

# assess data quality again 
from evaluation_metrics.dataset_stats import get_data_stats
print(get_data_stats(filtered_dataset))
```

### Adding new rules
To add a new custom rule to textPrep, for example MyRule, do the following steps:

1. Update version to `"1.X.0"`, where X = old_X+1, in `setup(..., version='...', ...)` in `../setup.py`
1. Create a new file called `my_rule.py` in `preprocessing_pipeline`
1. Create the empty class `MyRule` in `my_rule.py`
1. Add `MyRule` to the list of imports `from .pipeline import (...)` in `preprocessing_pipeline/__init__.py`
1. Add `from .my_rule import MyRule` in `preprocessing_pipeline/pipeline.py`
1. Add `MyRule` to the list of imports `from ..preprocessing_pipeline import (...)` in `settings/common.py`
1. Implement your rule by adding, at minimum, the following methods:
```python
class MyRule:

    # Relevant class variables

    def __init__(self):
        # Relevant instance variables
    
    # ----------------------------------------
    # Other relevant class or instance methods
    # ----------------------------------------

    def my_rule(
        self,
        d,
        # my_parameter1,
        # my_parameter2,
        # ...,
        ):
        new_d = []
        # Implementation of my_rule : d -> new_d
        return new_d

    def batch_my_rule(self, D):
        return [self.my_rule(d) for d in D]

    def __str__(self):
        return 'MyRule'
```

### Referencing textPrep

```
Churchill, Rob and Singh, Lisa. 2021. textPrep: A Text Preprocessing Toolkit for Topic Modeling on Social Media Data. DATA 2021.
```

```bibtex 
@inproceedings{churchill2021textprep,
author = {Churchill, Rob and Singh, Lisa},
title = {textPrep: A Text Preprocessing Toolkit for Topic Modeling on Social Media Data},
booktitle = {DATA 2021},
year = {2021},
}
```