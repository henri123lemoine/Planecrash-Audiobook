
from settings import BOARD_URL
from functions import Story, Voice

def main():
    story = Story()
    story.extract(board_url=BOARD_URL)
    story.save_json("data/story.json")

    story = Story.load_from_json("data/story.json")

    blocks = story.get_all_blocks()

if __name__ == "__main__":
    main()
    