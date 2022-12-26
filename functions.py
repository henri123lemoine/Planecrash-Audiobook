import requests
from bs4 import BeautifulSoup
from settings import X

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
3. Create a json file with the following format:
    {
        "title": "Board title",
        "authors": ["Author 1", "Author 2", "etc"],
        "characters": ["Character 1", "Character 2", "etc"],
        "word_count": 123456,
        "threads": [
            {
                "title": "Thread title",
                "authors": ["Author 1", "Author 2", "etc"],
                "characters": ["Character 1", "Character 2", "etc"],
                "episodes": [
                    {
                        "title": "Episode title",
                        "authors": ["Author 1", "Author 2", "etc"],
                        "characters": ["Character 1", "Character 2", "etc"],
                        "intro": "Intro text",
                        "outro": "Outro text",
                        "blocks": [
                            {
                                "character": "Character",
                                "screenname": "Screenname",
                                "author": "Author",
                                "icon": "Icon URL",
                                "content": [
                                    (e.g.)>"And then he said: 'Hi!'", in a voice that was **very** loud.
                                    "Narrator": "And then he said: ",
                                    "Character1": "Hi!",
                                    "Narrator": " in a voice that was ",
                                    "Narrator_bold": "very",
                                    "Narrator": " loud."
                                ]
                            },
                            {
                                "character": "Character",
                                "screenname": "Screenname",
                                "author": "Author",
                                "icon": "Icon URL",
                                "content": [
                                    "voice 1": "text voice 1",
                                    "voice 2": "text voice 2",
                                    etc.
                                ]
                            },
                            etc.
                        ]
                    },
                    {
                        "blocks": [
                            {
                                "character": "Character",
                                "screenname": "Screenname",
                                "author": "Author",
                                "icon": "Icon URL",
                                "content": [
                                    "voice 1": "text voice 1",
                                    "voice 2": "text voice 2",
                                    etc.
                                ]
                            },
                            etc.
                        ]
                    },
                    etc.
                ]
            },
            etc.
        ]
    }


class Block:
    def __init__(self, html_block):
        self.html_block = BeautifulSoup(str(html_block), "html.parser")
        
        self.character = character.text if (character:=self.html_block.find("div", {"class": "post-character"})) else None
        self.screenname = screenname.text if (screenname:=self.html_block.find("div", {"class": "post-screenname"})) else None
        self.author = self.html_block.find("div", {"class": "post-author"}).text
        self.icon_url = icon.find("img")["src"] if (icon:=self.html_block.find("div", {"class": "post-icon"})) else None
        self.content = content.text if (content:=self.html_block.find("div", {"class": "post-content"})) else None
    def __str__(self):
        return f"Character: {self.character}\nScreenname: {self.screenname}\nAuthor: {self.author}\nIcon: {self.icon_url}\nContent: {self.content}"
    def __repr__(self):
        return f"|{self.html_block}|"
    def get_image(self):
        return Image(self.icon_url) if self.icon_url else None
    def get_word_count(self):
        return len(self.content.split()) if self.content else 0


class Thread:
    def __init__(self, url: str):
        self.url = url
        page = requests.get(self.url)
        self.soup = BeautifulSoup(page.content, "html.parser")
        self.title = self.soup.find("span", {"id": "post-title"}).text
        self.authors = set([t.text.replace("\n", "") for t in self.soup.find_all("div", {"class": "post-author"})])
        self.characters = set([t.text for t in self.soup.find_all("div", {"class": "post-character"})])
        self.blocks = [Block(b) for b in self.soup.find_all("div", {"class": ["post-container post-post", "post-container post-reply"]})]
    def __str__(self):
        return f"Title: {self.title}\nAuthors: {self.authors}\nCharacters: {self.characters}\nBlocks count: {len(self.blocks)}\nURL: {self.url}"
    def __repr__(self):
        blocks = '\n'.join(repr(block) for block in self.blocks)
        return f"|{self.title}|{self.authors}|{self.characters}|\n{blocks}"
    def get_word_count(self) -> int:
        return sum([block.get_word_count() for block in self.blocks])
    def get_character_word_count(self) -> int:
        character_word_count = {}
        for character in self.characters:
            character_word_count[character] = 0
        for block in self.blocks:
            if block.content and block.character:
                character_word_count[block.character] += block.get_word_count()
        return character_word_count
    def get_episodes(self) -> list:
        """
        Splits the thread into episodes of roughly 10000 words.
        """
        episodes = []
        episode = Episode(self)
        for block in self.blocks:
            if episode.get_word_count() + block.get_word_count() > 10000:
                episodes.append(episode)
                episode = Episode(self)
            episode.add_block(block)
        episodes.append(episode)
        return episodes


class Story:
    def __init__(self):
        self.board_url = "https://glowfic.com/board_sections/703"
        self.page = requests.get(self.board_url)
        self.soup = BeautifulSoup(self.page.content, "html.parser")
        self.title = self.soup.find("title").text.split("|")[0].strip()
        self.tags = self.soup.find_all("td", {"class": ["post-subject vtop odd", "post-subject vtop even"]})
        self.threads_links = ["https://glowfic.com" + t.find("a")["href"] + "?view=flat" for t in self.tags]#[:1]
        self.threads = [Thread(thread_link) for thread_link in self.threads_links]
    def __str__(self):
        story = f"Story: {self.title}\nAuthors: {', '.join(self.get_all_authors())}\nCharacters: {', '.join(self.get_all_characters())}\n\n"
        for thread in self.threads:
            story += f"{thread.title}\n{thread.url}\nWord count: {thread.get_word_count()}\n\n"
        story += f"Total word count: {sum([thread.get_word_count() for thread in self.threads])}"
        return story
    def __repr__(self):
        threads = '\n'.join(repr(thread) for thread in self.threads)
        return f"|{self.title}|{','.join(self.get_all_authors())}|{','.join(self.get_all_characters())}|\n\n{threads}"
    def get_all_characters(self) -> set:
        all_characters = set()
        for thread in self.threads:
            all_characters = all_characters.union(thread.characters)
        return all_characters
    def get_all_authors(self) -> set:
        all_authors = set()
        for thread in self.threads:
            all_authors = all_authors.union(thread.authors)
        return all_authors
    def get_characters_screennames(self) -> dict:
        all_characters_screennames = {}
        for character in self.characters:
            all_characters_screennames[character] = []
        for thread in self.threads:
            for block in thread.blocks:
                if block.character and block.screenname:
                    if block.screenname not in all_characters_screennames[block.character]:
                        all_characters_screennames[block.character].append(block.screenname)
        return all_characters_screennames
    def get_all_blocks(self) -> list:
        all_blocks = []
        for thread in self.threads:
            all_blocks.extend(thread.blocks)
        return all_blocks
    def get_characters_blocks(self) -> dict:
        all_characters_blocks = {}
        for character in self.characters:
            all_characters_blocks[character] = []
        for block in self.get_all_blocks():
            if block.character:
                all_characters_blocks[block.character].append(block)
        return all_characters_blocks
    def get_word_count(self) -> int:
        return sum([thread.word_count for thread in self.threads])
    def get_character_word_count(self) -> dict:
        character_word_count = {}
        for character in self.characters:
            character_word_count[character] = 0
        for thread in self.threads:
            for character in thread.characters:
                character_word_count[character] += thread.character_word_count[character]
        return character_word_count
    def create_txt(self, path: str):
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.__repr__())
    def find_text(self, text: str) -> list:
        found = []
        for thread in self.threads:
            for block in thread.blocks:
                if text in block.content:
                    found.append(block)
        return found