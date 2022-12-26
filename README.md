# Planecrash_Audio
Each thread is made of blocks. Each block contains a few pieces of information:

Character "post-character" (optional)
Screenname "post-screenname" (optional)
Author "post-author" (always present)
Icon "post-icon" (optional)
Content "post-content" (optional)
Each block is contained in a div with class "post-container post-post" or "post-container post-reply"

The thread itself contains:

Title "post-title"
Authors "post-author"'s
Characters "post-character"'s (optional)
Blocks "post-container post-post"'s and "post-container post-reply"'s
The thread is contained in a div with class "content"