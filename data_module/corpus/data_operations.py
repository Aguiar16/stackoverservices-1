import re
import glob
import pandas as pd
import copy


class Corpus(object):
    """Docstring"""

    def __init__(self, docs_paths):
        self.corpus = []
        self.docs_names = docs_paths


    def load(self):
        """
        :return A list of Strings each one beeing a document
        """

        self.corpus = []
        
        
        for file_name in self.docs_names:

            with open(file_name, 'r') as fh:
                new_discussion = {}
                
                text = fh.read().split("\n\n")
                
                new_discussion["id"] = file_name[-12:-4]
                new_discussion["question_title"] = text[0]
                new_discussion["question_body"] = text[1]
                new_discussion["answers"] = text[2:]

                self.corpus.append(new_discussion)


    def get_discussions_text(self):
        """docstring"""
        
        text = []
        
        for discussion in self.corpus:

            doc = discussion["question_title"] + " " +\
                  discussion["question_body"] + " " +\
                  " ".join(discussion["answers"])
            
            text.append(doc)
            
        return text


    def corpus_word_frequency(self):
        """docstring"""

        corpus_text = self.get_discussions_text()

        bag_of_words = " ".join(corpus_text).split()
        tokens = set(bag_of_words)

        words_by_doc = {}

        for doc in corpus_text:
            text = doc.split()

            for word in tokens:
                if word in text:
                    if word in words_by_doc.keys():
                        words_by_doc[word] += 1
                    else:
                        words_by_doc[word] = 1

        return words_by_doc


    def export_pruned(self, limits, destination):
        """doctring"""

        if not self.corpus:
            print("A corpus need to loaded first")
            return
        
        upper_prunning = None
        lower_prunning = None

        word_count = self.corpus_word_frequency()

        word_count_df = pd.DataFrame.from_dict(
            word_count, orient="index", columns=["w_count"])
        
        if "upper" in limits.keys():
            upper_prunning = word_count_df.loc[
                word_count_df.w_count > limits["upper"]
            ]

        if "lower" in limits.keys():
            lower_prunning = word_count_df.loc[
                word_count_df.w_count < limits["lower"]
            ]
        
        print(list(upper_prunning.index))

        for doc in self.corpus:
            file_name = destination + "instance_" + doc["id"] + ".txt"
            
            question_title = doc["question_title"]
            question_body = doc["question_body"]
            answers = doc["answers"]

            if "upper" in limits.keys():
                question_title = " ".join(
                    [word for word in question_title.split() if word not in list(upper_prunning.index)])
                
            
                question_body = " ".join(
                    [word for word in question_body.split() 
                        if word not in list(upper_prunning.index)])
                
                answers = [
                    [word for word in answer.split() 
                        if word not in list(upper_prunning.index)]
                    for answer in answers
                ]
                answers = [" ".join(txt) for txt in answers if txt]
                        
            if "lower" in limits.keys():
                question_title = " ".join(
                    [word for word in question_title.split() 
                        if word not in list(lower_prunning.index)])
            
                question_body = " ".join(
                    [word for word in question_body.split() 
                        if word not in list(lower_prunning.index)])
                
                answers = [
                    [word for word in answer.split() 
                        if word not in list(lower_prunning.index)]
                    for answer in answers
                ]
                answers = [" ".join(txt) for txt in answers if txt]
            
            with open(file_name, 'w') as fh:
                fh.write(question_title)
                fh.write("\n\n" + question_body)
                
                for answer in answers:
                    fh.write("\n\n" + answer)
            
            print("Writed " + doc["id"])

        return upper_prunning, lower_prunning


def remove_single_quotes(word):
    word = word.strip()
    
    if word[0] == "'" and word[-1] == "'":
        word = word[1:-1]
    
    return word


def remove_block_tag(tags_exp, text):
    """
    Receives a text and tag pair for oppening and closing 
    and eliminates all ocurrences of the tags and its text
    in between. The tags must be passed as regex.
    """
    
    tag_open, tag_close = tags_exp[0], tags_exp[1]
    
    while True:
        start_match = re.search(tag_open, text)
        end_match = re.search(tag_close, text)

        if not (start_match and end_match):
            break
        
        text = text[:start_match.start()] + " " + text[end_match.end():]
    return text


def remove_single_tag(tag_exp, text):
    """
    Receives a tag as regex and remove all ocurrences in the text.
    """
    
    while True:
        matched = re.search(tag_exp, text)
        if not matched: break
        text = text[:matched.start()] + " " + text[matched.end():]
    
    return text


def filter_by_words(questions_df, answers_df, simple_words, compound_words):
    """ docstring """

    matched_ids = []
    not_matched_ids = []

    simple_word_set = set(simple_words)

    punctuation_rgx = r"[^()[\]<>+\-_=\*|\^{}$&%#@!?.,:;/\"]+"


    for index, row in questions_df.iterrows():

        found_flag = False

        title = row.Title.lower()

        in_title_compound = [
            True if re.compile(compound_word).search(title) else False 
            for compound_word in compound_words]
        
        clean_text = re.findall(punctuation_rgx, title)
        clean_text = [word for line in clean_text for word in line.split()]
        clean_text = list(map(remove_single_quotes, clean_text))
        
        simple_matched = simple_word_set.intersection(set(clean_text))
        in_title_simple = [True] * len(simple_matched)
        in_title = in_title_compound + in_title_simple

        if any(in_title):
            found_flag = True
        else:

            body = row.Body.lower()

            in_body_compound = [
                True if re.compile(compound_word).search(body) else False 
                    for compound_word in compound_words]
            
            clean_text = re.findall(punctuation_rgx, body)
            clean_text = [word for line in clean_text for word in line.split()]
            clean_text = list(map(remove_single_quotes, clean_text))

            simple_matched = simple_word_set.intersection(set(clean_text))
            in_body_simple = [True] * len(simple_matched)
            in_body = in_body_compound + in_body_simple

            if any(in_body):
                found_flag = True
            else:
                answers = answers_df.loc[answers_df.ParentId == row.Id]

                for idx, line in answers.iterrows():
                    
                    answer = line.Body.lower()

                    in_answers_compound = [
                        True if re.compile(compound_word).search(answer) else
                        False for compound_word in compound_words]
                    
                    clean_text = re.findall(punctuation_rgx, answer)
                    clean_text = [
                        word for line in clean_text for word in line.split()]
                    clean_text = list(map(remove_single_quotes, clean_text))

                    simple_matched = simple_word_set.intersection(
                        set(clean_text))
                    in_answers_simple = [True] * len(simple_matched)
                    in_answers = in_answers_compound + in_answers_simple

                    if any(in_answers):
                        found_flag = True
                        break
        
        if found_flag:
            matched_ids.append(row.Id)
        else:
            not_matched_ids.append(row.Id)
        
    return matched_ids, not_matched_ids

