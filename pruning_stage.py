import os
import glob
import pandas as pd


from data_module.corpus import data_operations as do


########################### EXECUTION STARTS BELLOW ############################


DATA_FOLDER = os.path.join(
    os.path.dirname(__file__), 'data/microservices/')

TECH_FILES = glob.glob(DATA_FOLDER + 'clean/tech/*.txt')
NONTECH_FILES = glob.glob(DATA_FOLDER + 'clean/nontech/*.txt')

upper_limit = len(NONTECH_FILES) * 0.8
lower_limit = len(NONTECH_FILES) * 0.02

corpus = do.Corpus(NONTECH_FILES)
corpus.load()

corpus.export_pruned(
    {
        "upper": upper_limit,
        "lower": lower_limit
    },
    DATA_FOLDER + 'clean/pruned/nontech/U_80_L_2/'
)
