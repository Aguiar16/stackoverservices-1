import os
import argparse
import pandas as pd
import json

from data_module import discussions as dcs
from data_module import data_manager as dm
from data_module.corpus import data_operations as do


DATA_FOLDER = os.path.join(
    os.path.dirname(__file__), 'data/microservices/raw/')

ANSWERS_FILE = DATA_FOLDER + 'answers.csv'
QUESTIONS_FILE = DATA_FOLDER + 'questions.csv'
UNION_FILE = DATA_FOLDER + 'relevance_union.csv'
INTERSECTION_FILE = DATA_FOLDER + 'relevance_intersection.csv'

sql_model = 'misc/microservcices_query_model.json'

# with open(sql_model, 'r') as jh:
#     query_details = json.load(jh)
#     print("QUERYING DISCUSSIONS")
#     dm.query_questions(query_details, QUESTIONS_FILE)

questions_ids = tuple(pd.read_csv(QUESTIONS_FILE)["Id"])

dm.query_answers(questions_ids, ANSWERS_FILE)

# parser = argparse.ArgumentParser(
#     description='Query and extract relevant data')

# parser.add_argument(
#     '-d', '--db_info', metavar='D', nargs=1,
#     type=str, help='JSON with the database data')

# args = vars(parser.parse_args())

# if args['db_info']:
#     details_path = args['db_info'][0]
#     query_details = {
#         "specs_file": details_path,
#         "QUESTIONS_FILE": QUESTIONS_FILE,
#         "ANSWERS_FILE": ANSWERS_FILE
#     }

#     dcs.query_data(query_details)
# else:
#     print("Missing parameter db_info")
