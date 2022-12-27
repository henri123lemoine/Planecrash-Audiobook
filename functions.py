import requests
from bs4 import BeautifulSoup
import json
import unicodedata
import pickle

from settings import BOARD_URL

"""
The format of the Glowfic board is as follows:
Glowfic board
    Title
    Threads:
        Thread 1
            Title
            Authors
            Character
            Blocks:
                Block 1
                    Character - Screenname - Author - Icon - Content
                Block 2
                    Character - Screenname - Author - Icon - Content
                etc.
        Thread 2
        etc.

Every Glowfic board contains a title and threads.
Every thread contains a title, authors, characters, and blocks.
Blocks all contain an author, but the other fields are optional.

1. Get the Glowfic board (and all threads and blocks)
2. Separate long threads into episodes of roughly 30-60 minutes each (10,000 words)
3. Create a json file
"""

class Block:
    def __init__(self):
        self.character = ""
        self.screenname = ""
        self.author = ""
        self.url = ""
        self.icon_url = ""
        self.content = ""
        self.content_text = ""        

    def __str__(self):
        return f"Character: {self.character}\nScreenname: {self.screenname}\nAuthor: {self.author}\nIcon: {self.icon_url}\nContent: {self.content_text}"
    
    def __repr__(self):
        return f"{self.content}"

    def get_block(self, html_block):
        self.html_block = BeautifulSoup(str(html_block), "html.parser")
        self.url = self.html_block.find("a", {"rel": "alternate"})["href"]
        self.character = character.text if (character:=self.html_block.find("div", {"class": "post-character"})) else None
        self.screenname = screenname.text if (screenname:=self.html_block.find("div", {"class": "post-screenname"})) else None
        self.author = self.html_block.find("div", {"class": "post-author"}).text.replace("\n", "")
        self.icon_url = icon.find("img")["src"] if (icon:=self.html_block.find("div", {"class": "post-icon"})) else None
        self.content = str(content) if (content:=self.html_block.find("div", {"class": "post-content"})) else None
        self.content_text = content.text if (content:=self.html_block.find("div", {"class": "post-content"})) else None
        return self
    
    def to_json(self):
        d = {}
        d["character"] = self.character
        d["screenname"] = self.screenname
        d["author"] = self.author
        d["url"] = self.url
        d["icon_url"] = self.icon_url
        d["content"] = self.content
        d["content_text"] = self.content_text
        return d
    
    def get_word_count(self):
        return len(self.content_text.split()) if self.content_text else 0
    
    def split_voices(self):
        """
        Splits the block's html content into voices.
        Splits can occur when:
        - A quote is used (between "") -> the voice is the character who said the quote
        - A linebreak is used (between <br> tags) -> the voice is pause (0.2 seconds)
        - Elsewhere -> the voice is the narrator

        Whenever there is a **bold** effect (illustrated by <strong> tags) or a *italic* effect (illustrated by <em> tags), the voice the regular voice plus the effect.

        E.g.: He said, *entirely* unbegrudgingly: "I would never say it *that* way, you **idiot!!**".
        This would be split into 4 voices voices:
        - "He said, ": narrator
        - "entirely": narrator + italic
        - " unbegrudgingly: narrator
        - "I would never say it ": character
        - "that": character + italic
        - " way, you ": character
        - "idiot!!": character + bold

        Returns a list of voice tuples (voice, effects, text)
        """
        pass
    
    @staticmethod
    def load_from_json(d):
        block = Block()
        block.character = d["character"]
        block.screenname = d["screenname"]
        block.author = d["author"]
        block.url = d["url"]
        block.icon_url = d["icon_url"]
        block.content = d["content"]
        block.content_text = d["content_text"]
        return block
    

