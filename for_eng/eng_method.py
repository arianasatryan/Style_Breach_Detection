import os
import re
import operator
import json
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import scipy.sparse as sp
import pandas as pd
import numpy as np
from scipy.stats import wilcoxon
from sklearn.cluster import AgglomerativeClustering
avgwordlength = 5

train_path = '/Users/hekpo/PycharmProjects/Style_Breach_Detection/for_eng/data/pan17-style-breach-detection-training-dataset-2017-02-15'
test_path = '/Users/hekpo/PycharmProjects/Style_Breach_Detection/for_eng/data/pan17-style-breach-detection-test-dataset-2017-02-15'
train_files = os.listdir(train_path + '/')
test_files = os.listdir(test_path + '/')
train_results_path = '/Users/hekpo/PycharmProjects/Style_Breach_Detection/for_eng/results/train_results'
test_results_path = '/Users/hekpo/PycharmProjects/Style_Breach_Detection/for_eng/results/test_results'

def by_method(method_name, segments, dataframe,
              allowed_portion = 1, alpha_value = 1,
              n_clusters = 2, linkage = 'ward', affinity = 'euclidean'):

    style_change_borders = []
    starts_of_segments = get_starts_of_sentsegs(segments)
    if(method_name == 'Wilcoxon'):
        # doing Wilcoxon sign-rank test
        num_of_segments = len(segments)
        pvalues = {}
        for i in range(num_of_segments - 1):
            stat, pvalue = wilcoxon(dataframe.iloc[i], dataframe.iloc[i + 1], zero_method = 'pratt', alternative = 'two-sided')
            pvalues[i + 1] = pvalue
        # sorting pvalues in increasing  order
        sorted_pvalues = sorted(pvalues.items(), key = operator.itemgetter(1))
        # defining % of suspicious parts
        p = allowed_portion
        S = int(p * num_of_segments)
        if p != 1:
            S += 1
        # making a decision whether is a border
        for tpl in (sorted_pvalues[:S]):
            if tpl[1] <= alpha_value:
                style_change_borders.append(starts_of_segments[tpl[0] + 1])                                # +1 cause the numeration of paragraphs starts at 1
        style_change_borders.sort()
        return style_change_borders
    if(method_name == 'AgglomerativeClustering'):
        if len(segments) > 1:
            if linkage == 'ward':
                affinity = 'euclidean'
            model = AgglomerativeClustering(n_clusters = n_clusters, linkage = linkage, affinity = affinity)
            clusters = model.fit_predict(dataframe)
            for i in range(len(clusters) - 1):
                if clusters[i] != clusters[i + 1]:
                    style_change_borders.append(starts_of_segments[i + 1 + 1])     # +1 cause the numeration of paragraphs starts at 1
        return style_change_borders

def get_starts_of_paragraphs(paragraphs):
    start_of_paragraph = {}
    i = 1
    length = 0
    for item in paragraphs:
        start_of_paragraph[i] = length
        i += 1
        length += (len(item) + 2)
    return start_of_paragraph

def get_starts_of_sentsegs(sentseg):
    start_of_sentseg = {}
    i = 1
    length = 0
    for item in sentseg:
        start_of_sentseg[i] = length
        i += 1
        length += (len(item) + 1)
    return start_of_sentseg

def get_paragraphs_of(file_dir):
    with open(file_dir, encoding='utf-8')as fin:
        text = fin.read()
        white_line_regex = r"(?:\r?\n){2,}"
        paragraphs = re.split(white_line_regex, text.strip())
    return paragraphs

def get_sentsegs_of(file_dir, m):
    with open(file_dir, encoding = 'utf-8')as fin:
        text = fin.read()
    sents = sent_tokenize(text)
    sent_num = len(sents)
    i = 0
    paragraphs = []
    while i + m < sent_num:
        sents_str = ' '.join([str(elem) for elem in sents[i:i + m]])
        paragraphs.append(sents_str)
        i += m
    sents_str = ' '.join([str(elem) for elem in sents[i:sent_num]])
    paragraphs.append(sents_str)
    return paragraphs


#punctuation tokenizer 
punct_list = [ '.', '?', '!', ',' , ';', ':', '-', '--', '[', ']', '{', '}', '(', ')', '"']
def punct_tokenizer(text):
    punct_tokens = []
    for item in text:
        if item in punct_list:
            punct_tokens.append(item)
    return punct_tokens

# stopwords tokenizer
stopWords = set(stopwords.words('english'))
def stopword_tokenizer(text):
    word_tokens = word_tokenize(text)
    stopword_tokens = []
    for item in word_tokens:
        if item in stopWords:
            stopword_tokens.append(item)
    return stopword_tokens

#POS tokenizer
def pos_tokenizer(text):
    word_tokens = word_tokenize(text)
    results = pos_tag(word_tokens)
    pos_tokens = []
    for word_pos in results:
        pos_tokens.append(word_pos[1])
    return pos_tokens

