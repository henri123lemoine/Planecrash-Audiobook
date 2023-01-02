from bs4 import BeautifulSoup
from get_voice import Voice




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
        block = ""
        block += f"Character: {self.character}\n" if self.character else ""
        block += f"Screenname: {self.screenname}\n" if self.screenname else ""
        block += f"Author: {self.author}\n"
        block += f"Icon url: {self.icon_url}\n" if self.icon_url else ""
        block += f"Permalink: {self.url}\n"
        content = self.content if len(self.content)<200 else str(self.content[:200]) + " [...]"
        block += f"Content:\n{content}\n"
        block += f"Voices:\n[\n\t{voices}\n]"
        return block

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

    async def async_extract(self, html: BeautifulSoup) -> "Block":
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
    


if __name__ == "__main__":
    # Test the class
    # 1. Extract a block
    # 2. Transform it to json and back    

    import requests
    JSON_PATH = "data/threads JSON"
    
    thread_url = 'https://glowfic.com/posts/6322?view=flat'

    # Extract a block
    block_html = BeautifulSoup(requests.get(thread_url).content, "html.parser").find("div", {"class": ["post-container post-post", "post-container post-reply"]})

    block = Block().extract(block_html)
    print(f"Block:\n{block}")
    print("Extracted block successfully\n")

    # Transform it to json and back
    block_json = block.to_json()
    print(f"Block JSON:\n{block_json}")
    print("Transformed block to json successfully\n")

    block = Block.load_from_json(block_json)
    print(f"Block:\n{block}")
    print("Transformed json to block successfully\n")


