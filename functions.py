import requests
from bs4 import BeautifulSoup
import json
from typing import List, Tuple, Dict, Union, Optional

from settings import BOARD_URL, VOICE_DICT

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
    def __init__(self, character: str, content: str):
        self.character = character
        self.voice_name = VOICE_DICT.get(character)
        self.content = content
        self.len_content = len(self.content)
        self.voices = []

        # tag order list
        self.tag_order = []
        # text portions list
        self.text_portions = []
        """
        ex:
        content: "blabla1<tag1>blabla2<tag2>blabla3</tag2>blabla4</tag1>blabla5"
        tag_order: ["tag1", "tag2", "/tag2", "/tag1"]
        text_portions: ["blabla1", "blabla2", "blabla3", "blabla4", "blabla5"]
        """
        def get_tag_order(self):
            # get the tag order list
            # get the text portions list
            for tag in self.html_block.find_all(True):
                self.tag_order.append(tag.name)
                self.text_portions.append(tag.text)
            # remove the last tag
            self.tag_order.pop()
            # remove the first text portion
            self.text_portions.pop(0)
        

class Block:
    def __init__(self):
        self.html_block = BeautifulSoup("", "html.parser")
        self.character = ""
        self.screenname = ""
        self.author = ""
        self.icon_url = ""
        self.block_url = ""
        self.content = ""
        self.content_text = ""    
        self.voices = []    

    def __str__(self) -> str:
        voices = "\n\t".join([f"{voice[0]}: {voice[1]}" for voice in self.voices])
        block = f"""Character: {self.character}
Screenname: {self.screenname}
Author: {self.author}
Icon URL: {self.icon_url}
Block URL: {self.block_url}
Content: {self.content_text}
Voices:
    {voices}"""
        return block

    def extract(self, html_block: BeautifulSoup) -> "Block":
        # Extract the block information from the html block
        self.html_block = html_block
        self.character = character.text if (character:=self.html_block.find("div", {"class": "post-character"})) else None
        self.screenname = screenname.text if (screenname:=self.html_block.find("div", {"class": "post-screenname"})) else None
        self.author = self.html_block.find("div", {"class": "post-author"}).text.replace("\n", "")
        self.icon_url = icon.find("img")["src"] if (icon:=self.html_block.find("div", {"class": "post-icon"})) else None
        self.block_url = 'https://www.glowfic.com' + self.html_block.find("a", {"rel": "alternate"})["href"]
        self.html_block.find("a", {"rel": "alternate"})["href"]
        self.content = str(content) if (content:=self.html_block.find("div", {"class": "post-content"})) else None
        self.content_text = content.text if (content:=self.html_block.find("div", {"class": "post-content"})) else None
        self.voices = []#Voice(self.character, self.content_text).split_voice()
        return self

    def to_json(self) -> dict:
        return {
            "character": self.character,
            "screenname": self.screenname,
            "author": self.author,
            "icon_url": self.icon_url,
            "block_url": self.block_url,
            "content": self.content,
            "content_text": self.content_text,
            "voices": [[voice[0], voice[1]] for voice in self.voices],
            "html_block": str(self.html_block)
        }
    
    @staticmethod
    def load_from_json(d: dict) -> "Block":
        block = Block()
        block.html_block = BeautifulSoup(d["html_block"], "html.parser")
        block.character = d["character"]
        block.screenname = d["screenname"]
        block.author = d["author"]
        block.icon_url = d["icon_url"]
        block.block_url = d["block_url"]
        block.content = d["content"]
        block.content_text = d["content_text"]
        block.voices = [(voice[0], voice[1]) for voice in d["voices"]]
        return block
    

