import os
from datetime import datetime

# general
DIRECTORY = os.getcwd()
DATA_PATH = os.path.join(DIRECTORY, "data")
SCRIPTS_PATH = os.path.join(DIRECTORY, "scrapping")

# wikipedia
EXTRACTED_PATH = os.path.join(DATA_PATH, "extracted_wikidumps")
RESULT_PATH = os.path.join(DATA_PATH, "final_wikidumps")
NUM_PAGES = 500

# wykop
WYKOP_URL = "https://wykop.pl/tag/"
DATE = datetime(2023, 1, 1).date()

# reddit
