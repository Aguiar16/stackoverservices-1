import os
import pandas as pd
import nltk
import re
import spacy
import glob

from sklearn.feature_extraction.text import CountVectorizer
from data_module.corpus import data_operations as do


def get_top_n_words(corpus, n=None):
    """
    List the top n words in a vocabulary according 
    to occurrence in a text corpus.
    
    get_top_n_words(["I love Python", "Python is a language programming", 
    "Hello world", "I love the world"]) -> 
    [('python', 2),
     ('world', 2),
     ('love', 2),
     ('hello', 1),
     ('is', 1),
     ('programming', 1),
     ('the', 1),
     ('language', 1)]
    """

    vec = CountVectorizer().fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    
    words_freq = [
        (word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    
    return words_freq[:n]


########################### EXECUTION STARTS BELLOW ############################


nlp = spacy.load('en_core_web_sm')
# nlp = spacy.load('en')

DATA_FOLDER = os.path.join(
    os.path.dirname(__file__), 'data/microservices/')

RAW_ANSWERS_FILE = DATA_FOLDER + 'raw/answers.csv'

# change this data source to change the corpus
RAW_QUESTIONS_FILE = DATA_FOLDER + 'nontech_discussions.csv'

RAW_UNION_FILE = DATA_FOLDER + 'raw/relevance_union.csv'
CLEAN_UNION_FILE = DATA_FOLDER + 'clean/relevance_union.csv'

rawdata_answers = pd.read_csv(RAW_ANSWERS_FILE)
rawdata_questions = pd.read_csv(RAW_QUESTIONS_FILE)
rawdata_union = pd.read_csv(RAW_UNION_FILE)

open_tags = [
    r'&#xA;', r'&#xD;', r'<br>', r'<em>', r'</em>', r'<p>',
    r'</p>', r'<ul>', r'</ul>', r'<li>', r'</li>',
    r'<strong>', r'</strong>', r'<img src=[^>]*>',
    r'<blockquote>', r'</blockquote>', r'<ol>', r'</ol>', r'<hrs>'
    r'<sub>', r'</sub>', r'<h3>', r'</h3>', r'<h1>', r'</h1>', r'<h2>',
    r'</h2>', r'<h4>', r'</h4>', r'<h5>', r'</h5>', r'<div[^>]*>', r'</div>',
    r'<pre>', r'</pre>', r'<code>', r'</code>', r'<a href=[^>]*>',r'(</a>)',
    r'<br>', r'<br/>'
]

closed_tags = [
    (r'<a href=[^>]*>',r'(</a>)'),
    (r'<div[^>]*>',r'(</div>)'),
    (r'<code>', r'</code>'),
    (r'<blockquote>',r'</blockquote>')
]

stop_words = set(
    open('stopword_list.txt', 'r').read().replace("\n", " ").split()
)


dscs = rawdata_questions
punctuation_rgx = r"[^()[\]<>+\-_=\*|\^{}$&%#@!?.,:;/\"]+"

for idx, question in dscs.iterrows():

    file_name = 'instance_' + str(question["Id"]) + ".txt"

    file_path = DATA_FOLDER + 'clean/nontech/' + file_name

    with open(file_path, '+w') as fh:

        # Cleaning questions body
        for closed_tag in closed_tags:
            question["Body"] = do.remove_block_tag(closed_tag, question["Body"])
            
        for open_tag in open_tags:
            question["Body"] = do.remove_single_tag(open_tag, question["Body"])

        # Cleaning question title
        stage_one = re.findall(punctuation_rgx, question['Title'].lower())
        stage_one = [word for line in stage_one for word in line.split()]
        stage_one = list(map(do.remove_single_quotes, stage_one))
        
        stage_two = re.findall(r"[^\d]+", " ".join(stage_one))
        stage_two = [word for line in stage_two for word in line.split()]

        words_to_remove = stop_words.intersection(set(stage_two))

        stage_three = [
            word for word in stage_two if word not in words_to_remove]

        leemed_title = nlp(" ".join(stage_three))
        leemed_title = " ".join(
            [word.lemma_ for word in leemed_title 
                if word.lemma_ != "-PRON-" and word.lemma_ != "'s"])
        
        # Cleaning question body
        stage_one = re.findall(punctuation_rgx, question['Body'].lower())
        stage_one = [word for line in stage_one for word in line.split()]
        stage_one = list(map(do.remove_single_quotes, stage_one))

        stage_two = re.findall(r"[^\d]+", " ".join(stage_one))
        stage_two = [word for line in stage_two for word in line.split()]

        words_to_remove = stop_words.intersection(set(stage_two))

        stage_three = [
            word for word in stage_two if word not in words_to_remove]

        leemed_body = nlp(" ".join(stage_three))
        leemed_body = " ".join(
            [word.lemma_ for word in leemed_body 
                if word.lemma_ != "-PRON-" and word.lemma_ != "'s"])

        fh.write(leemed_title)
        fh.write('\n\n')
        fh.write(leemed_body)

        # Cleaning answers
        answers = rawdata_answers.loc[
            rawdata_answers.ParentId == question["Id"]]

        for idx, answer in answers.iterrows():
            for closed_tag in closed_tags:
                answer["Body"] = do.remove_block_tag(closed_tag, answer["Body"])
            
            for open_tag in open_tags:
                answer["Body"] = do.remove_single_tag(open_tag, answer["Body"])
            
            # Cleaning answer body
            stage_one = re.findall(punctuation_rgx, answer['Body'].lower())
            stage_one = [word for line in stage_one for word in line.split()]
            stage_one = list(map(do.remove_single_quotes, stage_one))
            
            stage_two = re.findall(r"[^\d]+", " ".join(stage_one))
            stage_two = [word for line in stage_two for word in line.split()]

            words_to_remove = stop_words.intersection(set(stage_two))

            stage_three = [
                word for word in stage_two if word not in words_to_remove]

            leemed_answer = nlp(" ".join(stage_three))
            leemed_answer = " ".join(
                [word.lemma_ for word in leemed_answer 
                    if word.lemma_ != "-PRON-" and word.lemma_ != "'s"])

            fh.write('\n\n')        
            fh.write(leemed_answer)

    print("Discussion %d printed" % question['Id'])
