
from settings import BOARD_URL, JSON_PATH, VOICE_DICT
from Story.get_voice import Voice
from Story.get_block import Block
from Story.get_thread import Thread
from Story.get_board import Board


def main():
    board = Board().extract(BOARD_URL)
    board.save_json(JSON_PATH)

    board = Board.load_from_json(JSON_PATH)

    blocks = board.get_all_blocks()

if __name__ == "__main__":
    main()
    