#long_word tokenizer
def longword_tokenizer(text):
    word_tokens = word_tokenize(text)
    long_words = []
    for item in word_tokens:
        if len(item)>avgwordlength*1.5:
            long_words.append(item)
    return long_words

def shortword_tokenizer(text):
    word_tokens = word_tokenize(text)
    short_words = []
    for item in word_tokens:
        if len(item)<avgwordlength/1.5:
            short_words.append(item)
    return short_words

def avgsent_length(text):
    sent_tokens = sent_tokenize(text)
    return len(text)/len(sent_tokens)

def longsent_procent(text):
    sent_tokens = sent_tokenize(text)
    avg_sent_len = len(text)/len(sent_tokens)
    long_sents_count = 0
    for sent in sent_tokens:
        if len(sent)>avg_sent_len:
            long_sents_count += 1
    return long_sents_count/len(sent_tokens)

def space_procent(text):
    space_count = 0
    for item in text:
        if item.isspace():
            space_count += 1
    return space_count/len(text)


# train_or_test is a string just to separate results_directories('train'or 'test')
#how_to_split is a string that specify method of splitting('par' or 'sent')
def method_for_files(files, how_to_split, method_name, allowed_portion = 1, alpha_value = 1, n_clusters = 2, linkage = 'ward', affinity = 'euclidean'):
    if files == train_files:
        path = train_path
        train_or_test = 'train'
        output_path = train_results_path
    else:
        path = test_path
        train_or_test = 'test'
        output_path = test_results_path
    for file in files:
        if file.endswith(".txt"):
            filename, file_format = os.path.splitext(os.path.basename(path + '/' + file))
            if (how_to_split == 'par'):
                segments = get_paragraphs_of(path + '/' + file)
                starts_of_segments = get_starts_of_paragraphs(segments)
            elif (how_to_split == 'sent'):
                segments = get_sentsegs_of(path + '/' + file, m = 10)

            # 1.word tfidf
            word_vectorizer = TfidfVectorizer(tokenizer = word_tokenize)
            word_vectors = word_vectorizer.fit_transform(segments)
            # 2.punctation tfidf
            punct_vectorizer = TfidfVectorizer(tokenizer = punct_tokenizer)
            punct_vectors = punct_vectorizer.fit_transform(segments)
            # 3.POS tfidf
            pos_vectorizer = TfidfVectorizer(tokenizer = pos_tokenizer)
            pos_vectors = pos_vectorizer.fit_transform(segments)
            # 4.stopwords tfidf
            stopword_vectorizer = TfidfVectorizer(tokenizer = stopword_tokenizer)
            stopword_vectors = stopword_vectorizer.fit_transform(segments)
            # 5.3-grams tfidf
            three_gram_vectorizer = TfidfVectorizer(ngram_range = (3, 3))
            three_gram_vectors = three_gram_vectorizer.fit_transform(segments)
            """#new features
            # longword tfidf
            longword_vectorizer = TfidfVectorizer(tokenizer = longword_tokenizer)
            longword_vectors = longword_vectorizer.fit_transform(segments)
            # shortword tfidf
            shortword_vectorizer = TfidfVectorizer(tokenizer = shortword_tokenizer)
            shortword_vectors = shortword_vectorizer.fit_transform(segments)
            # additional features
            avgsentlens = []
            longsentprocs = []
            spaceprocs = []
            for segment in segments:
                avgsentlens.append(avgsent_length(segment))
                longsentprocs.append(longsent_procent(segment))
                spaceprocs.append(space_procent(segment))
            add_df = pd.DataFrame(np.column_stack([avgsentlens, longsentprocs, spaceprocs]))
            """
            # used features tf-idfs concatenating
            vectors = sp.hstack((word_vectors, punct_vectors, pos_vectors, stopword_vectors, three_gram_vectors), format = 'csr')
            #vectors = sp.hstack((word_vectors, pos_vectors, stopword_vectors), format = 'csr')
            #vectors = sp.hstack((longword_vectors, shortword_vectors), format = 'csr')
            #vectors = sp.hstack((word_vectors, pos_vectors, stopword_vectors, longword_vectors, shortword_vectors), format = 'csr')
            #vectors = sp.hstack((word_vectors, punct_vectors, pos_vectors, stopword_vectors, three_gram_vectors, longword_vectors, shortword_vectors), format = 'csr')

            denselist = (vectors.todense()).tolist()
            df = pd.DataFrame(denselist)
            #df = pd.concat([df, add_df], axis = 1, ignore_index = True)

            style_change_borders = by_method(method_name = method_name, segments = segments, dataframe = df,
                                             allowed_portion = allowed_portion, alpha_value = alpha_value,
                                             n_clusters = n_clusters, linkage = linkage, affinity = affinity)

            # writing results
            with open(output_path + '/' + ('%s.truth' % filename), 'w') as o_f:
                json.dump({"borders": style_change_borders}, o_f, indent = 4)


method_for_files(train_files, 'par', method_name = 'Wilcoxon', allowed_portion = 1, alpha_value = 0.05)


