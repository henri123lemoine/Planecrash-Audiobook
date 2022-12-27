import unicodedata
html_block = """<div class="post-content"><p> </p>
<p> </p>
<p>I would be, if I had any idea what they were. </p>
<p> </p>
<p> </p>
<p> She said, "What - do you imagine Asmodeus sees, when he sees a slave who is in love with someone? What, from the angle of a god, does <strong>that</strong> even look like?"</p></div>"""

"""
->
[("Silence 0.2", None, ""), ("Silence 0.2", None, ""), ("Narrator", None, "I would be, if I had any idea what they were."), ("Silence 0.2", None, ""), ("Silence 0.2", None, ""), ("Narrator", None, "She said, "), ("Keltham", None, "What - do you imagine Asmodeus sees, when he sees a slave who is in love with someone? What, from the angle of a god, does"), ("Narrator", "bold", "that"), ("Narrator", None, "even look like?")]
"""

html_block2 = """<div class="post-content"><p>"And Project Lawful is supposed to fix that.  Not in Hell, here in Golarion."</p>
<p><br/>"I don't want to be broken anymore.  Are you ready - to unbreak me, to do the things to me that the Most High thought only I could survive."</p></div>"""

def split_voices(html_block):
    """
    Splits the block's html content into voices.
    Splits can occur when:
    - A quote is used -> the voice is the character who said the quote
    - A linebreak is used (<br> tag or <p> </p> tags) -> the voice is "Silence 0.2"
    - Elsewhere -> the voice is the Narrator

    Whenever there is a **bold** effect (illustrated by <strong> tags) or a *italic* effect (illustrated by <em> tags), the voice the voice + effect.

    E.g. from the html above:
    '<div class="post-content">' is ignored (not a voice)
    '<p> </p>' is a silence -> (Silence 0.2, None, '')
    '<p> </p>' is a silence -> (Silence 0.2, None, '')
    '<p>I would be, if I had any idea what they were. </p>' is the narrator -> (Narrator, None, 'I would be, if I had any idea what they were.')
    '<p> </p>' is a silence -> (Silence 0.2, None, '')
    '<p> </p>' is a silence -> (Silence 0.2, None, '')
    '<p> She said,' is the narrator -> (Narrator, None, 'She said,')
    '"What - do you imagine Asmodeus sees, when he sees a slave who is in love with someone? What, from the angle of a god, does ' is the narrator -> (Narrator, None, 'What - do you imagine Asmodeus sees, when he sees a slave who is in love with someone? What, from the angle of a god, does')
    '<strong>that</strong>' is the narrator + bold -> (Narrator, 'bold', 'that')
    'even look like?"</p></div>' is the narrator -> (Narrator, None, 'even look like?')

    Returns a list of voice tuples (voice, effects, text)

    Algorithm:
    1. Preprocess the html block (remove the <div class="post-content"> tag and the </div> tag) (use unicodedata.normalize('NFC', str(html_block)))


    """
    voices = []
    narrator = "Narrator"
    character = "Keltham"
    silence = "Silence 0.2"

    effects = []

    stack = []
    for char in html_block:
        if char == '<':
            stack.append(char)
        elif char == '>':
            stack.pop()
        elif not stack:
            voices.append(char)

    # Preprocess the html block
    html_block = unicodedata.normalize('NFC', str(html_block))
    html_block = html_block.replace('<div class="post-content">', '').replace('</div>', '').replace('<br>', '').replace('<p>\xa0</p>', '').replace('<p> </p>', '').replace('<p>', '').replace('</p>', '').replace('</strong>', '<strong>').replace('</em>', '<em>')
    
    if '"' in html_block:
        nar1, char1, nar2 = html_block.split('"')
        return split_voices(nar1) + split_voices(char1) + split_voices(nar2)
    if '\n' in html_block:
        html_block = html_block.split('\n')
        return split_voices(html_block[0]) + [(silence, None, '')] + split_voices(html_block[1])
    if '<strong>' in html_block:
        nar1, bold, nar2 = html_block.split('<strong>')
        return split_voices(nar1) + [(narrator, 'bold', bold)] + split_voices(nar2)
    if '<em>' in html_block:
        nar1, italic, nar2 = html_block.split('<em>')
        return split_voices(nar1) + [(narrator, 'italic', italic)] + split_voices(nar2)
    return [(narrator, None, html_block)]
#UGH SOLVE THIS MESS


#     def split_voices_line(line):
#         """
#         Splits the line into voices.
        
#         First split between characters, then effects:
#         1. A quote is used: we must find 2 " characters. E.g. 'This is a quote: "Hi"'. line_tmp = line.split('"'); voice1 = (Narrator, None, line_tmp[0]); voice2 = (Character, None, line_tmp[1]); voice3 = (Narrator, None, line_tmp[2]). If line_tmp 1 or 3 is empty, we don't add the voice.
#         2. A linebreak is used: we must find <br> or <p>\xa0</p> tags.
        
