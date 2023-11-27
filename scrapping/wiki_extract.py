import argparse
import json
import os
import re
import subprocess

import git
import jsonlines
import requests as req
from tqdm import tqdm

from const import DATA_PATH, EXTRACTED_PATH, RESULT_PATH, SCRIPTS_PATH


def create_files():
    """Create files for storing data extracted from wikidump and final converted data"""
    isExist = os.path.exists(EXTRACTED_PATH)
    if not isExist:
        try:
            os.mkdir(EXTRACTED_PATH)
        except OSError as error:
            print(f"Directory {EXTRACTED_PATH} can not be created")
    else:
        print(f"extracted_wikidumps directory already exist.")
    isExist = os.path.exists(RESULT_PATH)
    if not isExist:
        try:
            os.mkdir(RESULT_PATH)
        except OSError as error:
            print(f"Directory {RESULT_PATH} can not be created")
    else:
        print(f"final_wikidumps directory already exist.")


def get_wikiextractor():
    """If wikiextractor is not in the directory yet, downloads it and corrects imports"""
    isExist = os.path.exists(os.path.join(SCRIPTS_PATH, "wikiextractor"))
    if not isExist:
        with tqdm(
            desc="Downloading wikiextractor from github", total=1
        ) as progress_bar:
            git.Git(str(SCRIPTS_PATH)).clone(
                "https://github.com/attardi/wikiextractor.git"
            )

            with open(
                SCRIPTS_PATH + "/wikiextractor/wikiextractor/WikiExtractor.py"
            ) as f:
                lines = f.readlines()

            with open(
                SCRIPTS_PATH + "/wikiextractor/wikiextractor/WikiExtractorCorrected.py",
                "w",
            ) as sources:
                for line in lines:
                    if re.search("from .extract", line):
                        sources.write(
                            "from extract import Extractor, ignoreTag, define_template, acceptedNamespaces"
                        )
                    else:
                        sources.write(line)
            progress_bar.update(1)
    else:
        print(f"wikiextractor already downloaded.")


def get_extract_wikidump(wikidump: str):
    """Downloads patricular wikidump and extracts it to 'extracted' directory
    Parameters:
        ----------
                wikidump (str): adress of a wikidump.bz2 file in a following form:
        https://dumps.wikimedia.org/plwiki/20231020/plwiki-20231020-pages-articles-multistream.xml.bz2"
    """

    DUMP_NAME = wikidump.split("/")[-1]
    isExist = os.path.exists(DATA_PATH + "/" + DUMP_NAME)
    if not isExist:
        bzip_file = req.get(wikidump)
        with open(DATA_PATH + "/" + DUMP_NAME, "wb") as f:
            f.write(bzip_file.content)
    isExist = os.path.exists(os.path.join(SCRIPTS_PATH, "wikiextractor"))
    if isExist:
        run_stat = subprocess.run(
            [
                "python",
                # File to run
                str(
                    SCRIPTS_PATH
                    + "/wikiextractor/wikiextractor/WikiExtractorCorrected.py"
                ),
                # Processing parameters to get as json
                "--json",
                # Directory to store Extracted text
                "-o",
                str(EXTRACTED_PATH),
                # Archive file to extract from
                str(DATA_PATH + "/" + DUMP_NAME),
            ]
        )
    else:
        print("Wikiextractor not found in the directory")


def convert_files():
    """Read files from extracted wikidump and converts it to txt files named articleid_articletitle with matching metadata json file"""

    for files in os.listdir(EXTRACTED_PATH):
        file = os.path.join(EXTRACTED_PATH, files)
        for f in os.listdir(file):
            full_file_path = os.path.join(file, f)
            with jsonlines.open(full_file_path) as fp:
                for line in fp:
                    id = line["id"]
                    content = line["text"]
                    url = line["url"]
                    revid = line["revid"]
                    original_title = line["title"]
                    corrected_title = original_title.replace("/", "_")
                    corrected_title = re.sub(
                        r"[-()\"#/@;:<>{}`+=~|.!?,]", "_", original_title
                    )
                    with open(
                        RESULT_PATH + "/" + id + "_" + corrected_title,
                        "w",
                        encoding="utf8",
                    ) as new:
                        new.write(original_title)
                        new.write("\n")
                        new.write(content)

                    with open(
                        RESULT_PATH
                        + "/"
                        + id
                        + "_"
                        + corrected_title
                        + "_metadata.json",
                        "w",
                    ) as outfile:
                        metadata = {
                            "id": id,
                            "url": url,
                            "title": original_title,
                            "revid": revid,
                            "source": f,
                        }
                        json.dump(metadata, outfile)


if __name__ == "__main__":
    argument = argparse.ArgumentParser()
    argument.add_argument(
        "--wikidump",
        type=str,
        help="pass the wikidump adress f.e https://dumps.wikimedia.org/csbwiki/20230301/csbwiki-20230301-pages-articles-multistream.xml.bz2",
        default="def",
    )
    my_args = argument.parse_args()
    if my_args.wikidump != "def":
        wiki = my_args.wikidump
        create_files()
        get_wikiextractor()
        get_extract_wikidump(wiki)
        convert_files()