class Thread:
    def __init__(self):
        self.soup = BeautifulSoup("", "html.parser")
        self.title = ""
        self.authors = []
        self.characters = []
        self.thread_url = ""
        self.blocks = []
    
    def __str__(self) -> str:
        blocks = "\n".join([str(block) for block in self.blocks])

        thread = f"""Title: {self.title}
Authors: {self.authors}
Characters: {self.characters}
Thread URL: {self.thread_url}
Blocks:
{blocks}"""
        return thread
    
    def extract(self, thread_url: str) -> "Thread":
        # Extract the thread information from the Thread URL
        self.thread_url = thread_url
        self.html_thread = BeautifulSoup(requests.get(self.thread_url).content, "html.parser")
        self.title = self.html_thread.find("span", {"id": "post-title"}).text
        self.authors = list(set([t.text.replace("\n", "") for t in self.soup.find_all("div", {"class": "post-author"})]))
        self.characters = list(set([t.text for t in self.html_thread.find_all("div", {"class": "post-character"})]))
        self.blocks = [Block().extract(b) for b in self.html_thread.find_all("div", {"class": ["post-container post-post", "post-container post-reply"]})]
        return self
    
    def to_json(self) -> dict:
        # Convert the thread to a dictionary
        return {
            "title": self.title,
            "authors": self.authors,
            "characters": self.characters,
            "thread_url": self.thread_url,
            "blocks": [block.to_json() for block in self.blocks],
            "html_thread": str(self.html_thread)
        }

    @staticmethod
    def load_from_json(d: dict) -> "Thread":
        thread = Thread()
        thread.thread_url = d["thread_url"]
        thread.html_thread = BeautifulSoup(d["html_thread"], "html.parser")
        thread.title = d["title"]
        thread.authors = d["authors"]
        thread.characters = d["characters"]
        thread.thread_url = d["thread_url"]
        thread.blocks = [Block.load_from_json(block) for block in d["blocks"]]
        return thread


class Story:
    def __init__(self):
        self.soup = BeautifulSoup("", "html.parser")
        self.title = ""
        self.authors = []
        self.characters = []
        self.board_url = BOARD_URL
        self.threads = []
        
    def __str__(self):
        threads = "\n".join([str(thread) for thread in self.threads])

        story = f"""Title: {self.title}
Authors: {self.authors}
Characters: {self.characters}
Board URL: {self.board_url}
Threads:
{threads}"""
        return story
        
    def extract(self, board_url: str) -> "Story":
        # Extract the story information from the Board URL
        self.board_url = board_url
        self.board_html = BeautifulSoup(requests.get(self.board_url).content, "html.parser")
        self.title = self.board_html.find("title").text.split("|")[0].strip()
        tags = self.board_html.find_all("td", {"class": ["post-subject vtop odd", "post-subject vtop even"]})
        threads_links = ["https://glowfic.com" + t.find("a")["href"] + "?view=flat" for t in tags]#[6:7]
        self.threads = [Thread().extract(thread_link) for thread_link in threads_links]
        self.characters = list(set([character for thread in self.threads for character in thread.characters]))
        self.authors = list(set([author for thread in self.threads for author in thread.authors]))
        return self
    
    def to_json(self) -> dict:
        return {
            "title": self.title,
            "authors": self.authors,
            "characters": self.characters,
            "board_url": self.board_url,
            "threads": [thread.to_json() for thread in self.threads],
            "board_html": str(self.board_html)
        }

    def save_json(self, path: str, indent: int = 4) -> None:
        with open(path, "w") as json_file:
            json.dump(self.to_json(), json_file, indent=indent)

    def get_all_blocks(self) -> list:
        return [block for thread in self.threads for block in thread.blocks]
    
    def get_word_count(self) -> int:
        return sum([len(block.content_text.split()) for block in self.get_all_blocks()])
    
    @staticmethod
    def load_from_json(path: str):
        with open(path, "r") as json_file:
            d = json.load(json_file)
        story = Story()
        story.board_url = d["board_url"]
        story.board_html = BeautifulSoup(d["board_html"], "html.parser")
        story.title = d["title"]
        story.threads = [Thread.load_from_json(thread) for thread in d["threads"]]
        story.characters = d["characters"]
        story.authors = d["authors"]
        return story
    

