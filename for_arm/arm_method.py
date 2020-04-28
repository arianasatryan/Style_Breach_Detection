import os
import json
import operator
from for_arm.arm_tokenizer import tokenize
from nltk.tag.perceptron import PerceptronTagger
from sklearn.feature_extraction.text import TfidfVectorizer
import scipy.sparse as sp
import pandas as pd
from scipy.stats import wilcoxon
from sklearn.cluster import AgglomerativeClustering
from information import get_starts_of_paragraphs, get_paragraphs_of

PICKLE = "averaged_perceptron_tagger.pickle"

train_path = '/Users/hekpo/PycharmProjects/Style_Breach_Detection/for_arm/data/train_dataset'
test_path = '/Users/hekpo/PycharmProjects/Style_Breach_Detection/for_arm/data/test_dataset'
train_files = os.listdir(train_path + '/')
test_files = os.listdir(test_path + '/')
train_results_path = '/Users/hekpo/PycharmProjects/Style_Breach_Detection/for_arm/results/train_results'
test_results_path = '/Users/hekpo/PycharmProjects/Style_Breach_Detection/for_arm/results/test_results'
train_output_path = '/Users/hekpo/PycharmProjects/Style_Breach_Detection/for_arm/results/train_results'
test_output_path = '/Users/hekpo/PycharmProjects/Style_Breach_Detection/for_arm/results/test_results'

def by_method(method_name, paragraphs, dataframe,
              allowed_portion = 1, alpha_value = 1,
              n_clusters = 2, linkage = 'ward', affinity = 'euclidean'):

    style_change_borders = []
    starts_of_paragraphs = get_starts_of_paragraphs(paragraphs)
    if(method_name == 'Wilcoxon'):
        # doing Wilcoxon sign-rank test
        num_of_paragraphs = len(paragraphs)
        pvalues = {}
        for i in range(num_of_paragraphs - 1):
            stat, pvalue = wilcoxon(dataframe.iloc[i], dataframe.iloc[i + 1], zero_method = 'pratt', alternative = 'two-sided')
            pvalues[i + 1] = pvalue
        # sorting pvalues in increasing  order
        sorted_pvalues = sorted(pvalues.items(), key = operator.itemgetter(1))
        # defining % of suspicious parts
        p = allowed_portion
        S = int(p * num_of_paragraphs)
        if p != 1:
            S += 1
        # making a decision whether is a border
        for tpl in (sorted_pvalues[:S]):
            if tpl[1] <= alpha_value:
                style_change_borders.append(starts_of_paragraphs[tpl[0] + 1])                                # +1 cause the numeration of paragraphs starts at 1
        style_change_borders.sort()
        return style_change_borders
    if(method_name == 'AgglomerativeClustering'):
        if len(paragraphs) > 1:
            if linkage == 'ward':
                affinity = 'euclidean'
            model = AgglomerativeClustering(n_clusters = n_clusters, linkage = linkage, affinity = affinity)
            clusters = model.fit_predict(dataframe)
            for i in range(len(clusters) - 1):
                if clusters[i] != clusters[i + 1]:
                    style_change_borders.append(starts_of_paragraphs[i + 1 + 1])     # +1 cause the numeration of paragraphs starts at 1
        return style_change_borders

# punctuation tokenizer
punct_list = ['«', '»', '(', ')', '/', '\\',
              ',', '.', '․', ':', '։',
              '՝', '՟', '՚',
              '՜', '՛', '՞', '—']
def punct_tokenizer(text):
    punct_tokens = []
    for item in text:
        if item in punct_list:
            punct_tokens.append(item)
    return punct_tokens

# stopwords tokenizer
stopwords_list = open('stopwords_hy.txt', encoding='utf-8').read().splitlines()
def stopword_tokenizer(text):
    word_tokens = tokenize(text)
    stopword_tokens = []
    for item in word_tokens:
        if item in stopwords_list:
            stopword_tokens.append(item)
    return stopword_tokens

# POS tokenizer
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
                paragraphs = get_paragraphs_of(path + '/' + file)
                starts_of_paragraphs = get_starts_of_paragraphs(paragraphs)

            # 1.word tfidf
            word_vectorizer = TfidfVectorizer(tokenizer=tokenize)
            word_vectors = word_vectorizer.fit_transform(paragraphs)
            # 2.punctation tfidf
            punct_vectorizer = TfidfVectorizer(tokenizer=punct_tokenizer)
            punct_vectors = punct_vectorizer.fit_transform(paragraphs)
            # 3.POS tfidf
            pos_vectorizer = TfidfVectorizer(tokenizer=pos_tokenizer)
            pos_vectors = pos_vectorizer.fit_transform(paragraphs)
            # 4.stopwords tfidf
            stopword_vectorizer = TfidfVectorizer(tokenizer=stopword_tokenizer)
            stopword_vectors = stopword_vectorizer.fit_transform(paragraphs)
            # 5.3-grams tfidf
            three_gram_vectorizer = TfidfVectorizer(tokenizer=tokenize, ngram_range=(3, 3))
            three_gram__vectors = three_gram_vectorizer.fit_transform(paragraphs)

            # used features tf-idfs concatenating
            vectors = sp.hstack((word_vectors, punct_vectors, pos_vectors, stopword_vectors, three_gram__vectors), format='csr')
            # vectors = sp.hstack((word_vectors, pos_vectors, stopword_vectors), format='csr')
            denselist = (vectors.todense()).tolist()
            df = pd.DataFrame(denselist)

            style_change_borders = by_method(method_name = method_name, paragraphs = paragraphs, dataframe = df,
                                             allowed_portion = allowed_portion, alpha_value = alpha_value,
                                             n_clusters = n_clusters, linkage = linkage, affinity = affinity)

            # writing results
            with open(output_path + '/' + ('%s.truth' % filename), 'w') as o_f:
                json.dump({"positions": style_change_borders}, o_f, indent = 4)


method_for_files(test_files, 'par', method_name = 'Wilcoxon', allowed_portion = 1, alpha_value = 0.05)




