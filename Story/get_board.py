from bs4 import BeautifulSoup
import requests
import json
import os
import asyncio
from get_thread import Thread




class Board:
    def __init__(self):
        self.soup = BeautifulSoup("", "html.parser")
        self.title = ""
        self.authors = []
        self.characters = []
        self.url = BOARD_URL
        self.threads = []
        
    def __str__(self):
        threads = "\n".join([str(thread) for thread in self.threads])
        return f"Title: {self.title}\nAuthors: {self.authors}\nCharacters: {self.characters}\nURL: {self.url}\nThreads:\n{threads}"
        
    def extract(self, url: str) -> "Board":
        # Extract the story information from the Board URL
        self.url = url
        html = BeautifulSoup(requests.get(self.url).content, "html.parser")
        self.title = html.find("title").text.split("|")[0].strip()
        tags = html.find_all("td", {"class": ["post-subject vtop odd", "post-subject vtop even"]})
        threads_links = ["https://glowfic.com" + t.find("a")["href"] + "?view=flat" for t in tags]

        self.threads = [Thread().extract(thread_link) for thread_link in threads_links]
        self.characters = list(set([character for thread in self.threads for character in thread.characters]))
        self.authors = list(set([author for thread in self.threads for author in thread.authors]))
        return self
    
    async def async_extract(self, url: str) -> "Board":
        # Extract the story information from the Board URL
        self.url = url
        html = BeautifulSoup(requests.get(self.url).content, "html.parser")
        self.title = html.find("title").text.split("|")[0].strip()
        tags = html.find_all("td", {"class": ["post-subject vtop odd", "post-subject vtop even"]})
        threads_links = ["https://glowfic.com" + t.find("a")["href"] + "?view=flat" for t in tags]#[:1]

        tasks = []
        for thread_link in threads_links:
            task = asyncio.create_task(Thread().async_extract(thread_link))
            tasks.append(task)

        self.threads = await asyncio.gather(*tasks)
        return self
    
    def to_json(self) -> dict:
        return {
            "title": self.title,
            "authors": self.authors,
            "characters": self.characters,
            "url": self.url
        }

    def save_json(self, path: str, indent: int=4) -> None:
        with open(f"{path}/board.json", "w") as json_file:
            json.dump(self.to_json(), json_file, indent=indent)
        
        for thread in self.threads:
            thread.save_json(path, indent)

    @staticmethod
    def load_from_json(path: str):
        with open(f"{path}/board.json", "r") as json_file:
            board_d = json.load(json_file)
        thread_ds = [f"{path}/{thread}" for thread in os.listdir(path) if thread != "board.json"]

        board = Board()
        board.url = board_d["url"]
        board.title = board_d["title"]
        board.authors = board_d["authors"]
        board.characters = board_d["characters"]
        board.threads = [Thread.load_from_json(thread_d) for thread_d in thread_ds]
        return board
    
    def get_all_blocks(self) -> list:
        return [block for thread in self.threads for block in thread.blocks]
    
    def get_word_count(self) -> int:
        return sum([len(block.content_text.split()) for block in self.get_all_blocks()])




if __name__ == "__main__":
    # Test the class
    # 1. Extract the story information from the Board URL
    # 2. Save the story information to a test JSON file
    # 3. Load the story information from the JSON file

    import time

    BOARD_URL = "https://glowfic.com/board_sections/703"

    JSON_PATH_test = "data/threads JSON/tests"

    async def main():
        start = time.time()
        board = await Board().async_extract(BOARD_URL)
        end = time.time()
        print(f"Extracted board successfully in {end - start:.2f} seconds")

        start = time.time()
        board.save_json(f"{JSON_PATH_test}")
        end = time.time()
        print(f"Saved board successfully in {end - start:.2f} seconds")

        start = time.time()
        board = Board.load_from_json(f"{JSON_PATH_test}")
        end = time.time()
        print(f"Loaded board successfully in {end - start:.2f} seconds")

    asyncio.run(main())