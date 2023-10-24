import configparser
import json
import os.path
import time
import warnings

import pandas as pd
import praw
from prawcore import TooManyRequests
from tqdm.auto import tqdm

import const

warnings.filterwarnings("ignore")


def scrape_subreddits_by_keywords(
    df_scraped: pd.DataFrame, subreddits: list, keywords: list[str]
) -> pd.DataFrame:
    for subreddit in tqdm(subreddits, desc="Subreddits"):
        for keyword in tqdm(keywords, desc="Keywords", leave=False):
            while True:
                try:
                    for submission in subreddit.search(keyword, sort="hot"):
                        post_id = submission.id
                        title = submission.title
                        text = submission.selftext
                        subreddit_title = submission.subreddit.title

                        df_scraped = pd.concat(
                            [
                                df_scraped,
                                pd.DataFrame(
                                    [
                                        {
                                            "post_id": post_id,
                                            "title": title,
                                            "text": text,
                                            "subreddit_title": subreddit_title,
                                            "keyword": keyword,
                                        }
                                    ]
                                ),
                            ],
                            ignore_index=True,
                        )
                    break
                except TooManyRequests:
                    print("Too many requests. Waiting for a minute...")
                    time.sleep(60)
    return df_scraped


if __name__ == "__main__":
    if os.path.exists("config.ini"):
        config = configparser.ConfigParser()
        config.read("config.ini")

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
    elif os.path.exists("credentials.json"):
        with open("credentials.json", "r") as json_file:
            credentials = json.load(json_file)

        client_id = credentials["client_id"]
        client_secret = credentials["client_secret"]
        user_agent = credentials["user_agent"]

        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
        )
    else:
        raise ValueError("Please provide credentials to Reddit API in root directory")

    # every active Polish politics related subreddits
    subreddit_array = [
        reddit.subreddit("Polska"),
        reddit.subreddit("PolskaPolityka"),
        reddit.subreddit("lewica"),
        reddit.subreddit("libek"),
        reddit.subreddit("ShitKonfaSays"),
    ]

    # common political topics
    keywords = [
        "Platforma Obywatelska",
        "Koalicja Obywatelska",
        "Morawiecki",
        "Kaczyński",
        "Mentzen",
        "Tusk",
        "Hołownia",
        "Kukiz",
        "Wybory",
        "Wybory 2023",
        "Referendum",
        "CPK",
        "Aborcja",
        "Konfederacja",
        "Trzecia Droga",
        "Inflacja",
        "Gospodarka",
        "Prawo i Sprawiedliwość",
    ]

    reddit_scrapped_file_path = os.path.join(const.DATA_PATH, "reddit_scraped.feather")
    if not os.path.exists(reddit_scrapped_file_path):
        print(f"Creating {reddit_scrapped_file_path}")
        df = pd.DataFrame(
            columns=["post_id", "title", "text", "subreddit_title", "keyword"]
        )
    else:
        print(
            f"File {reddit_scrapped_file_path} already exists. New posts are going to be appended"
        )
        df = pd.read_feather(reddit_scrapped_file_path)

    length_before_scraping = len(df)

    df = scrape_subreddits_by_keywords(
        df_scraped=df, subreddits=subreddit_array, keywords=keywords
    )
    length_after_scraping = len(df)

    df = df.drop_duplicates(subset="post_id").reset_index(drop=True)
    length_after_dropping_duplicates = len(df)

    print(
        f"Dataset size changed from {length_before_scraping} to {length_after_dropping_duplicates}"
    )
    print(
        f"Downloaded {length_after_scraping-length_before_scraping} out of which {length_after_scraping-length_after_dropping_duplicates} were already duplicates"
    )

    df.to_feather(
        os.path.join(const.DATA_PATH, "reddit_scraped.feather"),
    )
