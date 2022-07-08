from csv import DictWriter, DictReader
import os
import glob
import random
import re
import pandas as pd
import pickle
import zipfile

ROOT_PATH = os.path.abspath(os.curdir)
ROOT_NST_PATH = os.path.join(os.path.abspath(
    os.curdir), "../AMG-Data/NST/NST_csv")
SAMPLE_SIZE = 1000
FILE_NAME = "File name"
NUMBER = "Number"
SUBTITLE = "Subtitle"
PROGRAM_ID = "Program ID"
TOKENIZED_SUBTITLES = "Tokenized subtitles"
STAT = "Stat"
VALUE = "Value"
RULE_NAME = "Rule name"
RULE_METHOD = "Rule method"
TOPIC_ID = "Topic ID"
TOPIC_WORDS = "Topic words"
WORD = "Word"
FREQUENCY = "Frequency"
WORD_PAIR = "Word pair"
CO_FREQUENCY = "Co-frequency"


# Load NST sample from NST folder
def load_nst_sample_from_nst(sample_size=SAMPLE_SIZE, full_sample=False):
    if os.path.isdir(ROOT_NST_PATH):
        filename_start = len(ROOT_NST_PATH) + 1

        # Extract only Norwegian subtitle files
        nst_files = filter(
            lambda filename: filename[-7:-4] == "TTV", glob.glob(ROOT_NST_PATH + "/*.csv"))

        # Either get a sample or the full dataset
        nst_filenames = []
        if full_sample:
            nst_filenames = list(nst_files)
        else:
            nst_filenames = random.sample(
                list(nst_files), int(1.1 * sample_size))

        nst_sample = {}
        for filename in nst_filenames:
            try:
                file_df = pd.read_csv(filename, sep=";")
            except pd.errors.ParserError:
                pass
            else:
                nst_sample[filename[filename_start:]] = file_df.iloc[:, 1:]
            if not full_sample and len(nst_sample) == sample_size:
                break
        print("Sample size:", len(nst_sample), "\n")
    else:
        print("NST files not found")
    return nst_sample


# Load NST sample
def load_nst_sample(file_path):
    nst_sample = {}
    try:
        file = open(file_path, "r", encoding="utf-8")
    except FileNotFoundError:
        print("NST sample file not found")
    else:
        with file:
            file_reader = DictReader(file, delimiter=";")
            file_name = ""
            subtitle_list = []
            for row in file_reader:
                if file_name != row[FILE_NAME]:
                    if file_name != "":
                        nst_sample[file_name] = pd.DataFrame(
                            subtitle_list).drop(columns=[FILE_NAME, NUMBER])
                    subtitle_list = []
                    file_name = row[FILE_NAME]
                subtitle_list.append(row)
            nst_sample[file_name] = pd.DataFrame(
                subtitle_list).drop(columns=[FILE_NAME, NUMBER])
    return nst_sample


def subtitles_file_exists(relative_folder_path, file_name):
    file_path = os.path.join(
        ROOT_PATH, relative_folder_path, "data", str(file_name + r".csv"))
    return os.path.exists(file_path)


# Write preprocessed subtitles to file
def write_subtitles_file(relative_folder_path, file_name, subtitled_programs_dict):
    file_path = os.path.join(
        ROOT_PATH, relative_folder_path, "data", str(file_name + r".csv"))
    _write_csv_file(file_path, subtitled_programs_dict.items(), key=PROGRAM_ID,
                    value=TOKENIZED_SUBTITLES, value_formatter=lambda value: ",".join(value))


# Load preprocessed subtitles file
def load_subtitles(relative_folder_path, file_name):
    file_path = os.path.join(
        ROOT_PATH, relative_folder_path, "data", str(file_name + r".csv"))
    return _read_csv_file(file_path, key=PROGRAM_ID, value=TOKENIZED_SUBTITLES,
                          value_formatter=lambda value: value.split(","))


def load_subtitles_from_nst_sample(nst_sample_size):
    file_path = os.path.join(
        ROOT_PATH, "nst_sample", str(f"nst_{nst_sample_size}_text.csv"))
    subtitled_programs = {}
    with open(file_path, "r", encoding="utf-8") as file:
        reader = DictReader(file, delimiter=";")
        first_row = next(reader)
        file_name = first_row[FILE_NAME]
        subtitle_list = [first_row[SUBTITLE]]
        for row in reader:
            if row[FILE_NAME] != file_name:
                subtitled_programs[file_name] = " ".join(
                    subtitle_list).split()
                subtitle_list = []
                file_name = row[FILE_NAME]
            subtitle_list.append(row[SUBTITLE])
        subtitled_programs[file_name] = " ".join(subtitle_list).split()
    return subtitled_programs


def stats_file_exists(relative_folder_path, file_name):
    file_path = os.path.join(
        ROOT_PATH, relative_folder_path, "stats", str(file_name + r"_stats.csv"))
    return os.path.exists(file_path)


# Write textPrep stats of preprocessed data to file
def write_stats_file(relative_folder_path, file_name, stats):
    file_path = os.path.join(
        ROOT_PATH, relative_folder_path, "stats", str(file_name + r"_stats.csv"))
    _write_csv_file(file_path, stats, key=STAT, value=VALUE)


# Load textPrep stats of preprocessed data
def load_stats_file(relative_folder_path, file_name):
    file_path = os.path.join(
        ROOT_PATH, relative_folder_path, "stats", str(file_name + r"_stats.csv"))
    return _read_csv_file(file_path, key=STAT, value=VALUE)


