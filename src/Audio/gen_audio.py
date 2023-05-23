import os
import json
import asyncio
import aiohttp

import logging
logging.basicConfig(filename='gen_audio.log', level=logging.INFO)

import sys
sys.path.append(os.getcwd())

try:
    from config import PLAY_HT_API_KEY, PLAY_HT_USER_ID
except (ImportError, ModuleNotFoundError):
    from src.config import PLAY_HT_API_KEY, PLAY_HT_USER_ID


# Define async function to post each request
async def post_request(session, url, payload, headers, semaphore):
    while True:
        async with semaphore, session.post(url, data=json.dumps(payload), headers=headers) as response:
            if response.status == 429:
                await asyncio.sleep(60)  # Wait for a minute before retrying
                continue
            else:
                return await response.json()

# Define async function to get job status
async def get_job_status(session, url, headers, semaphore, sleep_time=5):
    while True:
        async with semaphore, session.get(url, headers=headers) as response:
            if response.status == 429:
                await asyncio.sleep(60)  # Wait for a minute before retrying
                continue
            else:
                res = await response.json()
                if res['output'] is not None:
                    return res

# Define async function to process each text group
async def process_text_group(session, text_group, post_semaphore, get_semaphore):
    url = "https://play.ht/api/v2/tts"

    headers = {
        "accept": text_group.get('accept', "application/json"),
        "content-type": text_group.get('content_type', "application/json"),
        "Authorization": f"Bearer {PLAY_HT_API_KEY}",
        "X-USER-ID": PLAY_HT_USER_ID
    }

    payload = {
        "text": text_group.get('text'),
        "voice": text_group.get('voice'),
        "quality": text_group.get('quality', "premium"), # draft, low, medium, high, premium
        "output_format": text_group.get('output_format', "flac"),
        "speed": text_group.get('speed', 1),
        "sample_rate": text_group.get('sample_rate', 48000),
    }
    if 'seed' in text_group and text_group['seed'] is not None:
        payload["seed"] = text_group['seed']

    # Semaphore is used here to limit the number of concurrent POST requests
    async with post_semaphore:
        response = await post_request(session, url, payload, headers, post_semaphore)

        if "id" not in response:
            print(f"Payload: {payload}")
            print(f"Response: {response}")
            raise Exception("Error in posting request")
        job_id = response["id"]

    # Get the job status once the job is posted
    url = f"{url}/{job_id}"
    return await get_job_status(session, url, headers, get_semaphore)

# Define function to process multiple text groups asynchronously
async def generate_audio(text_groups, concurrent_posts=50, concurrent_gets=100):
    post_semaphore = asyncio.Semaphore(concurrent_posts)
    get_semaphore = asyncio.Semaphore(concurrent_gets)

    async with aiohttp.ClientSession() as session:
        tasks = [process_text_group(session, text_group, post_semaphore, get_semaphore) for text_group in text_groups]
        results = await asyncio.gather(*tasks, return_exceptions=True) # This will return any exceptions that happened instead of raising them.
        
        # Filter out any None results which may have occurred due to exceptions
        results = [result for result in results if result is not None]
        
        return results

# The second function processes the output of the generate_audio function
def process_output(data):
    transformed_data = []
    for item in data:
        new_item = {
            'text': item['input']['text'],
            'voice': item['input']['voice'],
            'duration': item['output']['duration'],
            'size': item['output']['size'],
            'url': item['output']['url']
        }
        transformed_data.append(new_item)
    return transformed_data


def validate_input(text_groups):
    if not isinstance(text_groups, list):
        raise ValueError("Input must be a list")
    for group in text_groups:
        if not isinstance(group, dict):
            raise ValueError("Each group must be a dictionary")
        if 'text' not in group or 'voice' not in group:
            raise ValueError("Each group must have 'text' and 'voice' keys")
        if not isinstance(group['text'], str) or not isinstance(group['voice'], str):
            raise ValueError("'text' and 'voice' values must be strings")
    return True


