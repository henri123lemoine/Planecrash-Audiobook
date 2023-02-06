from bs4 import BeautifulSoup
import requests
import json
import asyncio
from get_block import Block
from helper_functions import make_title



class Thread:
    def __init__(self):
        self.soup = BeautifulSoup("", "html.parser")
        self.title = ""
        self.authors = []
        self.characters = []
        self.url = ""
        self.blocks = []
    
    def __str__(self) -> str:
        blocks = "\n".join([str(block) for block in self.blocks])
        return f"Title: {self.title}\nAuthors: {self.authors}\nCharacters: {self.characters}\nURL: {self.url}\nBlocks:\n{blocks}"
    
    def extract(self, url: str) -> "Thread":
        # Extract the thread information from the Thread URL
        self.url = url
        html = BeautifulSoup(requests.get(self.url).content, "html.parser")
        self.title = html.find("span", {"id": "post-title"}).text

        self.blocks = [Block().extract(b) for b in html.find_all("div", {"class": ["post-container post-post", "post-container post-reply"]})]
        self.characters = list(set([block.character for block in self.blocks]))
        self.authors = list(set([block.author for block in self.blocks]))
        return self
    
    async def async_extract(self, url: str) -> "Thread":
        # Extract the thread information from the Thread URL
        self.url = url
        html = BeautifulSoup(requests.get(self.url).content, "html.parser")
        self.title = html.find("span", {"id": "post-title"}).text

        tasks = []
        for b in html.find_all("div", {"class": ["post-container post-post", "post-container post-reply"]}):
            task = asyncio.create_task(Block().async_extract(b))
            tasks.append(task)

        self.blocks = await asyncio.gather(*tasks)
        self.characters = list(set([block.character for block in self.blocks]))
        self.authors = list(set([block.author for block in self.blocks]))
        return self
    
    def to_json(self) -> dict:
        # Convert the thread to a dictionary
        return {
            "title": self.title,
            "authors": self.authors,
            "characters": self.characters,
            "url": self.url,
            "blocks": [block.to_json() for block in self.blocks],
        }

    def save_json(self, path: str, indent: int=4) -> None:
        with open(f"{path}/{make_title(self.title)}.json", "w") as json_file:
            json.dump(self.to_json(), json_file, indent=indent)

    @staticmethod
    def load_from_json(path: str) -> "Thread":
        with open(path, "r") as json_file:
            d = json.load(json_file)
        thread = Thread()
        thread.title = d["title"]
        thread.authors = d["authors"]
        thread.characters = d["characters"]
        thread.url = d["url"]
        thread.blocks = [Block.load_from_json(block) for block in d["blocks"]]
        return thread



if __name__ == "__main__":
    # Test the class
    # 1. Extract a thread
    # 2. Save the thread
    # 3. Load the thread

    JSON_PATH = "data/threads JSON"
    
    thread_url = 'https://glowfic.com/posts/6322?view=flat'

    # Extract the thread
    thread = Thread().extract(thread_url)
    print("Extracted thread successfully")

    # Save the thread
    thread.save_json(f"{JSON_PATH}/tests")
    print("Saved thread successfully")

    # Load the thread
    thread = Thread.load_from_json(f"{JSON_PATH}/tests/{thread.title}.json")
    print("Loaded thread successfully")

