import json

# from settings import Y
from functions import Story


def main():
    story2 = Story.load_from_json('data/story.json')

if __name__ == "__main__":
    main()
    