#         Miscellanous notes:
#             - Multi-line quotes makes this much harder; split_voices for a single line won't work.
#             - We'll need to first find the quotes. Then, we'll need to find the linebreaks. Then, we'll need to find the effects.
#         """
#         line = line.replace('<br>', '').replace('<p>\xa0</p>', '<br>').replace('<div class="post-content">', '').replace('</div>', '')
        

#     # Preprocess the html block
#     html_block = html_block.replace('<div class="post-content">', '').replace('</div>', '').replace('<p>\xa0</p>', '<br>')

#     # Go line by line, and split the block into voices
#     voices = []
#     voice = None
#     effects = None
#     text = ''

#     for line in html_block.splitlines():
#         if line.startswith('<div class="post-content">'):
#             continue
#         elif line.startswith('<p>'):
#             if line == '<p> </p>':
#                 voices.append(('Silence 0.2', None, ''))
#             else:
#                 if voice is not None:
#                     voices.append((voice, effects, text))
#                 voice = 'Narrator'
#                 effects = None
#                 text = line[3:-4]
#         elif line.startswith('<strong>'):
#             if voice is not None:
#                 voices.append((voice, effects, text))
#             voice = 'Narrator'
#             effects = 'bold'
#             text = line[8:-9]
#         elif line.startswith('<em>'):
#             if voice is not None:
#                 voices.append((voice, effects, text))
#             voice = 'Narrator'
#             effects = 'italic'
#             text = line[4:-5]
#         elif line.startswith('<br>'):
#             if voice is not None:
#                 voices.append((voice, effects, text))
#             voice = 'Silence 0.2'
#             effects = None
#             text = ''
#         else:
#             text += line
#     if voice is not None:
#         voices.append((voice, effects, text))
#     return voices
    
voices = split_voices(html_block)
for voice in voices:
    print(voice)























































import requests
from bs4 import BeautifulSoup
import json
import unicodedata
import pickle
class Block:
    def __init__(self, html_block):
        self.html_block = BeautifulSoup(str(html_block), "html.parser")
        self.url = self.html_block.find("a", {"rel": "alternate"})["href"]
        self.character = character.text if (character:=self.html_block.find("div", {"class": "post-character"})) else None
        self.screenname = screenname.text if (screenname:=self.html_block.find("div", {"class": "post-screenname"})) else None
        self.author = self.html_block.find("div", {"class": "post-author"}).text
        self.icon_url = icon.find("img")["src"] if (icon:=self.html_block.find("div", {"class": "post-icon"})) else None
        self.content = content if (content:=self.html_block.find("div", {"class": "post-content"})) else None
        self.content_text = content.text if (content:=self.html_block.find("div", {"class": "post-content"})) else None

    def create_json_dict(self):
        d = {}
        d["character"] = self.character
        d["screenname"] = self.screenname
        d["author"] = self.author
        d["url"] = self.url
        d["icon_url"] = self.icon_url
        d["content"] = self.content
        d["content_text"] = self.content_text
        return d

class Thread:
    def __init__(self, url: str):
        self.url = url
        page = requests.get(self.url)
        self.soup = BeautifulSoup(page.content, "html.parser")
        self.title = self.soup.find("span", {"id": "post-title"}).text
        self.authors = set([t.text.replace("\n", "") for t in self.soup.find_all("div", {"class": "post-author"})])
        self.characters = set([t.text for t in self.soup.find_all("div", {"class": "post-character"})])
        self.blocks = [Block(b) for b in self.soup.find_all("div", {"class": ["post-container post-post", "post-container post-reply"]})]
    
    def create_json_dict(self):
        d = {}
        d["title"] = self.title
        d["authors"] = self.authors
        d["characters"] = self.characters
        d["url"] = self.url
        d["blocks"] = [block.create_json_dict() for block in self.blocks]
        return d

class Story:
    def __init__(self):
        self.board_url = "https://glowfic.com/board_sections/703"
        self.page = requests.get(self.board_url)
        self.soup = BeautifulSoup(self.page.content, "html.parser")
        self.title = self.soup.find("title").text.split("|")[0].strip()
        self.characters = set([character for thread in self.threads for character in thread.characters])
        self.authors = set([author for thread in self.threads for author in thread.authors])
        self.tags = self.soup.find_all("td", {"class": ["post-subject vtop odd", "post-subject vtop even"]})
        self.threads_links = ["https://glowfic.com" + t.find("a")["href"] + "?view=flat" for t in self.tags][6:7]
        self.threads = [Thread(thread_link) for thread_link in self.threads_links]
        
    def create_json_dict(self):
        d = {}
        d["title"] = self.title
        d["authors"] = self.get_all_authors()
        d["characters"] = self.get_all_characters()
        d["url"] = self.board_url
        d["threads"] = [thread.create_json_dict() for thread in self.threads]
        return d