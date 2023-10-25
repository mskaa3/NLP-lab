import os
from pathlib import Path
from time import sleep

import jsonlines
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from loguru import logger
from tqdm import tqdm

load_dotenv()


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "type key"
if DEVELOPER_KEY == "type key":
    print("Insert DEVELOPER_KEY")
    raise ValueError
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Wyszukiwanie !!!!
query = "pandoragate"

DATA_DIR = Path("data_nlp")

PUBLISHED_AFTER = "2023-10-01T00:00:00Z"
MAX_VIDEOS = 1000
MAX_COMMENTS_PER_VIDEO = 10000


def yt_vid_search(
    yt_api, q, count, published_after, max_results=50, parts="id,snippet", sleep_ts=0.5
):
    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = (
        yt_api.search()
        .list(
            q=q,
            part=parts,
            publishedAfter=published_after,
            regionCode="PL",
            maxResults=max_results,
        )
        .execute()
    )

    results = []
    total = 0
    # iterate video response
    while search_response:
        # extracting required info
        # from each result object
        for item in search_response["items"]:
            if total < count:
                total += 1
            else:
                search_response = False
                break
            if item["id"]["kind"] == "youtube#video":
                results.append(item)

        # Again repeat
        if search_response and "nextPageToken" in search_response:
            sleep(sleep_ts)
            search_response = (
                yt_api.search()
                .list(
                    q=q,
                    part=parts,
                    publishedAfter=published_after,
                    regionCode="PL",
                    maxResults=max_results,
                )
                .execute()
            )
        else:
            break

    return results


def fetch_video_comments(yt_api, video_id, count=10, max_q_results=100, sleep_ts=0.5):
    # empty list for storing reply
    total = 0
    comments = []
    # retrieve youtube video results
    video_response = (
        yt_api.commentThreads()
        .list(part="snippet,replies", videoId=video_id, maxResults=max_q_results)
        .execute()
    )

    # iterate video response
    while video_response:
        # extracting required info
        # from each result object
        for item in video_response["items"]:
            if total < count:
                comments.append(item)
                total += 1
            else:
                video_response = False
                break

        # Again repeat
        if video_response and "nextPageToken" in video_response:
            sleep(sleep_ts)
            video_response = (
                yt_api.commentThreads()
                .list(
                    part="snippet,replies",
                    videoId=video_id,
                    pageToken=video_response["nextPageToken"],
                    maxResults=max_q_results,
                )
                .execute()
            )
        else:
            break
    return comments


def main():
    yt_api = build(
        YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY
    )
    

    work_dir = DATA_DIR / "raw"
    query_dir = work_dir / Path(query)
    query_dir.mkdir(parents=True, exist_ok=True)

    videos_filepath = query_dir / "videos.jsonl"
    comments_filepath = query_dir / "comments.jsonl"

    videos = yt_vid_search(
        yt_api, count=MAX_VIDEOS, q=query, published_after=PUBLISHED_AFTER
    )
    with jsonlines.open(videos_filepath, mode="w") as writer:
        for video in videos:
            video["__search_query"] = query
            writer.write(video)

    with jsonlines.open(comments_filepath, mode="w") as writer:
        for video in tqdm(videos):
            try:
                raw_comments = fetch_video_comments(
                    yt_api, video["id"]["videoId"], count=MAX_COMMENTS_PER_VIDEO
                )
            except HttpError as e:
                if e.status_code == 403:
                    logger.warning(
                        f"Comments for video ({video['id']['videoId']}) are disabled."
                    )
                    continue
                raise e

            for comment in raw_comments:
                comment["__search_query"] = query
                writer.write(comment)


if __name__ == "__main__":
    main()
