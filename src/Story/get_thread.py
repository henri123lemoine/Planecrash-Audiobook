import aiohttp
from bs4 import BeautifulSoup
import json
from pathlib import Path

import os
import sys

import requests

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
from get_block import Block


def make_title(title):
    return title.replace(":", "-").replace("/", "_").replace("\\", "_").replace("<", "(").replace(">", ")").replace("*", "").replace("?", "").replace("|", "#")


class Thread:
    def __init__(self, url=None):
        self.title = ""
        self.authors = []
        self.characters = []
        self.url = ""
        self.blocks = []

        if url:
            self.extract(url)

    def __str__(self) -> str:
        blocks = "\n".join([str(block) for block in self.blocks])
        return f"Title: {self.title}\nAuthors: {self.authors}\nCharacters: {self.characters}\nURL: {self.url}\nBlocks:\n{blocks}"

    # async def async_extract(self, url: str):
    def extract(self, url: str):
        self.url = url
        resp = requests.get(self.url)
        html_content = resp.text

        html = BeautifulSoup(html_content, "html.parser")
        self.title = html.find("span", {"id": "post-title"}).text
        self.blocks = [Block(html_block) for html_block in html.find_all("div", {"class": ["post-container post-post", "post-container post-reply"]})]
        self.characters = list(set([block.character for block in self.blocks]))
        self.authors = list(set([block.author for block in self.blocks]))

    def to_json(self) -> dict:
        return {
            "title": self.title,
            "authors": self.authors,
            "characters": self.characters,
            "url": self.url,
            "blocks": [block.to_json() for block in self.blocks],
        }

    def save_json(self, path: str, indent: int=4):
        # Ensure the directories exist
        Path(path).mkdir(parents=True, exist_ok=True)

        # Create a valid filename
        file_name = make_title(self.title)

        file_path = f"{path}/{file_name}.json"
        with open(file_path, "w") as json_file:
            json.dump(self.to_json(), json_file, indent=indent)

    # @classmethod
    # def from_json(cls, path: str):
    #     with open(path, "r") as json_file:
    #         d = json.load(json_file)
    #     thread = cls()
    #     thread.title = d["title"]
    #     thread.authors = d["authors"]
    #     thread.characters = d["characters"]
    #     thread.url = d["url"]
    #     thread.blocks = [Block.from_json(block) for block in d["blocks"]]
    #     return thread

    @classmethod
    def from_json(cls, data: dict):
        thread = cls()
        thread.title = data["title"]
        thread.authors = data["authors"]
        thread.characters = data["characters"]
        thread.url = data["url"]
        thread.blocks = [Block.from_json(block_data) for block_data in data["blocks"]]
        return thread

    
if __name__ == "__main__":
    print("\n" * 5)

    JSON_PATH = "data/threads JSON"
    thread_url = 'https://glowfic.com/posts/4582?view=flat'

    # Extract the thread
    thread = Thread(thread_url)
    print("Extracted thread successfully")

    # Save the thread
    thread.save_json(f"{JSON_PATH}/tests")
    print("Saved thread successfully")

    # Load the thread
    file_path = f"{JSON_PATH}/tests/{thread.title}.json"
    thread = Thread.from_json(file_path)
    print("Loaded thread successfully")

    # Print number of blocks in thread
    print(f"Number of blocks in thread: {len(thread.blocks)}")
