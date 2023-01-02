
import re

# The regex pattern to match quotes that aren't between < and >
pattern = r'(?<!<)"(?![^<]*>)' + '|' + r'<[^<>]+>' + '|' + r'[()\n]' 

# The input string
content = '<p>This string has a quote: "Hi, here are some some <a href="link">link</a> tags." LOL<hr/></p>'

content = content.replace("<hr/>", "<hr></hr>")

print(content)

tags = []
tag_indices = []
mult_2_quote = True
i = 0
for tag_pattern in re.finditer(pattern, content):
    tag = tag_pattern.group()

    start = tag_pattern.start() + i
    end = tag_pattern.end() + i

    if tag == '"':
        tag = f'<{"/"*(mult_2_quote:=1-mult_2_quote)}quote>'
        content = f"{content[:start]}{tag}{content[end:]}"
        end = start + len(tag)
    elif tag == '(':
        tag = '<par>'
        content = f"{content[:start]}{tag}{content[end:]}"
        end = start + len(tag)
    elif tag == ')':
        tag = '</par>'
        content = f"{content[:start]}{tag}{content[end:]}"
        end = start + len(tag)
    elif tag == '<br/>':
        tag = '<shh></shh>'
        content = f"{content[:start]}{tag}{content[end:]}"
        end = start + len(tag)
    elif tag == '\n':
        tag = '<shh></shh>'
        content = f"{content[:start]}{tag}{content[end:]}"
        end = start + len(tag)
    elif tag[:3] == '<a ':
        tag = '<a>'
        content = f"{content[:start]}{tag}{content[end:]}"
        end = start + len(tag)
    
    i += len(tag) - len(tag_pattern.group())
    
    print(f"{tag} ({start}, {end})")
    
    tags.append(tag)
    tag_indices.append((start, end))

    i += len(tag) - len(tag_pattern.group())

print(tags)