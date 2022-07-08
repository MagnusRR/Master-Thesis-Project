from textPrep.evaluation_metrics.dataset_stats import get_data_stats
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud
import random
from PIL.ImageColor import colormap


DATA_STATS_HEADERS = ["dataset_size", "vocab_size", "total_tokens",
                      "avg_token_freq", "avg_token_per_doc", "avg_stopwords_per_doc"]

DARK_COLORMAP = list(
    filter(lambda color: color[:4] == "dark", colormap.keys()))


def create_stats_table(subtitled_programs):
    stats = get_data_stats(subtitled_programs)
    return list(zip(DATA_STATS_HEADERS, stats))


def display_n_wordclouds(topics, title, num_topics, figsize=(6.4, 4.8), dpi=100.00):
    fig = plt.figure(figsize=figsize, dpi=dpi)
    j = int(np.ceil(num_topics/4))
    for t in range(num_topics):
        i = t+1
        plt.subplot(j, 4, i).set_title("Topic #" + str(t))
        plt.plot()
        plt.imshow(create_wordcloud(topics[t], height=300))
        plt.axis("off")
    fig.suptitle(title)
    plt.show()


def display_wordcloud(topic, title):
    fig = plt.figure()
    plt.plot()
    plt.imshow(create_wordcloud(topic))
    plt.axis("off")
    fig.suptitle(title)
    plt.show()


def create_wordcloud(topic, score_based=True, height=400, width=400, random_color=True, color=None):
    plot_color = None
    if random_color:
        plot_color = DARK_COLORMAP[random.randrange(0, len(DARK_COLORMAP))]
    elif not random_color and color:
        plot_color = color
    else:
        plot_color = "black"
    wordcloud = WordCloud(height=height, width=width, background_color="white", prefer_horizontal=1,
                          color_func=lambda *args, **kwargs: plot_color)
    if score_based:
        wordcloud.fit_words(topic)
    else:
        wordcloud.generate(topic)
    return wordcloud
