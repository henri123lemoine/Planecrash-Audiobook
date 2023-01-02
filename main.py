
from settings import BOARD_URL, JSON_PATH, VOICE_DICT
from Story.get_thread import Thread
from Story.get_board import Board

# Get one thread
thread_title = "what the truth can destroy"

thread = Thread.load_from_json(f"{JSON_PATH}/{thread_title}.json")




# get = False
# load = True
# save = False

# if get:
#     story = Story().extract(BOARD_URL)
# if load:
#     story = Story.load_from_json(JSON_PATH)
# if save:
#     story.save_json(JSON_PATH)



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
    