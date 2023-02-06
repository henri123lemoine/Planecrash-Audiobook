import re
from typing import List, Tuple
#from settings import VOICE_DICT




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