# Write textPrep pipeline of preprocessed data to file
def write_pipeline_file(relative_folder_path, file_name, pipeline_methods):
    file_path = os.path.join(ROOT_PATH, relative_folder_path, "pipelines", str(
        file_name + r"_pipeline.csv"))
    _write_csv_file(file_path, pipeline_methods, key=RULE_NAME,
                    value=RULE_METHOD, key_formatter=lambda key: key.__name__, reverse_key_value_order=True)


# Write data word frequencies
def write_word_frequencies_file(relative_folder_path, file_name, word_frequencies):
    file_path = os.path.join(
        ROOT_PATH, relative_folder_path, str(file_name + r".csv"))
    _write_csv_file(file_path, list(word_frequencies.items()),
                    key=WORD, value=FREQUENCY)


# Load data word frequencies
def load_word_frequencies(relative_folder_path, file_name):
    file_path = os.path.join(
        ROOT_PATH, relative_folder_path, str(file_name + r".csv"))
    return _read_csv_file(file_path, key=WORD, value=FREQUENCY,
                          value_formatter=lambda value: int(value))


# Write data word co-frequencies to regular CSV file
def write_word_co_frequencies_file(relative_folder_path, file_name, word_co_frequencies):
    file_path = os.path.join(
        ROOT_PATH, relative_folder_path, str(file_name + ".csv"))
    _write_csv_file(file_path, word_co_frequencies, key=WORD_PAIR, value=CO_FREQUENCY,
                    key_formatter=lambda key: tuple(
                        re.sub(r"['\)\(]", "", key).split(",")),
                    value_formatter=lambda value: int(value))


# Load data word co-frequencies from regular CSV file
def load_word_co_frequencies(relative_folder_path, file_name):
    file_path = os.path.join(
        ROOT_PATH, relative_folder_path, str(file_name + ".csv"))
    return _read_csv_file(file_path, key=WORD_PAIR, value=CO_FREQUENCY)


# Write data word co-frequencies to zipped file
def write_word_co_frequencies_zip_file(relative_folder_path, file_name, word_co_frequencies):
    file_path = os.path.join(
        ROOT_PATH, relative_folder_path, str(file_name + ".pkl"))
    with zipfile.ZipFile(file_path + ".zip",
                         mode="w", compression=zipfile.ZIP_DEFLATED) as zipped_file:
        with zipped_file.open(file_name + ".pkl", mode="w", force_zip64=True) as file:
            pickle.dump(word_co_frequencies, file,
                        protocol=pickle.HIGHEST_PROTOCOL)


# Load data word co-frequencies from zipped file
def load_zipped_word_co_frequencies(relative_folder_path, file_name):
    file_path = os.path.join(
        ROOT_PATH, relative_folder_path, str(file_name + ".pkl"))
    with zipfile.ZipFile(file_path + ".zip", mode="r") as zipped_file:
        with zipped_file.open(file_name + ".pkl", mode="r") as file:
            return pickle.load(file)


def write_topics_file(relative_folder_path, file_name, topics, model=None, num_lda_topics=8, top2vec_embedding="distiluse"):
    file_path = os.path.join(ROOT_PATH, relative_folder_path)
    if model == "lda":
        file_path = os.path.join(file_path, model, str(
            file_name + f"_{model}_{num_lda_topics}_topics.csv"))
    elif model == "top2vec":
        file_path = os.path.join(file_path, model, str(
            file_name + f"_{model}_{top2vec_embedding}.csv"))
    else:
        file_path = os.path.join(file_path, str(file_name + ".csv"))
    _write_csv_file(file_path, topics, key=TOPIC_ID, value=TOPIC_WORDS,
                    value_formatter=lambda value: ",".join(value))


# Load topics of model
def load_model_topics(relative_folder_path, file_name, model=None, num_lda_topics=8, top2vec_embedding="distiluse"):
    file_path = os.path.join(ROOT_PATH, relative_folder_path)
    if model == "lda":
        file_path = os.path.join(file_path, model, str(
            file_name + f"_{model}_{num_lda_topics}_topics.csv"))
    elif model == "top2vec":
        file_path = os.path.join(file_path, model, str(
            file_name + f"_{model}_{top2vec_embedding}.csv"))
    else:
        file_path = os.path.join(file_path, str(file_name + ".csv"))
    return _read_csv_file(file_path, key=TOPIC_ID, value=TOPIC_WORDS,
                          key_formatter=lambda key: int(key),
                          value_formatter=lambda value: value.split(","))


def _read_csv_file(file_path, key, value, key_formatter=lambda key: key, value_formatter=lambda value: value):
    data = {}
    with open(file_path, "r", encoding="utf-8") as file:
        reader = DictReader(file, delimiter=";")
        for row in reader:
            row_key = key_formatter(row[key])
            row_value = value_formatter(row[value])
            data[row_key] = row_value
    return data


def _write_csv_file(file_path, data, key, value, key_formatter=lambda key: key, value_formatter=lambda value: value, reverse_key_value_order=False):
    with open(file_path, encoding="utf-8", mode="w", newline="") as file:
        writer = DictWriter(file, fieldnames=[key, value], delimiter=";")
        writer.writeheader()
        for (row_key, row_value) in data:
            row = {key: key_formatter(
                row_key), value: value_formatter(row_value)}
            if reverse_key_value_order:
                row = {key: value_formatter(
                    row_value), value: key_formatter(row_key)}
            writer.writerow(row)
