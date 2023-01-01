# This file contains helper functions to make the code more readable and easier to maintain.

def process_voice_content(content):
    # Remove div tags
    content = content[26:-6]

    

    # Replace newlines and <br/> tags with <silence></silence>
    content = content.replace('\n', '<br/>').replace('<br/>', '<silence></silence>')
    # Replace double quotes with <quote></quote>
    content = content.replace('"', '<quote></quote>')
    # Replace parentheses with <parenthesis></parenthesis>
    content = content.replace('(', '<parenthesis>').replace(')', '</parenthesis>')
    # Replace hr tags with <hr></hr>
    content = content.replace('<hr/>', '<hr></hr>')
    
    a = 1
    i = 0
    while (i:=i+1) < len(content):
        if content[i] == '"': content = f"{content[:i]}<{'/'*(a:=1-a)}quote>{content[i+1:]}"
    return content

