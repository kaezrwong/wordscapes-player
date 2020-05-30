import pyautogui as pag
import time

import whiteLettersToBlack
import scrabbleSolver

time.sleep(2)
topLeftX = 1823
topLeftY = 1165
botRightX = 2644
botRightY = 1716
image = pag.screenshot("screenshot.png", region=(topLeftX, topLeftY, botRightX-topLeftX, botRightY-topLeftY))

from PIL import Image 
image_file = Image.open("screenshot.png") # open colour image
image_file = image_file.convert('1') # convert image to black and white
image_file.save('bw.png')

# Tolerance level for checkPos function
checkPosTolerance = 50

# pag.locateAll returns multiple points for each image
# checkpos checks if the centres of these points belong 
# to the same letter. Return True if new letter, else False.
def checkPos(pos1, pos2):
    error = 0
    for i in range(2):
        error += abs(pos1[i-1] - pos2[i-1])
    if error < checkPosTolerance:
        return False
    else:
        return True

def checkPosLoop(pos, posList):
    for i in range(len(posList)):
        if not checkPos(pos, posList[i-1]):
            return False
    return True

# Read in letters
#posA = pag.locateOnScreen('Letters/A.png', region=(1823, 1165, 2644-1823, 1716-1165))
listOfLetters = ['A','B','D','E','H','K','L','M','N','O','P','R','S','T','U','V','W','Y','I','C','G']
boardLetters = ""
letterPositions = []


for letter in listOfLetters:
    oldPos = None
    for posA in pag.locateAll('Letters/{}.png'.format(letter), "screenshot.png", grayscale=True, confidence=0.9):
        posA = pag.center(posA)
        if oldPos == None:
            oldPos = posA
            pag.click((posA[0]+topLeftX),(posA[1]+topLeftY))
            if checkPosLoop(posA, letterPositions):
                boardLetters += letter
                letterPositions.append(posA)

        elif checkPos(oldPos, posA):
            oldPos = posA
            pag.click((posA[0]+topLeftX),(posA[1]+topLeftY))
            if checkPosLoop(posA, letterPositions):
                boardLetters += letter
                letterPositions.append(posA)

    #time.sleep(0.2)

if len(boardLetters) == 0:
    whiteLettersToBlack.whiteLettersToBlack("screenshot.png", "black_and_white.png")

    for letter in listOfLetters:
        oldPos = None
        for posA in pag.locateAll('Letters/{}.png'.format(letter), "black_and_white.png", grayscale=True, confidence=0.9):
            posA = pag.center(posA)
            if oldPos == None:
                oldPos = posA
                #pag.click((posA[0]+topLeftX),(posA[1]+topLeftY))
                if checkPosLoop(posA, letterPositions):
                    letterPositions.append(posA)
                    boardLetters += letter

            elif checkPos(oldPos, posA):
                oldPos = posA
                #pag.click((posA[0]+topLeftX),(posA[1]+topLeftY))
                if checkPosLoop(posA, letterPositions):
                    letterPositions.append(posA)
                    boardLetters += letter

        #time.sleep(0.2)

boardLetters = boardLetters.lower()
print(boardLetters)
print(letterPositions)

anagrams = scrabbleSolver.solve(boardLetters.lower())
boardLettersList = list(boardLetters)
for word in anagrams:
    temp = list.copy(boardLettersList)
    print("New word is: ", word, " and temp is reset to ", temp, "boardletterslist is ", boardLettersList)
    isMouseDown = False   
    for i in range(len(word)):
        for j in range(len(temp)):
            #print(word[i], temp[j])
            if word[i] == temp[j]:
                #print('Above was compared')
                posB = letterPositions[j]
                pag.moveTo((posB[0] + topLeftX), (posB[1] + topLeftY))
                if not isMouseDown:
                    pag.mouseDown()
                temp[j] = '0'
                break
                time.sleep(0.1)
    pag.mouseUp()
    time.sleep(1)


'''
# Drag cursor to create word
# Code works for 4 letter words
first4 = (2236, 1281)
second4 = (2406, 1440)
third4 = (2233, 1623)
fourth4 = (2057, 1446)

pag.moveTo((first4))
pag.mouseDown()
pag.moveTo(second4)
pag.moveTo(third4)
pag.moveTo(fourth4)
pag.mouseUp()
'''