if __name__ == '__main__':
    text_inputs = [
        # {
        #     'text': "Oh, it matters. See, even after you get rich and Law all that stuff out of existence, Very Serious People go on worrying about whether it will come back a hundred years later, if we let ourselves start to drift evolutionarily on the Good-Evil axis. I hadn't actually been informed as yet, but considering the choices I made in some test-pranks as a kid, I expect I'd have been told a few years later that my place on the Good-Evil axis wouldn't have entitled me to much support for having kids of my own. Which, fine, fair enough, if I'm the sort of person who goes around constantly assessing how much reciprocation other people owe me, instead of just being nice, I shouldn't be too surprised if Civilization decides it doesn't owe me much. Because what have I done for them, right, under the rules the way I say they should work? I can either prove they're wrong about people like me being unnecessary, or get out of the gene pool, fair enough. My ambition before I ended up here was to fairly make a billion labor-hours, and then marry about two dozen women and have about a hundred and forty-four kids. The first part to show them how much they need people like me, and the second part to unilaterally give the next generation some more people like me whether the rest of Civilization likes that or not.",
        #     'voice': 'flynn'
        # },
        # {
        #     'text': "...which I should, probably, just never think about again, because this world is not and never will be a test of my ability to shine inside Civilization. If I win here, it won't be because I was special, it'll be because I came in with a ton of knowledge that any other dath ilani might have. And if I lose here, it'll be because there were gods smarter than any human being who ate all the low-hanging-fruit that anybody at all in dath ilan could've found. But hey, I'm adaptable, I can reorient my entire life, might take me a couple of minutes but I can do it. I just - felt it might be helpful to say out loud, once, before it all drifts away. Help if somebody else knew, even for a halfminute, before I let it go.",
        #     'voice': 'flynn'
        # },
        # {
        #     'text': "Moving on. If churches are going to war, it means that the gods being smart doesn't prevent humans from being stupid, not sure why, but it obviously doesn't, so maybe I can still help there. Priority question, how much of my knowledge still holds here, if any. Does running electricity through water produce two gases, one of them lighter than air, which can be burned to yield water again?",
        #     'voice': 'flynn'
        # },
        # {
        #     'text': 'If molecular chemistry is the same, higher levels of organization will probably also be the same; and knowledge about steelmaking - or that synthetic hormones can signal the female reproductive system to not ovulate - will probably also hold.',
        #     'voice': 'fletcher'
        # },
        # {
        #     'text': "Just being nice is very stupid, if your planet's selecting for that they're going to have horrible problems the first time they encounter anyone else. - I'm not an alchemist, I can look it up but probably after the translation spell runs out unless that information is really important information.", 
        #     'voice': 'victor'
        # },
        # {
        #     'text': "If 'nice' sounds like a kind of thing that can be 'stupid' we've got some kind of translation difficulty running, that's a type error. 'Nice' is part of the utility function. If you don't already know that water is composed of hydrogen and oxygen, it probably isn't... I guess you could just not know what anything is made of. Do you know what water is made of that's not two one-proton atoms and one eight-proton atom?",
        #     'voice': 'flynn'
        # },
        # {
        #     'text': "I don't know what a proton is. Water freezes at a little above the ambient air temperature outdoors here at the Worldwound in the summer and floats when it's ice, and boils at a temperature you can get over a normal nonmagical fire and then is steam, and holds heat well compared to metal or plant matter or something. When it freezes in the sky it forms snowflakes.",
        #     'voice': 'victor'
        # },
        # {
        #     'text': "Sounds correct. Do snowflakes have six-sided structure under a microscope? Where I come from, that happens because molecules with two hydrogen and one oxygen have a least-energy crystal configuration that's hexagonal. If all of that is still true and for the same reasons, then I still know how to make advanced steel and build electrical generators. And the methodology I know to regenerate more of that knowledge will apply unchanged. Male and female reversible contraception... was tech in a relatively advanced state where I can't reproduce it directly. I can reproduce the methodology that generates it.",
        #     'voice': 'flynn'
        # },
        # {
        #     'text': "Snowflakes have six sides. What's steel used for, what're electrical generators used for -",
        #     'voice': 'victor'
        # },
        # {
        #     'text': "You don't have steel. Right then, if steel is a possible thing here and you don't have it, that's step one in climbing the tech tree. It's a metal that's harder than other metals, while still possible to work with at all; variations on it don't rust, keep edges better, and so on. What's your current advanced metallurgy like? Bronze, iron...",
        #     'voice': 'flynn'
        # },
        # {
        #     'text': "Magic weapons. They don't rust and keep an edge perfectly and they last forever. We have bronze and iron. I've seen work done in steel but I've also seen work done in adamantine, mithril, skymetal, there's lots of metals that exist but aren't mass-producible and I don't know what they'd be used for if they were.", 
        #     'voice': 'victor'
        # },
        # {
        #     'text': "Huh. Yeah, some of those terms aren't translating. I wonder if I actually know anything portable about steel, or there's just some nearly analogous metal here, or if steel still exists but there's processes that don't exist in dath ilan for building other metals above or beyond it. Let's try a basic tech on a higher level of organization. How expensive is it to produce a thousand copies of one book and how would you do that?",
        #     'voice': 'flynn'
        # },
        # {
        #     'text': "I think it costs about what a laborer would earn in three years to get a thousand copies, and you'd go to a printing shop where they'd line up moveable metal - tile things? - with letters on them to make the pages, and then ink them and stamp the parchment. I think the biggest contributing expense is the paper and the binding. Cheliax releases national histories every few years but I don't think other places can afford to do that.",
        #     'voice': 'victor'
        # },
        # {
        #     'text': "You got printing presses, okay. I may or may not know anything useful about cheaper paper, if a book's worth of paper costs a day's wages. Let's try refrigeration, how expensive is ice in hotter climates and what would you do to get it?",
        #     'voice': 'flynn'
        # },
        {
            'text': "...I think you mostly cannot buy ice in Cheliax. I guess you could have someone ship it from the far north but I don't know this to have ever been done commercially, and my father's a merchant, I was broadly familiar with the things people were trying commercially in shipping. Probably you'd pay a spellcaster to prepare and cast Snowball for you, which would cost ten laborer-days and be about a hands-ful.",
            'voice': 'victor'
        }
    ]
    
    validate_input(text_inputs)
    
    result = asyncio.run(generate_audio(text_inputs))
    print(process_output(result))