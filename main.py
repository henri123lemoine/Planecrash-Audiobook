
from settings import BOARD_URL
from functions import Story

story = Story()
story.extract(board_url=BOARD_URL)
story.save_json("data/story.json")
print("Done")
# story2 = Story.load_from_json("data/story.json")

def main():
    # story = Story()
    # story.get_story()
    # story.save_json("data/story.json")
    pass

if __name__ == "__main__":
    main()
    