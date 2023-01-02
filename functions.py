import requests
from bs4 import BeautifulSoup
import json
import re
import os
from typing import List, Tuple, Dict, Union, Optional

from settings import BOARD_URL, VOICE_DICT
from Story.helper_functions import make_title, process_voice_content

"""
The format of the Glowfic board is as follows:
Story
    Title
    Authors
    Characters
    Board URL
    Threads:
        Thread 1
            Title
            Authors
            Character
            Thread URL
            Blocks:
                Block 1
                    Character
                    Screenname
                    Author
                    Icon
                    Block URL
                    Content
                    Content Text
                    Voices
                etc.
        etc.

The story information is stored in the Story class.
It contains a title string, an authors list, a characters list, a board url string, and threads (found at the board url).

The threads information is stored in the Thread class.
It contains a title string, an authors list, a characters list, a thread url string, and blocks (found at the thread url).

The blocks information is stored in the Block class.
It contains a character string, an screenname string, an author string, an icon url string, a block url string, a content string (containing html describing the block), a content text string (containing only the story-text part of the html), and a list of voice-text tuples (each containing the name of the character (including narrator) that says what text).

1. Get the Story
    1.1. Get the title
    1.2. Get the authors
    1.3. Get the characters
    1.4. Get the board url
    1.5. Get the threads
        1.5.1. Get the title
        1.5.2. Get the authors
        1.5.3. Get the characters
        1.5.4. Get the thread url
        1.5.5. Get the blocks
            1.5.5.1. Get the character
            1.5.5.2. Get the screenname
            1.5.5.3. Get the author
            1.5.5.4. Get the icon url
            1.5.5.5. Get the block url
            1.5.5.6. Get the content
            1.5.5.7. Get the content text
            1.5.5.8. Get the voices
2. Save the Story to a pretty json file
3. Save the Story to a pickle file
"""
class Voice:
    def __init__(self) -> None:
        self.voice_name = ""
        self.content = ""
        self.len_content = 0
        self.tags, self.text_portions = [], []
        self.voices = []
    
    def __str__(self) -> str:
        voices = "\n".join([f"{voice[0]}: {voice[1]}" for voice in self.voices])
        voice = f"Character voice: {self.voice_name}\nVoices:\n{voices}"
        return voice

    def extract(self, character: str, content: str) -> "Voice":
        self.voice_name = VOICE_DICT.get(character)
        self.content = process_voice_content(content)
        self.len_content = len(self.content)
        self.tags, self.text_portions = self.extract_tags_and_text()
        self.voices = self.extract_voices()
        return self
    
    def to_json(self) -> dict:
        return {
            "": 0
        }

    def extract_tags_and_text(self) -> Tuple[List[str], List[str]]:
        tags = []
        text_portions = []
        
        # Find all tags in the input string
        tag_indices = []
        for tag in re.finditer(r'<[^<>]*>', self.content):
            tag_indices.append((tag.start(), tag.end()))
            tags.append(tag.group()[1:-1])
        
        # Extract the text portions between the tags
        start = 0
        for start_index, end_index in tag_indices:
            text_portions.append(self.content[start:start_index])
            start = end_index
        text_portions.append(self.content[start:])
        
        text_portions = [text.strip() for text in text_portions][1:]
        return tags, text_portions

    def extract_voices(self):# -> List[List[str, List[str]]]:
        voices = []
        tags_stack = []
        for i in range(len(self.tags)):
            tag = self.tags[i]
            if tag[0] == '/':
                tags_stack.pop()
            else:
                tags_stack.append(tag)
            voices.append([self.text_portions[i], tags_stack.copy()])

        voices = [voice for voice in voices if voice != ['', []]]
        return voices





class Block:
    def __init__(self):
        self.character = ""
        self.screenname = ""
        self.author = ""
        self.icon_url = ""
        self.url = ""
        self.content = ""
        self.voices = []    

    def __str__(self) -> str:
        voices = "\n\t".join([f"{voice[0]}: {voice[1]}" for voice in self.voices])
        return f"Character: {self.character}\nScreenname: {self.screenname}\nAuthor: {self.author}\nIcon URL: {self.icon_url}\nPermalink: {self.url}\nContent: {self.content}\nVoices:\n{voices}"

    def extract(self, html: BeautifulSoup) -> "Block":
        # Extract the block information from the html block
        self.character = character.text if (character:=html.find("div", {"class": "post-character"})) else None
        self.screenname = screenname.text if (screenname:=html.find("div", {"class": "post-screenname"})) else None
        self.author = html.find("div", {"class": "post-author"}).text.replace("\n", "")
        self.icon_url = icon.find("img")["src"] if (icon:=html.find("div", {"class": "post-icon"})) else None
        self.url = 'https://www.glowfic.com' + html.find("a", {"rel": "alternate"})["href"]
        html.find("a", {"rel": "alternate"})["href"]
        self.content = str(content) if (content:=html.find("div", {"class": "post-content"})) else ""
        self.voices = []
        return self

    def to_json(self) -> dict:
        return {
            "character": self.character,
            "screenname": self.screenname,
            "author": self.author,
            "icon_url": self.icon_url,
            "url": self.url,
            "content": self.content,
            "voices": [[voice[0], voice[1]] for voice in self.voices]
        }
    
    @staticmethod
    def load_from_json(d: dict) -> "Block":
        block = Block()
        block.character = d["character"]
        block.screenname = d["screenname"]
        block.author = d["author"]
        block.icon_url = d["icon_url"]
        block.url = d["url"]
        block.content = d["content"]
        block.voices = [(voice[0], voice[1]) for voice in d["voices"]]
        return block
    




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





class Story:
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
        
    def extract(self, url: str) -> "Story":
        # Extract the story information from the Board URL
        self.url = url
        html = BeautifulSoup(requests.get(self.url).content, "html.parser")
        self.title = html.find("title").text.split("|")[0].strip()
        tags = html.find_all("td", {"class": ["post-subject vtop odd", "post-subject vtop even"]})
        threads_links = ["https://glowfic.com" + t.find("a")["href"] + "?view=flat" for t in tags]#[:1]#[6:7]

        self.threads = [Thread().extract(thread_link) for thread_link in threads_links]
        self.characters = list(set([character for thread in self.threads for character in thread.characters]))
        self.authors = list(set([author for thread in self.threads for author in thread.authors]))
        return self
    
    def to_json(self) -> dict:
        return {
            "title": self.title,
            "authors": self.authors,
            "characters": self.characters,
            "url": self.url
        }

    def save_json(self, path: str, indent: int=4) -> None:
        with open(f"{path}/story.json", "w") as json_file:
            json.dump(self.to_json(), json_file, indent=indent)
        
        for thread in self.threads:
            thread.save_json(path, indent)

    @staticmethod
    def load_from_json(path: str):
        with open(f"{path}/story.json", "r") as json_file:
            story_d = json.load(json_file)
        thread_ds = [f"{path}/{thread}" for thread in os.listdir(path) if thread != "story.json"]

        story = Story()
        story.url = story_d["url"]
        story.title = story_d["title"]
        story.authors = story_d["authors"]
        story.characters = story_d["characters"]
        story.threads = [Thread.load_from_json(thread_d) for thread_d in thread_ds]
        return story
    
    def get_all_blocks(self) -> list:
        return [block for thread in self.threads for block in thread.blocks]
    
    def get_word_count(self) -> int:
        return sum([len(block.content_text.split()) for block in self.get_all_blocks()])
