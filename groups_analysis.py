import os
import pandas as pd

from datetime import datetime
from data_module import data_manager as dm
from data_module.corpus import data_operations as do
from data_module.visualization import data_visualization as dv


DATA_FOLDER = os.path.join(
    os.path.dirname(__file__), 'data/microservices/')

QUESTIONS_FILE = DATA_FOLDER + 'raw/questions.csv'
TECHS_FILE = DATA_FOLDER + 'tech_discussions.csv'
NONTECHS_FILE = DATA_FOLDER + 'nontech_discussions.csv'
FALSE_POSITIVE_FILE = DATA_FOLDER + 'false_positive.csv'
UNIO_DATA = DATA_FOLDER + 'raw/relevance_union.csv'

questions = pd.read_csv(QUESTIONS_FILE, parse_dates=['CreationDate'])
tech_data = pd.read_csv(TECHS_FILE)
nontech_data = pd.read_csv(NONTECHS_FILE)
union_data = pd.read_csv(UNIO_DATA)


false_positive_ids = list(pd.read_csv(FALSE_POSITIVE_FILE)['Id'])
false_positive_data = union_data.loc[union_data.Id.isin(false_positive_ids)]


new_tech_data = questions.loc[questions.Id.isin(tech_data['Id'])]
new_nontech_data = questions.loc[questions.Id.isin(nontech_data['Id'])]
new_false_data = questions.loc[questions.Id.isin(false_positive_data['Id'])]


first_year = questions['CreationDate'].min().year
last_year = questions['CreationDate'].max().year

years = list(range(first_year, last_year+1))

category_data = {
    "Theoretical": [],
    "Tecnologic": [],
    "Non Related": []
}

for year in years:

    # Tech 
    tech_matched = [
        row['Id'] for idx, row in new_tech_data.iterrows() 
            if row["CreationDate"].year == year
    ]

    category_data["Tecnologic"].append(len(tech_matched))

    # NonTech
    nontech_matched = [
        row['Id'] for idx, row in new_nontech_data.iterrows() 
            if row["CreationDate"].year == year
    ]

    category_data["Theoretical"].append(len(nontech_matched))

    # NonRelated
    nonrelated_matched = [
        row['Id'] for idx, row in new_false_data.iterrows() 
            if row["CreationDate"].year == year
    ]

    category_data["Non Related"].append(len(nonrelated_matched))


dv.stacked_time_serie(category_data, map(str, years), "Discussions by Year")
