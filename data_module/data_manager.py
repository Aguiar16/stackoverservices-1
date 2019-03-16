import pandas as pd

from .query_builder import QueryBuilder
from openpyxl import Workbook
from google.cloud import bigquery


def query_posts(query):
    """
    Query google's Big Query plataform

    Parameters
    ----------
    query : String
        SQL command for the specific database

    Returns
    -------
    Pandas.Dataframe
        DataFrame containing the rows resulted from the query

    See Also
    --------

    Examples
    --------

    """
    client = bigquery.Client()
    job = client.query(query)

    result = job.result().to_dataframe()
    result.set_index('Id', inplace=True)
    result.fillna(0.0, inplace=True)

    return result


def query_questions(query_details, output):
    """
    docstring
    """

    questions_query = QueryBuilder.build(query_details)
    questions = query_posts(questions_query)
    print("SAVING QUESTIONS")
    questions.to_csv(output)


def query_answers(questions_ids, output):
    """docstring"""

    answers_query = """
        SELECT Id, ParentId, "CreationDate", "Body"
            FROM `sotorrent-org.2018_09_23.Posts`
            WHERE ParentId IN """

    answers_query = answers_query +\
        " (" + ", ".join(len(questions_ids) * ["%s"]) + ")"

    answers_query = answers_query % questions_ids
    answers = query_posts(answers_query)
    print("SAVING ANSWERS")
    answers.to_csv(output)


def query_discussions(questions_details, questions_path, answers_path):
    """docstring"""

    query_questions(questions_details, questions_path)
    print("QUESTIONS QUERY COMPLETE")

    questions = pd.read_csv(questions_path)
    questions.set_index('Id', inplace=True)
    ids = tuple(questions.index.values)

    query_answers(ids, answers_path)
    print("ANSWERS QUERY COMPLETE")


def get_union(df, quantile, quantile_range='upper'):
    """
    Get part of the data above or below a determined quantile
    """

    if quantile == 1:
        q = df.quantile(q=0.25)
    elif quantile == 2:
        q = df.quantile(q=0.5)
    elif quantile == 3:
        q = df.quantile(q=0.75)
    else:
        print("Invalid quantile")
        return

    if quantile_range == 'upper':
        #data = df.loc[
        #    (df.AnswerCount > q.AnswerCount) |
        #    (df.ViewCount > q.ViewCount) |
        #    (df.CommentCount > q.CommentCount) |
        #    (df.FavoriteCount > q.FavoriteCount) |
        #    (df.Score > q.Score)
        #]
        data = df.loc[
            (df.AnswerCount > q.AnswerCount) &
            (df.ViewCount > q.ViewCount) &
            (df.CommentCount > q.CommentCount) &
            (df.FavoriteCount > q.FavoriteCount) &
            (df.Score > q.Score)
        ]
    elif quantile_range == 'lower':
        data = df.loc[
            (df.AnswerCount < q.AnswerCount) |
            (df.ViewCount < q.ViewCount) |
            (df.CommentCount < q.CommentCount) |
            (df.FavoriteCount < q.FavoriteCount) |
            (df.Score < q.Score)
        ]
    else:
        print('Ivalid range of data')
        data = None

    return data, q


def quantile_clustering(df, quantile_info):
    """docstring"""
    
    result = {}

    for index in quantile_info.index:
        filtered = df.loc[df[index] > quantile_info[index]]
        result[index] = list(filtered['Id'])
    
    return result


def build_review_sheet(sample_size, input_data, output):
    """docstring"""

    df = pd.read_csv(input_data)
    sample = df.sample(n=sample_size)

    wb = Workbook()
    ws = wb.active
    ws.append(["link", "reviewer", "comment"])

    reviewer = 'Matheus'
    count = 1

    for i, r in sample.iterrows():
        if count > 66:
            reviewer = 'Alan'

        if count > 33:
            reviewer = 'Paulo'

        link = "https://stackoverflow.com/questions/" + str(int(r['Id']))

        ws.append([link, reviewer])

        count += 1

    wb.save(output)
