import os
import argparse
import pandas as pd
import pprint

from data_module import discussions as dcs
from data_module import data_manager as dm
from data_module.corpus import data_operations as do

pprinter = pprint.PrettyPrinter(width=140, indent=4)

DATA_FOLDER = os.path.join(
    os.path.dirname(__file__), 'data/microservices/')

USR_ANSWERS_FILE = DATA_FOLDER + 'usr_answers.csv'
USR_QUESTIONS_FILE = DATA_FOLDER + 'usr_questions.csv'

ANSWERS_FILE = DATA_FOLDER + 'raw/answers.csv'
QUESTIONS_FILE = DATA_FOLDER + 'raw/questions.csv'
UNION_FILE = DATA_FOLDER + 'raw/relevance_union.csv'

FALSE_POSITIVE_FILE = DATA_FOLDER + 'false_positive.csv'

# TECH_SIMPLE_FILE = 'data/technologies_simple.csv'
# TECH_COMPOUND_FILE = 'data/technologies_compound.csv'

TECH_SIMPLE_FILE = 'data/O_tech_simple.csv'
TECH_COMPOUND_FILE = 'data/O_tech_compound.csv'

# Load discussions dataframes
questions_df = pd.read_csv(QUESTIONS_FILE)
answers_df = pd.read_csv(ANSWERS_FILE)

usr_questions_df = pd.read_csv(USR_QUESTIONS_FILE)
usr_answers_df = pd.read_csv(USR_ANSWERS_FILE)

# Filter discussions in which the only answer was made by who asked the question
false_discussions = dcs.filter_no_discussions(
    questions_df, usr_answers_df, usr_questions_df)

discussions = questions_df.loc[~questions_df.Id.isin(false_discussions)]
discussions.fillna(0.0, inplace=True)

# metrics_union, q = dm.get_union(discussions, 3)
# metrics_union.set_index('Id', inplace=True)
# metrics_union.to_csv(UNION_FILE)
# metrics_union.to_csv('data/microservices/raw/relevance_intersection.csv')

union_data = pd.read_csv(UNION_FILE)

"""
User this section to filter non-related discussions
"""
# false_positve_ids = pd.read_csv(FALSE_POSITIVE_FILE)['Id']

# false_positives = union_data.loc[union_data.Id.isin(false_positve_ids)]

# valid_discussions = union_data.loc[~union_data.Id.isin(false_positve_ids)]
# valid_discussions.fillna(0.0, inplace=True)

"""end section"""


# Load Technologies data
tech_data = {}

tech_data["simple"] = list(pd.read_csv(TECH_SIMPLE_FILE)["tool"])
tech_data["compound"] = list(pd.read_csv(TECH_COMPOUND_FILE)["tool"])

tech_data["simple"] = list(map(lambda x: x.lower(), tech_data["simple"]))
tech_data["compound"] = list(map(lambda x: x.lower(), tech_data["compound"]))

# tech_ids, nontech_ids = do.filter_by_words(
#     valid_discussions, answers_df, tech_data["simple"], tech_data["compound"])

# tech_discussions = valid_discussions.loc[valid_discussions.Id.isin(tech_ids)]

# nontech_discussions = valid_discussions.loc[
#     valid_discussions.Id.isin(nontech_ids)]

"""
    Use this section to get data without non-related filtering
"""

tech_ids, nontech_ids = do.filter_by_words(
    union_data, answers_df, tech_data["simple"], tech_data["compound"])

tech_discussions = union_data.loc[union_data.Id.isin(tech_ids)]

nontech_discussions = union_data.loc[
    union_data.Id.isin(nontech_ids)]

print(len(nontech_discussions.index))
"""end section"""

# """
#     Uncomment the four line bellow to write results fo specific files,  
#     otherwise leave the comments to view the respctive data statistics
# """
# # tech_discussions.set_index('Id', inplace=True)
# # tech_discussions.to_csv(DATA_FOLDER + 'tech_discussions.csv')

# # nontech_discussions.set_index('Id', inplace=True)
# # nontech_discussions.to_csv(DATA_FOLDER + 'nontech_discussions.csv')


# """
#     Uncomment the code line bellow to see statistics, 
#     otherwise leave the comments to write data to files
# """
# data, quantiles = dm.get_union(discussions, 3)

# quantiles = quantiles.drop('Id')

# # Getting Tech discussions metrics
# metric_filter = dm.quantile_clustering(tech_discussions, quantiles)

# print("\n\nTech dicussions metrics\n\n")

# print("Metric\t\tTotal\t\tPercentual")
# for metric in metric_filter:
#     # Get number of metrics ocurrences
#     brute_value = len(metric_filter[metric])
#     corpus_relevance = brute_value / len(tech_discussions.index) * 100
    
#     pprinter.pprint((metric, brute_value, corpus_relevance))

#     # print( "%s\t\t\t%d\t\t\t%f" % (metric, brute_value, corpus_relevance))


# # Getting Non Tech discussions metrics
# metric_filter = dm.quantile_clustering(nontech_discussions, quantiles)

# print("\n\nNon Tech dicussions metrics\n\n")

# print("Metric\t\tTotal\t\tPercentual")
# for metric in metric_filter:
#     # Get number of metrics ocurrences
#     brute_value = len(metric_filter[metric])
#     corpus_relevance = brute_value / len(nontech_discussions.index) * 100
    
#     pprinter.pprint((metric, brute_value, corpus_relevance))

#     # print( "%s\t\t\t%d\t\t\t%f" % (metric, brute_value, corpus_relevance))


# # Getting False Positive discussions metrics
# metric_filter = dm.quantile_clustering(false_positives, quantiles)

# print("\n\nInvalid dicussions metrics\n\n")

# print("Metric\t\tTotal\t\tPercentual")
# for metric in metric_filter:
#     brute_value = len(metric_filter[metric])
#     corpus_relevance = brute_value / len(nontech_discussions.index) * 100
    
#     # print( "%s\t\t\t%d\t\t\t%f" % (metric, brute_value, corpus_relevance))
#     pprinter.pprint((metric, brute_value, corpus_relevance))


# print(len(nontech_discussions.index))
# print(len(tech_discussions.index))