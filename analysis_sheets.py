import os
import json
import argparse
import pandas as pd

from openpyxl import Workbook
from data_module import data_manager as dm
from data_module.corpus import data_operations as do


def techs_filter(questions_file, answers_file, techs, first_filter=None):
    """
    
    NOTE: When passing a value to first filter it is assumed that the union of
    the third quantile of each metric has been processed

    """

    answers_df = pd.read_csv(answers_file)
    questions_df = pd.read_csv(questions_file)
 
    techs["simple"] = list(map(lambda x: x.lower(), techs["simple"]))
    techs["compound"] = list(map(lambda x: x.lower(), techs["compound"]))
    
    questions_df.fillna(0.0, inplace=True)

    if first_filter:
        valid_data = questions_df.loc[~questions_df.Id.isin(first_filter)]
    else:
        valid_data, q = dm.get_union(questions_df, 3)
    
    matched, not_matched = do.filter_by_words(
        valid_data, answers_df, techs["simple"], techs["compound"])

    if 48921774 in matched:
        print("essa merda ainda tá aqui")
    else:
        print("deu bom")
    
    return questions_df.loc[questions_df.Id.isin(not_matched)]


def build_review_sheet(data_df, sample_size, output):
    """docstring"""

    if len(data_df.index) <= sample_size:
        data_sample = data_df
    else:
        data_sample = data_df.sample(n=sample_size)

    ids = list(data_sample['Id'])

    wb = Workbook()
    ws = wb.active
    ws.append(
        ["Discussion", "Reviewer", "Status",
        "Microservice Specific Technologies",
        "Microservice Related Technologies",
        "False Positives Discussions",
        "Comments"])

    reviewer = 'Alan'

    for id in ids:
        link = "https://stackoverflow.com/questions/" + str(id)
        ws.append([link, reviewer])

    wb.save(output)


DATA_FOLDER = os.path.join(
    os.path.dirname(__file__), 'data/microservices/')

ANSWERS_FILE = DATA_FOLDER + 'raw/answers.csv'
QUESTIONS_FILE = DATA_FOLDER + 'raw/questions.csv'
UNION_FILE = DATA_FOLDER + 'raw/relevance_union.csv'
INTERSECTION_FILE = DATA_FOLDER + 'raw/relevance_intersection.csv'

TECH_SIMPLE_FILE = 'data/technologies_simple.csv'
TECH_COMPOUND_FILE = 'data/technologies_compound.csv'

REVIEWED_FILE = 'data/reviewed_discussions.csv'

tech_data = {}

tech_data["simple"] = list(pd.read_csv(TECH_SIMPLE_FILE)["tool"])
tech_data["compound"] = list(pd.read_csv(TECH_COMPOUND_FILE)["tool"])

reviewed_data = list(pd.read_csv(REVIEWED_FILE)["Id"])

filtered_discussions = techs_filter(
    QUESTIONS_FILE, ANSWERS_FILE, tech_data)
    # 'data/filtered_non_tech.csv', ANSWERS_FILE, tech_data)
    # first_filter=reviewed_data)'

# build_review_sheet(
#     filtered_discussions, 100, 
#     '[ALAN] Technical discussions review - ROUND 6.xlsl')

# filtered_discussions.set_index('Id', inplace=True)

# filtered_discussions.to_csv('filtered_round6.csv')