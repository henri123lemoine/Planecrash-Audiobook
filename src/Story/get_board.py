import os
from bs4 import BeautifulSoup
import requests
import json
from tqdm import tqdm
from pathlib import Path

try:
    from .get_thread import Thread
except ImportError:
    from get_thread import Thread


class Board:
    def __init__(self, url=None):
        self.title = ""
        self.authors = []
        self.characters = []
        self.url = ""
        self.threads = []

        if url:
            self.extract(url)

    def __str__(self):
        threads = "\n".join([str(thread) for thread in self.threads])
        return f"Title: {self.title}\nAuthors: {self.authors}\nCharacters: {self.characters}\nURL: {self.url}\nThreads:\n{threads}"

    def extract(self, url: str):
        self.url = url
        html = BeautifulSoup(requests.get(self.url).content, "html.parser")
        self.title = html.find("title").text.split("|")[0].strip()
        tags = html.find_all("td", {"class": ["post-subject vtop odd", "post-subject vtop even"]})
        threads_links = ["https://glowfic.com" + t.find("a")["href"] + "?view=flat" for t in tags]

        self.threads = [Thread(thread_link) for thread_link in tqdm(threads_links, desc='Extracting threads')]

        self.characters = list(set([character for thread in self.threads for character in thread.characters]))
        self.authors = list(set([author for thread in self.threads for author in thread.authors]))

    def save_chunks(self, path: str, chunk_size: int = 200):
        all_blocks = []
        for thread in self.threads:
            all_blocks.extend(thread.blocks)

        num_chunks = (len(all_blocks) + chunk_size - 1) // chunk_size

        # Ensure the directories exist
        Path(path).mkdir(parents=True, exist_ok=True)

        for i in range(num_chunks):
            chunk = all_blocks[i * chunk_size : (i + 1) * chunk_size]
            chunk_title = f"{self.title}_chunk_{i + 1}_of_{num_chunks}"
            file_name = f"{path}/{chunk_title}.json"
            with open(file_name, "w") as json_file:
                json.dump([block.to_json() for block in chunk], json_file, indent=4)

    def to_json(self) -> dict:
        return {
            "title": self.title,
            "authors": self.authors,
            "characters": self.characters,
            "url": self.url,
            "threads": [thread.to_json() for thread in self.threads],
        }

    def save_json(self, path: str, indent: int=4):
        os.makedirs(path, exist_ok=True)
        with open(f"{path}/board.json", "w") as json_file:
            json.dump(self.to_json(), json_file, indent=indent)

    @classmethod
    def from_json(cls, path: str):
        with open(f"{path}/board.json", "r") as json_file:
            d = json.load(json_file)
        board = cls()
        board.title = d["title"]
        board.authors = d["authors"]
        board.characters = d["characters"]
        board.url = d["url"]
        board.threads = [Thread.from_json(thread_data) for thread_data in d["threads"]]
        return board

if __name__ == "__main__":
    print("\n"*5)
    
    BOARD_URL = "https://glowfic.com/board_sections/703"

    # Extract the board
    board = Board(BOARD_URL)
    print("Extracted board successfully")

    # Save the board
    JSON_PATH_test = "data/threads JSON/tests"
    board.save_json(JSON_PATH_test)
    print("Saved board successfully")

    # Load the board
    board = Board.from_json(JSON_PATH_test)
    print("Loaded board successfully")
    
    # Save the chunks
    board.save_chunks("data/board_chunks")
    print("Saved chunks successfully")

