import configparser
import time
import warnings

import pandas as pd
import praw
from prawcore import TooManyRequests
from tqdm.auto import tqdm

warnings.filterwarnings("ignore")


def scrape_keywords(df, keywords=None):
    if keywords is None:
        keywords = [
            "Platforma Obywatelska",
            "Koalicja Obywatelska",
            "Morawiecki",
            "Kaczyński",
            "Mentzen",
            "Tusk",
            "Wybory",
            "Wybory 2023",
            "Konfederacja",
            "Trzecia Droga",
            "Inflacja",
            "Gospodarka",
            "Prawo i Sprawiedliwość",
            "Lewica",
            "CPK",
            "referendum",
            "głosowanie",
            "PSL",
            "aborcja",
        ]
    for subreddit in tqdm(subreddit_array, desc="Subreddits"):
        for keyword in tqdm(keywords, desc="Keywords", leave=False):
            while True:
                try:
                    for submission in subreddit.search(keyword, sort="hot"):
                        try:
                            submission.comments.replace_more(limit=None)
                            commenters_id = [
                                [
                                    comment.author.name
                                    for comment in submission.comments.list()
                                    if comment.author is not None
                                ]
                            ]
                            date = pd.to_datetime(submission.created_utc, unit="s")
                            df = pd.concat(
                                [
                                    df,
                                    pd.DataFrame(
                                        {
                                            "subreddit": [subreddit.display_name],
                                            "title": submission.title,
                                            "selftext": submission.selftext,
                                            "author_name": submission.author.name,
                                            "upvote_ratio": submission.upvote_ratio,
                                            "ups": submission.ups,
                                            "downs": submission.downs,
                                            "score": submission.score,
                                            "date": date,
                                            "post_id": submission.id,
                                            "num_comments": submission.num_comments,
                                            "keyword": keyword,
                                            "commenters_id": commenters_id,
                                        }
                                    ),
                                ],
                                ignore_index=True,
                            )
                        except AttributeError as e:
                            print(f"{e}, author field not present")
                    break
                except TooManyRequests as tmre:
                    time.sleep(60)
                    print("waiting")
    return df


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("../config.ini")

    client_id = config["reddit"]["client_id"]
    secret_key = config["reddit"]["secret_key"]
    pw = config["reddit"]["pw"]

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=secret_key,
        password=pw,
        user_agent="MyAPI/0.0.1",
        username="repcak2000",
    )

    subreddit_array = [
        reddit.subreddit("lewica"),
        reddit.subreddit("libek"),
        reddit.subreddit("PolskaPolityka"),
        reddit.subreddit("Polska"),
        reddit.subreddit("ShitKonfaSays"),
    ]

    keywords = [
        "Platforma Obywatelska",
        "Koalicja Obywatelska",
        "Morawiecki",
        "Kaczyński",
        "Mentzen",
        "Tusk",
        "Wybory",
        "Wybory 2023",
        "Konfederacja",
        "Trzecia Droga",
        "Inflacja",
        "Gospodarka",
        "Prawo i Sprawiedliwość",
    ]

    df = pd.DataFrame(
        columns=[
            "subreddit",
            "title",
            "selftext",
            "author_name",
            "upvote_ratio",
            "ups",
            "downs",
            "score",
            "date",
            "post_id",
            "num_comments",
            "likes",
            "commenters_id",
        ]
    )
    df = scrape_keywords(df)
    df = df.drop_duplicates(subset="post_id").reset_index(drop=True)
    df.to_json(
        "../data/redditScrapped.json", orient="records", force_ascii=False, indent=4
    )
    # df.to_feather("../data/redditScrapped.feather")
