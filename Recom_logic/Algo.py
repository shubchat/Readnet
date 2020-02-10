from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys


def recos(db_name):

    engine = create_engine(f"postgresql:///{db_name}")
    stories = pd.read_sql_table("short_stories", engine)
    my_stop_words = text.ENGLISH_STOP_WORDS.union(
        [
            "gutenberg",
            "ebook",
            "online",
            "distributed",
            "transcriber",
            "etext",
            "note",
            "copyright",
            "start",
            "project",
            "end",
            "produced",
            "proofreading",
            "team",
            "http",
            "www",
            "pgdp",
            "net",
            "illustrated",
        ]
    )
    vectorizer = TfidfVectorizer(stop_words=my_stop_words)
    vectorizer.fit(stories["content"])
    X_vector = vectorizer.transform(stories["content"])
    similarity_matrix = cosine_similarity(X_vector)
    df_recos = pd.DataFrame(
        columns=[
            "bookno",
            "first_reco",
            "second_reco",
            "third_reco",
            "fourth_reco",
            "fifth_reco",
        ]
    )
    df_recos["bookno"] = np.array(stories["bookno"])
    i = 0
    while i <= df_recos.shape[0] - 1:

        df_recos.iloc[i] = np.take(
            np.array(stories["bookno"]), np.argsort(similarity_matrix)[:, -1:-7:-1][i]
        )
        i += 1

    df_recos.to_sql("recos", engine, if_exists="replace", index=False)

    return "Recommendations uploaded to DB"


if __name__ == "__main__":
    recos(sys.argv[1])

