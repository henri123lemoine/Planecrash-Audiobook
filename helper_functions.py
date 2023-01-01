import re

#  This file contains helper functions to make the code more readable and easier to maintain.

def process_voice_content(content):
    # Remove div tags
    content = content[26:-6]

    tags = []
    tag_indices = []
    for tag in re.finditer(r'<[^<>]+>', content):
        tag_indices.append((tag.start(), tag.end()))
        tags.append(tag.group()[1:-1])
    
    tmp = []
    for tag in tags:
        tmp.append(tag.split()[0])
    tags = tmp

    print(tags)

    text_portions = []
    start = 0
    for start_index, end_index in tag_indices:
        text_portions.append(content[start:start_index])
        start = end_index
    text_portions.append(content[start:])
    text_portions = [text.strip() for text in text_portions][1:]
    
    voices = []
    tags_stack = []
    for i in range(len(tags)):
        tag = tags[i]
        if tag[0] == '/':
            tags_stack.pop()
        else:
            tags_stack.append(tag.split()[0])
        voices.append([text_portions[i], tags_stack.copy()])

    voices = [voice for voice in voices if voice != ['', []]]
    return voices



#     # Replace newlines and <br/> tags with <silence></silence>
#     content = content.replace('\n', '<br/>').replace('<br/>', '<silence></silence>')
#     # Replace double quotes with <quote></quote>
#     content = content.replace('"', '<quote></quote>')
#     # Replace parentheses with <parenthesis></parenthesis>
#     content = content.replace('(', '<parenthesis>').replace(')', '</parenthesis>')
#     # Replace hr tags with <hr></hr>
#     content = content.replace('<hr/>', '<hr></hr>')
    
#     a = 1
#     i = 0
#     while (i:=i+1) < len(content):
#         if content[i] == '"': content = f"{content[:i]}<{'/'*(a:=1-a)}quote>{content[i+1:]}"
    return content


def make_title(title):
    return title.replace(":", "-").replace("/", "_").replace("\\", "_").replace("<", "(").replace(">", ")").replace("*", "").replace("?", "").replace("|", "#")