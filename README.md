# Planecrash_Audio

This Project has as goal to produce a fully automatic Text-To-Speech audiobook of Planecrash/Project Lawful.

Files in `src/`:
- `Audio/gen_audio.py` contains the code to create the audio using the play.ht TTS API.
- `Audio/get_voices.py` contains the code to get the list of--optionally, filtered--voices available from the V2-Ultrarealistic voices on the play.ht API.

- `Story/get_block.py` extracts information from a single tag. Tags contain a character name, screenname, author name, icon url, glofic.com url, and html.
- `Story/get_thread.py` extracts information from a single thread. Threads contain a title, a list of authors, a list of characters, and a list of tags.
- `Story/get_board.py` extracts information from a board. Boards contain a title, a list of authors, a list of characters, and a list of threads. `save_chunks` splits the story into chunks of 100-200 tags, and saves each chunk as a json file in `data/board_chunks/`.

- `make_audiobook.ipynb` contains the code to create the audiobook chunks and process them, as well as get the audio from Play.ht. It also is a convenient place to test the code, and to run a local version of the website.

- `app.py` contains the code to run the website, with relevant templates html files in `templates/`.

- `settings.py` contains the settings for the audiobook, including the Play.ht voice of each character, and some other constants. `config.py` contains the API Keys for Play.ht, formatted as follows:
```python
PLAY_HT_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
PLAY_HT_USER_ID = "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

#TODO
- Write code to make easier the process of generating an audio episode from the story. This may include:
    1. automatically separating threads in 30-minutes-length list of blocks. See `https://github.com/Cakoluchiam/fiction` for a way to separate the story in sensible chapters.
    2. make rapid testing easier using a local version of the website.

- Determine which characters have what voice, and what consistent accents to give each region from Golarion. Create custom voices if need be.

- Generate the full audiobook. Contact Play.ht to get custom prices.