class Thread:
    def __init__(self):
        self.title = ""
        self.authors = []
        self.characters = []
        self.blocks = []
    
    def __str__(self):
        return f"Title: {self.title}\nAuthors: {self.authors}\nCharacters: {self.characters}\nBlocks count: {len(self.blocks)}\nURL: {self.url}"
    
    def __repr__(self):
        blocks = '\n'.join(repr(block) for block in self.blocks)
        return f"|{self.title}|{self.authors}|{self.characters}|\n{blocks}"

    def get_thread(self, url: str):
        self.url = url
        page = requests.get(self.url)
        self.soup = BeautifulSoup(page.content, "html.parser")
        self.title = self.soup.find("span", {"id": "post-title"}).text
        self.blocks = [Block().get_block(b) for b in self.soup.find_all("div", {"class": ["post-container post-post", "post-container post-reply"]})]
        self.authors = list(set([t.text.replace("\n", "") for t in self.soup.find_all("div", {"class": "post-author"})]))
        self.characters = list(set([t.text for t in self.soup.find_all("div", {"class": "post-character"})]))
        return self

    def to_json(self) -> dict:
        d = {}
        d["title"] = self.title
        d["authors"] = self.authors
        d["characters"] = self.characters
        d["url"] = self.url
        d["blocks"] = [block.to_json() for block in self.blocks]
        return d

    def get_word_count(self) -> int:
        return sum([block.get_word_count() for block in self.blocks])
    
    @staticmethod
    def load_from_json(d):
        thread = Thread()
        thread.title = d["title"]
        thread.authors = d["authors"]
        thread.characters = d["characters"]
        thread.url = d["url"]
        thread.blocks = [Block.load_from_json(block) for block in d["blocks"]]
        return thread


class Story:
    def __init__(self):
        self.title = ""
        self.authors = []
        self.characters = []
        self.threads = []

    def __str__(self):
        story = f"Story: {self.title}\nAuthors: {', '.join(self.authors)}\nCharacters: {', '.join(self.characters)}\n\n"
        for thread in self.threads:
            story += f"{thread.title}\n{thread.url}\nWord count: {thread.get_word_count()}\n\n"
        story += f"Total word count: {sum([thread.get_word_count() for thread in self.threads])}"
        return story
    
    def __repr__(self):
        threads = '\n'.join(repr(thread) for thread in self.threads)
        return f"|{self.title}|{','.join(self.authors)}|{','.join(self.characters)}|\n\n{threads}"

    def get_story(self) -> str:
        self.board_url = BOARD_URL
        self.page = requests.get(self.board_url)
        self.soup = BeautifulSoup(self.page.content, "html.parser")
        self.title = self.soup.find("title").text.split("|")[0].strip()
        self.tags = self.soup.find_all("td", {"class": ["post-subject vtop odd", "post-subject vtop even"]})
        self.threads_links = ["https://glowfic.com" + t.find("a")["href"] + "?view=flat" for t in self.tags][6:7]
        self.threads = [Thread().get_thread(thread_link) for thread_link in self.threads_links]
        self.characters = list(set([character for thread in self.threads for character in thread.characters]))
        self.authors = list(set([author for thread in self.threads for author in thread.authors]))
        return self
    
    def to_json(self):
        d = {}
        d["title"] = self.title
        d["authors"] = self.authors
        d["characters"] = self.characters
        d["board_url"] = self.board_url
        d["threads"] = [thread.to_json() for thread in self.threads]
        return d

    def get_all_blocks(self) -> list:
        all_blocks = []
        for thread in self.threads:
            all_blocks.extend(thread.blocks)
        return all_blocks
    
    def get_word_count(self) -> int:
        return sum([thread.get_word_count() for thread in self.threads])
    
    def create_txt(self, path: str):
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.__repr__())
        
    def save(self, path: str):
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_from_json(path: str):
        with open(path, "r") as f:
            d = json.load(f)
        story = Story()
        story.title = d["title"]
        story.authors = d["authors"]
        story.characters = d["characters"]
        story.board_url = d["board_url"]
        story.threads = [Thread.load_from_json(t) for t in d["threads"]]
        return story