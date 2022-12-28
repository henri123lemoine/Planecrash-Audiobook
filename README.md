# Planecrash_Audio

The story information is stored in the Story class.
It contains a title string, an authors list, a characters list, a board url string, and threads (found at the board url).

The threads information is stored in the Thread class.
It contains a title string, an authors list, a characters list, a thread url string, and blocks (found at the thread url).

The blocks information is stored in the Block class.
It contains a character string, an screenname string, an author string, an icon url string, a block url string, a content string (containing html describing the block), and a content text string (containing only the story-text part of the html).

#TODO
- make things cleaner (rename classes and functions to make it more readable, make the code more pythonic, and add more comments when deemed necessary)
- Blocks should contain a list 'voices' of voice-text tuples, describing what voice should say what and in what order.
- Write code to make easier the process of generating an audio episode from the story. This may include:
    1. automatically separating threads in 30-minutes-length list of blocks.
    2. function to generate audiobook from list of blocks (including intro and outro).
 