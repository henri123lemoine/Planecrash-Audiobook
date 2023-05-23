from bs4 import BeautifulSoup
import requests


class Block:
    def __init__(self, html=None):
        self.character = ""
        self.screenname = ""
        self.author = ""
        self.icon_url = ""
        self.url = ""
        self.content = ""
        
        if html:
            self.extract(html)

    def __str__(self) -> str:
        voices = "\n\t".join([f"{voice['name']}: {voice['content']}" for voice in self.voices])
        content = self.content if len(self.content) < 200 else self.content[:200] + " [...]"
        block = f"Character: {self.character}\nScreenname: {self.screenname}\nAuthor: {self.author}\nIcon url: {self.icon_url}\nPermalink: {self.url}\nContent:\n{content}\nVoices:\n[\n\t{voices}\n]"
        return block

    def extract(self, html: BeautifulSoup):
        def find_text(class_name: str):
            return html.find("div", {"class": class_name}).text if (element := html.find("div", {"class": class_name})) else None

        self.character = find_text("post-character")
        self.screenname = find_text("post-screenname")
        self.author = find_text("post-author").replace("\n", "")
        self.icon_url = html.find("div", {"class": "post-icon"}).find("img")["src"] if (icon := html.find("div", {"class": "post-icon"})) else None
        self.url = 'https://www.glowfic.com' + html.find("a", {"rel": "alternate"})["href"]
        self.content = str(html.find("div", {"class": "post-content"})) if (content := html.find("div", {"class": "post-content"})) else ""

    def to_json(self) -> dict:
        return {
            "character": self.character,
            "screenname": self.screenname,
            "author": self.author,
            "icon_url": self.icon_url,
            "url": self.url,
            "content": self.content,
        }

    @classmethod
    def from_json(cls, d: dict):
        block = cls()
        block.character = d["character"]
        block.screenname = d["screenname"]
        block.author = d["author"]
        block.icon_url = d["icon_url"]
        block.url = d["url"]
        block.content = d["content"]
        return block


if __name__ == "__main__":
    thread_url = 'https://glowfic.com/posts/6322?view=flat'
    block_html = BeautifulSoup(requests.get(thread_url).content, "html.parser").find("div", {"class": ["post-container post-post", "post-container post-reply"]})
    # Test the class
    # 1. Extract a block
    # 2. Transform it to json and back

    # Extract a block
    block = Block(block_html)
    print(f"Block:\n{block}")
    print("Extracted block successfully\n")

    # Transform it to json and back
    block_json = block.to_json()
    print(f"Block JSON:\n{block_json}")
    print("Transformed block to json successfully\n")

    block_from_json = Block.from_json(block_json)
    print(f"Block:\n{block_from_json}")
    print("Transformed json to block successfully\n")