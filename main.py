
from settings import BOARD_URL, JSON_PATH, VOICE_DICT
from functions import Story, Voice

story = Story().extract(BOARD_URL)

get = True
load = False
save = True

if get:
    story = Story().extract(BOARD_URL)
if load:
    story = Story.load_from_json(JSON_PATH)
if save:
    story.save_json(JSON_PATH)


# from helper_functions import*
# b = story.threads[0].blocks[0]
# print(process_voice_content(b.content))

def main():
    # story = Story().extract(BOARD_URL)
    # story.save_json(JSON_PATH)

    # story = Story.load_from_json("data/story.json")

    # blocks = story.get_all_blocks()
    pass
if __name__ == "__main__":
    main()
    