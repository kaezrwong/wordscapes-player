# wordscapes-player
Python program to play the phone game Wordscapes - an anagramming crossword game.
This program reads the board tiles, finds words that can be made from these
letters (using an English dictionary n=84000) and inputs these words into the 
crossword. The number of levels to be continuously solved can be chosen.

INSTRUCTIONS
Connect phone with computer with Vysor or any similar platform that allows 
remote viewing and control of a phone.
Use findPixelBounds.py to enter the boundary coordinates of the board (circle
containing the tiles).
Run image_parsing.py to begin solving.

NOTES 
pyAutoGui is used to control the cursor functionality - drag the mouse to
any corner of the screen to activate the fail-safe and halt the program.
