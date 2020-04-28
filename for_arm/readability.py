import re
from nltk import word_tokenize
from collections import Counter
import math


def word_tokenizer(text):
    return word_tokenize(text)


def char_tokenizer(text):
    return [x for x in text if x.isalpha()]


def char_numbers(text):
    return [x for x in text if x.isalpha() and not x.isspace()]


def sentence_tokenizer(text):
    sentences = re.split('։ |։|:|: ', text)
    return [x for x in sentences if len(x)]


def syllables(text):
    c = Counter(text)
    return c["ա"] + c["ե"] + c["է"] + c["ը"] + c["ի"] + c["ո"] + c["և"] + c["օ"]


def flesch_reading_ease(text):
    word_counts = len(word_tokenizer(text))
    syllables_count = syllables(text)
    sentence_count = len(sentence_tokenizer(text))
    try:
        FSE = 78.39 + 2.6 * (word_counts/sentence_count) - 32.3 * (syllables_count / word_counts)
    except ZeroDivisionError:
        return 0.0
    return round(FSE, 2)


def smog_index(text):
    syllables_count = syllables(text)
    sentence_count = len(sentence_tokenizer(text))
    try:
        smog = 0.6*math.sqrt(syllables_count/ sentence_count) + 9
    except ZeroDivisionError:
        return 0.0
    return round(smog, 2)


def flesch_kincaid_grade(text):
    word_counts = len(word_tokenizer(text))
    syllables_count = syllables(text)
    sentence_count = len(sentence_tokenizer(text))
    try:
        FK = -0.33*(word_counts/sentence_count)+6.42*(syllables_count / word_counts) + 4.7
    except ZeroDivisionError:
        return 0.0
    return round(FK, 2)


def coleman_liau_index(text):
    char_count = len(char_tokenizer(text))
    word_count = len(word_tokenizer(text))
    sentence_count = len(sentence_tokenizer(text))
    try:
        CL = 1.2*(char_count / word_count)+62.65*(sentence_count/word_count) + 0.662
    except ZeroDivisionError:
        return 0.0
    return round(CL, 2)


def automated_readability_index(text):
    charnum_count = len(char_numbers(text))
    word_count = len(word_tokenizer(text))
    sentence_count = len(sentence_tokenizer(text))
    try:
        AT = 3.062*(charnum_count / word_count)-0.049*(word_count/sentence_count) + 0.078
    except ZeroDivisionError:
        return 0.0
    return round(AT, 2)

def dale_chall_readability_score(text):
    words = word_tokenizer(text)
    word_count = len(words)
    c = 0
    for word in words:
        if syllables(word) > 3:
            c += 1
    count = word_count - c
    try:
        per = float(count) / float(word_count) * 100
    except ZeroDivisionError:
        return 0.0
    difficult_words = 100 - per
    score = ((0.1579 * difficult_words) + (0.0496 * word_count / len(sentence_tokenizer(text))))
    if difficult_words > 5:
        score += 3.6365
    return round(score, 2)


def linsear_write_formula(text):
    words = word_tokenizer(text)[:100]
    sentence_count = len(sentence_tokenizer(' '.join(words)))
    c1 = 0
    c3 = 0
    for word in words:
        if syllables(word) < 3:
            c1 = c1 + 1
        else:
            c3 = c3 + 1
    try:
        lin = float((c1 + c3)/sentence_count)
    except ZeroDivisionError:
        return 0.0
    return round(lin, 2)


def difficult_words(text):
    c = 0
    for word in word_tokenizer(text):
        if syllables(word) > 3:
            c += 1
    return c


def gunning_fog(text):
    words = word_tokenizer(text)
    words_count = len(words)
    sentence_count = len(sentence_tokenizer(text))
    c = 0
    for word in words:
        if syllables(word) > 3:
            c += 1
    try:
        GF = 0.4*(words_count/sentence_count + 100*(c/words_count))
    except ZeroDivisionError:
        return 0.0
    return round(GF, 2)


get_readability_test = {
    'flesch_reading_ease': flesch_reading_ease,
    'smog_index': smog_index,
    'flesch_kincaid_grade': flesch_kincaid_grade,
    'coleman_liau_index': coleman_liau_index,
    'automated_readability_index': automated_readability_index,
    'dale_chall_readability_score': dale_chall_readability_score,
    'linsear_write_formula': linsear_write_formula,
    'difficult_words': difficult_words,
    'gunning_fog': gunning_fog
}