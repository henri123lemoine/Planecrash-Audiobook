from bs4 import BeautifulSoup
import re
from typing import Tuple, List
from settings import VOICE_DICT

class Voice:
    def __init__(self, character: str, content: str):
        self.character = character
        self.voice_name = VOICE_DICT.get(character)
        print(f"Voice content 1: {content}")
        self.content = content[26:-6]
        self.len_content = len(self.content)
        print(f"Voice content 2: {self.content}")
        # Replace opening quotes by <quote> and closing quotes by </quote>
        opening_quote = True
        opening_parenthesis = True
        i = 0
        while i < self.len_content:
            if self.content[i] == '"':
                if opening_quote:
                    self.content = self.content[:i] + '<quote>' + self.content[i+1:]
                    opening_quote = False
                    i += 6
                else:
                    self.content = self.content[:i] + '</quote>' + self.content[i+1:]
                    opening_quote = True
                    i += 7
            elif self.content[i] == '(':
                if opening_parenthesis:
                    self.content = self.content[:i] + '<parenthesis>' + self.content[i+1:]
                    opening_parenthesis = False
                    i += 12
                else:
                    self.content = self.content[:i] + '</parenthesis>' + self.content[i+1:]
                    opening_parenthesis = True
                    i += 13
            i += 1
        self.len_content = len(self.content)

        
        print(f"Voice content 3: {self.content}")
        self.html_block = BeautifulSoup(self.content, "html.parser")
        self.voices = []

        self.tags, self.text_portions = self.extract_tags_and_text()

    def extract_tags_and_text(self) -> Tuple[List[str], List[str]]:
        tags = []
        text_portions = []
        
        # Find all tags in the input string
        tag_indices = []
        for tag in re.finditer(r'<[^<>]+>', self.content):
            tag_indices.append((tag.start(), tag.end()))
            tags.append(tag.group()[1:-1])
        
        # Extract the text portions between the tags
        start = 0
        for start_index, end_index in tag_indices:
            text_portions.append(self.content[start:start_index])
            start = end_index
        text_portions.append(self.content[start:])
        
        text_portions = [text.strip() for text in text_portions][1:]

        curr_tags_stack = []
        for tag in tags:
            pass #todo

            

        return tags, text_portions

        


print("\n"*10)
character = "Keltham"
content = """<div class="post-content"><p>"I am the most proven Asmodean in Project Lawful.  I am the sanest person in Project Lawful.  <em>I am the scariest person in Project Lawful.  And right now, I AM THE MOST ANNOYED PERSON IN PROJECT LAWFUL.  <strong>THIS DOMINANCE</strong> CONTEST IS OVER.  <strong>I WIN.</strong>  NOW BEHAVE LIKE FUCKING SANE PEOPLE UNTIL SEVAR GETS BACK OR I WILL FUCKING MAKE YOU BEHAVE.</em>"</p></div>"""
content = """<div class="post-content"><p>"Asmodeus has the stronger claim on our souls," says Security firmly. \xa0And then shuts up, it\'s harder to get in trouble for saying too little.</p></div>"""
voice = Voice(character, content)
print("\n"*10)
for tag, text in zip(voice.tags, voice.text_portions):
    print(f"<{tag}>\n{text}")

# print(len(voice.tags))
# print(len(voice.text_portions))

# import re

# def extract_tags_and_text(content: str) -> tuple[list[str], list[str]]:
#     tags = []
#     text_portions = []
#     stack = []
    
#     # Find all tags in the input string
#     tag_indices = []
#     for tag in re.finditer(r'<[^<>]+>', content):
#         tag_indices.append((tag.start(), tag.end()))
#         tags.append(tag.group()[1:-1])
    
#     # Extract the text portions between the tags
#     start = 0
#     for start_index, end_index in tag_indices:
#         text_portions.append(content[start:start_index])
#         start = end_index
#     text_portions.append(content[start:])
    
#     return tags, text_portions

# content = "blabla1<tag1>blabla2<tag2>blabla3</tag2>blabla4</tag1>blabla5"
# tags, text_portions = extract_tags_and_text(content)
# print(tags)
# print(text_portions)
