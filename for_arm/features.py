from for_arm.arm_tokenizer import tokenize
from nltk.tag.perceptron import PerceptronTagger
from nltk.tokenize import sent_tokenize
PICKLE = "averaged_perceptron_tagger.pickle"

def get_punct_list():
    return ['«', '»', '(', ')', '/', '\\', ',', '.', '․', ':', '։', '՝', '՟', '՚', '՜', '՛', '՞', '—']
def get_prefixes_list():
    return open('prefixes_hy.txt', encoding='utf-8').read().splitlines()
def get_suffixes_list():
    return open('suffixes_hy.txt', encoding='utf-8').read().splitlines()
def get_tokenized(text):
    return tokenize(text)

def punct_tokenizer(text):
    punct_list = get_punct_list()
    punct_tokens = []
    for item in text:
        if item in punct_list:
            punct_tokens.append(item)
    return punct_tokens

def punct_space_tokenizer(text):
    punct_list = get_punct_list()
    none_spaced=[]
    left_spaced = []
    right_spaced = []
    two_spaced=[]
    for index in range(1,len(text)-1):
        if text[index] in punct_list:
            if text[index-1] == ' ' and text[index+1] == ' ':
                two_spaced.append(text[index-1:index+2])
            if text[index-1] == ' ' and text[index+1] != ' ':
                left_spaced.append(text[index-1:index+1])
            if text[index-1] != ' ' and text[index+1] == ' ':
                right_spaced.append(text[index:index+2])
            if text[index-1] != ' ' and text[index+1] != ' ':
                none_spaced.append(text[index])
    return (none_spaced + left_spaced + right_spaced + two_spaced)

def prefix_tokenizer(text):
    prefixes_list = get_prefixes_list()
    word_tokens = get_tokenized(text)
    prefix_tokens = []
    for item in word_tokens:
        for prefix in prefixes_list:
            if item.startswith(prefix):
                prefix_tokens.append(prefix)
    return prefix_tokens

def suffix_tokenizer(text):
    suffixes_list = get_suffixes_list()
    word_tokens = get_tokenized(text)
    prefix_tokens = []
    for item in word_tokens:
        for suffix in suffixes_list:
            if item.endswith(suffix):
                prefix_tokens.append(suffix)
    return prefix_tokens

def long_word_tokenizer(text):
    word_tokens = get_tokenized(text)
    avg_word_len = len(text)/len(word_tokens)
    long_words = []
    for item in word_tokens:
        if len(item)>avg_word_len:
            long_words.append(item)
    return long_words

def short_word_tokenizer(text):
    punct_list = get_punct_list()
    word_tokens = get_tokenized(text)
    avg_word_len = len(text)/len(word_tokens)
    short_words = []
    for item in word_tokens:
        if len(item) < avg_word_len and item not in punct_list:
            short_words.append(item)
    return short_words

def sent_count(text):
    sents = sent_tokenize(text)
    return len(sents)

def avg_sent_len(text):
    sents = sent_tokenize(text)
    return len(text)/len(sents)

def max_sent_len(text):
    sents = sent_tokenize(text)
    sent_len = []
    for sent in sents:
        sent_len.append(len(sent))
    return max(sent_len)

def min_sent_len(text):
    sents = sent_tokenize(text)
    sent_len = []
    for sent in sents:
        sent_len.append(len(sent))
    return min(sent_len)

def long_sent_portion(text):
    sents = sent_tokenize(text)
    avg_sent_len = len(text)/len(sents)
    long_sent_count = 0
    for sent in sents:
        if len(sent) > avg_sent_len:
            long_sent_count += 1
    return long_sent_count/len(sents)

def short_sent_portion(text):
    sents = sent_tokenize(text)
    avg_sent_len = len(text)/len(sents)
    short_sent_count = 0
    for sent in sents:
        if len(sent) < avg_sent_len:
            short_sent_count += 1
    return short_sent_count/len(sents)

def stopword_tokenizer(text):
    stopwords_list = open('stopwords_hy.txt', encoding='utf-8').read().splitlines()
    word_tokens = tokenize(text)
    stopword_tokens = []
    for item in word_tokens:
        if item in stopwords_list:
            stopword_tokens.append(item)
    return stopword_tokens

def pos_tokenizer(text):
    word_tokens = tokenize(text)
    # using pretrained model to tag all tokens
    pretrained_tagger = PerceptronTagger(load=True)
    results = pretrained_tagger.tag(word_tokens)
    # collecting pos from resulting tuples
    pos_tokens = []
    for word_pos in results:
        pos_tokens.append(word_pos[1])
    return pos_tokens

