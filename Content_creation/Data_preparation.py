import os
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys


def get_metadata():
    bookno = []
    Title = []
    Author = []
    Language = []
    content = []
    for a in os.listdir(path="books"):
        if a.endswith(".txt"):
            with open(f"books/{a}", "r+", errors="ignore") as f:
                text = f.read()
                Title1 = []
                Author1 = []
                Language1 = []
                for line in f:
                    y = line.split()
                    # raise Exception("The files is {}".format(f))
                    # print(len(y))
                    # if y[1]=='Title:':
                    if len(y) > 0 and y[0] == "Title:":
                        Title1 = y.copy()
                    if len(y) > 0 and y[0] == "Author:":
                        Author1 = y.copy()
                    if len(y) > 0 and y[0] == "Language:":
                        Language1 = y.copy()
            bookno.append(a)
            Title.append(Title1)
            Author.append(Author1)
            Language.append(Language1)
            content.append(text)
    df_books = pd.DataFrame()
    stories = pd.DataFrame(columns=["bookno", "content"])
    df_books["bookno"] = bookno
    df_books["title"] = [" ".join(T) for T in Title]
    df_books["author"] = [" ".join(A) for A in Author]
    df_books["lang"] = [" ".join(L) for L in Language]
    df_books["title"] = df_books["title"].str.lstrip("Title:")
    df_books["author"] = df_books["author"].str.lstrip("Author:")
    df_books["lang"] = df_books["lang"].str.lstrip("Language:")
    stories["bookno"] = bookno
    stories["content"] = content

    return df_books, stories


def push_metadata_todb(user_name, password, db_name):
    df_books, stories = get_metadata()
    con = psycopg2.connect(
        dbname="postgres", user=user_name, host="", password=password
    )
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
    engine = create_engine(f"postgresql:///{db_name}")
    df_books.to_sql("metadata", engine, if_exists="append", index=False)
    stories.to_sql("short_stories", engine, if_exists="append", index=False)
    return "Data uploaded to DB"


if __name__ == "__main__":
    push_metadata_todb(sys.argv[1], sys.argv[2], sys.argv[3])

# import psycopg2

# con = psycopg2.connect(dbname="postgres", user="shubyog", host="", password=test)

# con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# cur = con.cursor()
# cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier("test")))

