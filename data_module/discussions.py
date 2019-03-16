import json
import pandas as pd

from .data_manager import query_discussions


def query_data(data_specs):
    """docstring"""
    
    with open(data_specs["specs_file"], 'r') as jh:
        query_details = json.load(jh)
        print("QUERYING DISCUSSIONS")
        query_discussions(
            query_details,
            data_specs["QUESTIONS_FILE"],
            data_specs["ANSWERS_FILE"])
        
        print("DISCUSSIONS QUERY COMPLETE")

def filter_no_discussions(questions_df, answers_df):
    """docstring"""

    not_dscs = []

    for idx, question in questions_df.iterrows():
        answers = answers_df.loc[answers_df.ParentId == question.Id]

        if len(answers.index) == 1:
            if answers.iloc[0].OwnerUserId == question.OwnerUserId:
                not_dscs.append(question.Id)

    return not_dscs        

# def filter_no_discussions(questions_df, answers_df, usrs_df):
#     """docstring"""

#     not_dscs = []

#     questions = usrs_df.loc[usrs_df.Id.isin(questions_df["Id"])]

#     for idx, question in questions.iterrows():
#         answers = answers_df.loc[answers_df.ParentId == question.Id]

#         if len(answers.index) == 1:
#             if answers.iloc[0].OwnerUserId == question.OwnerUserId:
#                 not_dscs.append(question.Id)

#     return not_dscs

