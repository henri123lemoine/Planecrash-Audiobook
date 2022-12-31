# Planecrash_Audio

The story information is stored in the Story class.
It contains a title string, an authors list, a characters list, a board url string, and threads (found at the board url).

The threads information is stored in the Thread class.
It contains a title string, an authors list, a characters list, a thread url string, and blocks (found at the thread url).

The blocks information is stored in the Block class.
It contains a character string, an screenname string, an author string, an icon url string, a block url string, a content string (containing html describing the block), and a content text string (containing only the story-text part of the html).

#TODO
- Blocks should contain a list 'voices' of voice-text tuples, describing what voice should say what and in what order. (in progress)

- Write code to make easier the process of generating an audio episode from the story. This may include:
    1. automatically separating threads in 30-minutes-length list of blocks.
    2. function to generate audiobook from list of blocks (including intro and outro).
    In the first place, get access to play.ht audio and play around with it, and associate voices with characters in VOICE_DICT.

- Determine which characters have what voice, and what consistent accents to give each region from Golarion.

## Process tags
    <div class="post-content"></div>"
    remove

    <a href=""></a>
    One possibility is to just remove them; another is to make the narrator say "link attached" or something of the sort. TBD
    
    <img alt="Project Lawful Year 1:  Jun 28 2021 - Jun 28 2022" height="1199" src="https://i.imgur.com/5HeP9cG.jpg" width="1884"/>
    One option is to manually describe the image and make the narrator describe it. See todo_helper.txt for all examples.
    
    <span style="font-size: 11pt; font-family: Arial; color: #000000; background-color: transparent; font-weight: 400; font-style: normal; font-variant: normal; text-decoration: none; vertical-align: baseline;white-space: pre-wrap;"></span>
    manually go through spans and see what to change; for some of them, a voice changer should suffice; for some, nothing needs to be changed.
    Ex: [https://www.glowfic.com/replies/1898979#reply-1898979]
    
    <br/>
    Add a short silence, just like in the case of <p>\xa0</p>.
    
    <em></em>
    speak slighly slower
    
    <strong></strong>
    speak slighly louder
    
    <blockquote></blockquote>
    sadly, this will have to be done manually. Sometimes it is a quote from a previous block, sometimes it is a god speaking, etc. 
    Ex: [https://www.glowfic.com/replies/1836894#reply-1836894]
    
    <abbr title="saying goodbye"></abbr>
    All of them are in conversation with Abadar; go through this conversation manually.
    
    <table style="width: auto;">
	    <tbody>
	      <tr>
	        <td style="border: 0;">text</td>
          </tr>
        </tbody>
      </table>
    Reformulate it manually.
    All examples from: [https://www.glowfic.com/posts/4582?page=26]
    
    <big>msg</big>
    See todo_helper.txt for all <big> tags. This only includes Otolmens, Dispater and Curse of Laughter talking, plus a single Pilar sound effect.

    <small>msg</small>
    Whispering maybe? Often accompagnied with parentheses. See todo_helper.txt, though it is far from complete.

    <hr/>
    This can denote a scene change, or just a page-turning sound à la HPMORPodcast, or just continuation. Go through them manually. See todo_helper.txt for all examples.

    <p>paragraph</p>
    <p dir="ltr" style="line-height: 1.38; margin-top: 0pt; margin-bottom: 0pt;"><p>

    <details>
	    <summary>warning/description of spoiler text</summary>
	    <p>spoiler text</p>
    </details>
    This is a dropdown spoiler tag. Most are either hidding torture or hidding sexual content, but some are just normal content that's hidden for unknown reasons. See todo_helper.txt for all examples. 
    I think it makes sense for the audiobook to assume the reader will read them; another possibility is for it to be automatically skipped; a final possibility is for there to be two generated audiobooks, one with no sussy stuff and one with everything laid bare (TBD which is best). I'll probably deal with them manually.
    
    - " " Quotes should be transformed into <quote> </quote>, and ( ) into <parenthesis> </parenthesis>. This will make easier the processing, I believe. Quotes mean the block.character's voice is used, and parentheses mean either whispering, or lower voice, or something else; TBD.