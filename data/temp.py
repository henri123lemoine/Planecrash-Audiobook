

"""
Update a content block, such as the following, in order to make it easier to process and separate sections of text into separate voices.

<div class="post-content"><p>And then types and retypes, more briefly, because wow is this taking some time:</p>
<p>&nbsp;</p>
<p><span style="text-decoration: underline;">My beliefs about the probable loci of my disagreements with Carissa Sevar, more located and pointed at than argued:</span></p>
<p>- Do not in fact respect reasoning of local mortals about their afterlife prospects, suspect they're mostly not thinking about it, <a href="https://wikipedia.org/non-existence">nonexistence</a> isn't exactly an easy option for them anyways, don't think their expressed opinions are really&nbsp;<em>bound to</em> the relative weight of an eternity in Axis or Hell.&nbsp; <strong>No</strong> people who can remember millennia of existence as paving stone / lemure and also millennia in Axis, and do an interpersonal comparison there - if even <em>that</em> would be meaningful and not just default to whichever came last.&nbsp; <em>Given all that,</em>&nbsp;situation with 9x Axis inhabitants saying 'this life was a good deal' and 1x Hell <big>inhabitants</big> saying 'bad deal' doesn't seem so much like a 90% majority<a href="oauwieidhuwed"> vote</a>, as people dividing a cake where 9 get nice deals and 1 gets crumbs; the person who got the crumbs has a kind of priority in saying whether the overall deal was fair or not.</p>
<abbr title="saying goodbye"></abbr>
<p>- Have estimate of Pharasma's apparent power given observations about Her, does not seem to rule out rigging Her Creation to destruct.</p>
<img alt="Project Lawful Year 1:  Jun 28 2021 - Jun 28 2022" height="1199" src="https://i.imgur.com/5HeP9cG.jpg" width="1884"/><br/>
<hr/><br/>
<p>- Tropian probability distortions: <em>clearly </em>a thing, even allowing for some of our history to have been produced by divine interventions imitating tropes.&nbsp; If we don't do this now, Pharasma's Creation might be waiting a long long time on the next story-empowered people who would have a probabilistically anomalous chance at fixing or even <em>changing</em> things.</p><br/></div>

<div class="post-content"></div>:remove that part

<a href="https://link.com" rel="noopener">this is a link to link.com</a>:remove

<img alt="Project Lawful Year 1:  Jun 28 2021 - Jun 28 2022" height="1199" src="https://i.imgur.com/5HeP9cG.jpg" width="1884"/>: replace with "[IMAGE]" and make MANUAL_ACTION_REQUIRED True.

<span style="font-size: 11pt; font-family: Arial; color: #000000;"></span>: make MANUAL_ACTION_REQUIRED True.

<br/>: replace with <shh></shh> tag

<em></em>: nothing

<strong></strong>: nothing

<blockquote></blockquote>: make MANUAL_ACTION_REQUIRED True

<abbr title="saying goodbye"></abbr>: make MANUAL_ACTION_REQUIRED True

<table style="width: auto;">
<tbody>
<tr>
<td style="border: 0;">text</td>
</tr>
</tbody>
</table>
make MANUAL_ACTION_REQUIRED True

<big>msg</big>: make MANUAL_ACTION_REQUIRED True

<small>msg</small>: make MANUAL_ACTION_REQUIRED True

<hr/>: replace with <shh></shh> tag and make MANUAL_ACTION_REQUIRED True

<p>paragraph</p>: nothing
<p dir="ltr" style="line-height: 1.38; margin-top: 0pt; margin-bottom: 0pt;"><p>: replace with <p></p> and make MANUAL_ACTION_REQUIRED True

<details>
<summary>warning/description of spoiler text</summary>
<p>spoiler text</p>
</details>
make MANUAL_ACTION_REQUIRED True

"text": replace with <quote>text</quote>

(text): replace with <par>text</par>
"""

import re

# The regex pattern to match quotes that aren't between < and >
pattern = r'(?<!<)"(?![^<]*>)' + '|' + r'<[^<>]+>' + '|' + r'[()\n]' 

# The input string
content = """<div class="post-content"><p>And then types and retypes, more briefly, because wow is this taking some time:</p>
<p>&nbsp;</p>
<p><span style="text-decoration: underline;">My beliefs about the probable loci of my disagreements with Carissa Sevar, more located and pointed at than argued:</span></p>
<p>- Do not in fact respect reasoning of local mortals about their afterlife prospects, suspect they're mostly not thinking about it, <a href="https://wikipedia.org/non-existence">nonexistence</a> isn't exactly an easy option for them anyways, don't think their expressed opinions are really&nbsp;<em>bound to</em> the relative weight of an eternity in Axis or Hell.&nbsp; <strong>No</strong> people who can remember millennia of existence as paving stone / lemure and also millennia in Axis, and do an interpersonal comparison there - if even <em>that</em> would be meaningful and not just default to whichever came last.&nbsp; <em>Given all that,</em>&nbsp;situation with 9x Axis inhabitants saying 'this life was a good deal' and 1x Hell <big>inhabitants</big> saying 'bad deal' doesn't seem so much like a 90% majority<a href="oauwieidhuwed"> vote</a>, as people dividing a cake where 9 get nice deals and 1 gets crumbs; the person who got the crumbs has a kind of priority in saying whether the overall deal was fair or not.</p>
<abbr title="saying goodbye"></abbr>
<p>- Have estimate of Pharasma's apparent power given observations about Her, does not seem to rule out rigging Her Creation to destruct.</p>
<img alt="Project Lawful Year 1:  Jun 28 2021 - Jun 28 2022" height="1199" src="https://i.imgur.com/5HeP9cG.jpg" width="1884"/><br/>
<hr/><br/>
<p>- Tropian probability distortions: <em>clearly </em>a thing, even allowing for some of our history to have been produced by divine interventions imitating tropes.&nbsp; If we don't do this now, Pharasma's Creation might be waiting a long long time on the next story-empowered people who would have a probabilistically anomalous chance at fixing or even <em>changing</em> things.</p><br/></div>"""

MANUAL_ACTION_REQUIRED = False

if '<img' in content or '<span' in content or '<blockquote' in content or '<abbr' in content or '<table' in content or '<big' in content or '<small' in content or '<hr' in content or '<p ' in content or '<details' in content:
    MANUAL_ACTION_REQUIRED = True

# <dir>
content = content[26:-6]

# <a> (whatever tag between <a and >)
content = re.sub(r'<a[^>]*>', '', content)

# <img>; MANUAL_ACTION_REQUIRED must be set to True
content = re.sub(r'<img[^>]*>', '[IMAGE]', content)

# <br/>
content = re.sub(r'<br/>', '<shh></shh>', content)

# <em>
# <strong>
# <blockquote>
# <abbr>
# <table>
# <big>
# <small>
# <hr>
# <p dir="ltr" style="line-height: 1.38; margin-top: 0pt; margin-bottom: 0pt;"><p>
# <details>

# "" (whatever " symbol not between < and >)




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