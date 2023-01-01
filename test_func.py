from bs4 import BeautifulSoup
import re
from typing import Tuple, List
from settings import VOICE_DICT
from helper_functions import process_voice_content

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

character = "Keltham"
content = """<div class="post-content"><p>And then types and retypes, more briefly, because wow is this taking some time:</p>
<p>&nbsp;</p>
<p><span style="text-decoration: underline;">My beliefs about the probable loci of my disagreements with Carissa Sevar, more located and pointed at than argued:</span></p>
<p>- A possibly theoretically unresolvable epistemic disagreement (though we'll know better at INT 29) where I've updated off my isekai experience about what 'typically happens', and ended up in a world full of people to whom this observation is theoretically inaccessible.</p>
<p>- Very different model of the theoretical origins and hence likely psychology of beings and Powers who could devise continuation causal-weaves for otherwise halted entities; in particular, greater expectation of coordination among them, and expecting most utility functions of non-mortal-caring such entities to settle on maxima which don't have mortals inside them at all.</p>
<p>- Unresolvable values difference about disutility of nonexistence:&nbsp; eternal suffering &lt;&lt; null &lt; eternal happiness.&nbsp; Would consider Hell at least 100 times as bad as Axis is good.</p>
<p>- Do not in fact respect reasoning of local mortals about their afterlife prospects, suspect they're mostly not thinking about it, nonexistence isn't exactly an easy option for them anyways, don't think their expressed opinions are really&nbsp;<em>bound to</em> the relative weight of an eternity in Axis or Hell.&nbsp; No people who can remember millennia of existence as paving stone / lemure and also millennia in Axis, and do an interpersonal comparison there - if even <em>that</em> would be meaningful and not just default to whichever came last.&nbsp; <em>Given all that,</em>&nbsp;situation with 9x Axis inhabitants saying 'this life was a good deal' and 1x Hell inhabitants saying 'bad deal' doesn't seem so much like a 90% majority vote, as people dividing a cake where 9 get nice deals and 1 gets crumbs; the person who got the crumbs has a kind of priority in saying whether the overall deal was fair or not.</p>
<p>- Pharasma thought the things She trapped in Her creation couldn't endanger Her and so She did not need to treat with them as agents and divide gains fairly with them, or even ask what they wanted.&nbsp; I see myself as agent, this world as a deal, and reject the deal.</p>
<p>- Expect Golarion typical, Pharasma roughly balanced entire multiverse to sort around 1/3 of petitioners to each category on each axis.&nbsp; No obvious reason why Pharasma would have built a setup where later on almost nobody got sorted to Hell in Her own expectation.</p>
<p>- Suspect Iomedae's "goddess of victory over Evil" deal, maybe not so much distorts Her probabilities, as constrains the way She can behave about them.&nbsp; Iomedae has notably not distributed a timetable with probabilities to Her followers.&nbsp; Iomedae is opposed by gods much more powerful than Her and maybe smarter who do not want Her to win.&nbsp; If everybody got hope by trying hard, every god would own that hope to the same degree, none more hopeful than the others.</p>
<p>- Have estimate of Pharasma's apparent power given observations about Her, does not seem to rule out rigging Her Creation to destruct.</p>
<p>- I'm sorta broken, yeah.&nbsp; Everyone else in Golarion is completely bugshit wacko, though.</p>
<p>- Tropian probability distortions: <em>clearly </em>a thing, even allowing for some of our history to have been produced by divine interventions imitating tropes.&nbsp; If we don't do this now, Pharasma's Creation might be waiting a long long time on the next story-empowered people who would have a probabilistically anomalous chance at fixing or even <em>changing</em> things.</p></div>"""

print("\n"*10)
process_voice_content(content)

# voice = Voice().extract(character, content)

# print(voice.content)

# for v in voice.voices:
#     print(v)






content = """<div class="post-content"><p></p>
<p></p>
<p><span style="text-decoration: underline;"></span></p>
<p></p>
<p></p>
<p></p>
<p><em></em><em></em><em></em></p>
<p></p>
<p></p>
<p>""</p>
<p></p>
<p></p>
<p><em></em><em></em></p></div>"""
