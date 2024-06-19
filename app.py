import os
import json
import sqlite3
import datetime
from pathlib import Path

import ollama
import urllib3
from dotenv import load_dotenv

def validate_or_create_tables(cursor):
    '''ensure db tables exist'''
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "articles" (
        "articleID"	INTEGER NOT NULL UNIQUE,
        "timestamp"	TEXT NOT NULL,
        "title"	TEXT NOT NULL UNIQUE,
        "description"	TEXT NOT NULL,
        "content"	TEXT NOT NULL UNIQUE,
        "processed"	INTEGER NOT NULL,
        PRIMARY KEY("articleID" AUTOINCREMENT)
    );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS "scores" (
        "scoreID"	INTEGER NOT NULL UNIQUE,
        "lastChange"	TEXT NOT NULL,
        "topic"	TEXT NOT NULL UNIQUE,
        "score"	REAL NOT NULL,
        PRIMARY KEY("scoreID" AUTOINCREMENT)
    );""")

def gnews_api_call(apikey, query = "food AND trend", lang = "en", countries = ["us"], pages = 1):
    MAX = 25
    EXPAND = "content"

    # Creating a PoolManager instance for sending requests.
    HTTP = urllib3.PoolManager()
    TIMESTAMP = f"{datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")}"

    articles = []

    for page in range(1, pages+1):
        for country in countries:
            url = f"https://gnews.io/api/v4/search?q={query}&lang={lang}&country={country}&max={MAX}&apikey={apikey}&page={page}&expand={EXPAND}"

            # Sending a GET request and getting back response as HTTPResponse object.
            response = HTTP.request("GET", url=url)

            # TODO: check if articles are returned or if asked for page too high
            
            with open("testing_output"+TIMESTAMP+" raw.txt", "a+", encoding="utf-8") as f:
                f.write(json.dumps(response.json(), indent=4))

            data = json.loads(response.data)
            articlesRaw = data["articles"]
            for article in articlesRaw:
                x = (article["title"], article["description"], article["content"])
                articles.append(x)
    
    return articles

def add_articles_to_db(cursor, con, articles):   
    for article in articles:
        title = article[0]
        description = article[1]
        content = article[2]

        # check if article already in db
        res = cursor.execute("SELECT * FROM articles WHERE title=?", [title])
        test = res.fetchall()
        if test:
            continue

        if not determine_if_article_relevant(article):
            continue #skips to the next iteration of the loop if article isnt relevant

        ts = f"{datetime.datetime.now()}"
        data = (ts, title, description, content)
        sql = "INSERT OR IGNORE INTO articles (timestamp, title, description, content, processed) VALUES (?, ?, ?, ?, 0);"
        cursor.execute(sql, data)
    
    con.commit()

def determine_if_article_relevant(article):
    prompt = f"""
Your job is to decide whether an article is about a culinary topic/produce/trend or not, for example: 

-Article about local grocery store closing: No
-Article about specific produce sales going up or down: yes
-Article about recall on The Psychology of Comfort Food: no
-Article about TikTok cooking trend: yes
-Article on Exploring Unusual Flavor Combinations: yes
-Article on The Impact of Food Packaging on Environmental Sustainability: no
-Article that Promotes a deal on Jr. Bacon Cheeseburgers at Wendy's: no
-Article that Discusses HPV vaccines and their impact on cancer prevention in men and women: no
-Article that Offers recipes for Father's Day brunch: no
-Article that Describes a new restaurant show called The Utility Show, focused on independent restaurants: no

The articles classified as "yes" are directly related to culinary topics, which include:

Food preparation and cooking techniques.
Trends in food consumption and culinary innovations.
Sales and popularity of specific produce.
Cultural or social trends related to food.

Common Trend for "No" Responses:
The articles classified as "no" are focused on topics adjacent to food but do not deal directly with culinary aspects such as:

Business operations related to food retail.
Psychological or environmental factors influencing food choices or packaging.
Non-culinary aspects of the food industry.

The ONLY response you should give is only one word PER ARTICLE: "YES" or "NO"

No more than a single word response to any one article I give you.

The article is:
{article}"""

    response = ollama.chat(model='llama3', messages=[
    {
        'role': 'user',
        'content': prompt,
    },
    ])

    print(response)
    if response.get("message", {}).get("content").lower() in ['yes', 'YES']:
        return True
    elif response.get("message", {}).get("content").lower() in ['no', 'NO']:
        return False
    else:
        return False

def main():
    # load api key into env
    load_dotenv(Path(".env"))

    # connect to db
    con = sqlite3.connect("app.db")
    cur = con.cursor()
    validate_or_create_tables(cur)

    articles = gnews_api_call(apikey=os.getenv("GNEWS_API_KEY"), countries=['us', 'ca'], pages=3)
    add_articles_to_db(cur, con, articles)
    print("done")

if __name__ == "__main__":
    main()