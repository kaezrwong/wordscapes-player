import pyautogui as pag
import time
import pytesseract
import cv2
from PIL import Image
import PIL.ImageOps  

import whiteLettersToBlack
import scrabbleSolver

level = int(input("Please enter the current level: "))

topLeftX = 2323
topLeftY = 1134
botRightX = 2841
botRightY = 1642

# Next level button/centre of circle containing letters
nextLevelXY = (2598, 1395)

# Rearrange letter button
rearrangeButton = (2245, 1109)

# Close Piggybank button
piggybankButton = (2839, 464) 

# Tolerance level for checkPos function
checkPosTolerance = 50

# Current Stage
# Levels 1-80 = 1
# Levels 81- = 2
stage = 2

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

# Invert image to always be black
def convertLettersToBlack(imageName):
    img = Image.open(imageName)
    _img = img.load()
    row = img.size[0]/2
    col = img.size[1]/2
    if ((int(_img[row,col][0]) < 240) and (int(_img[row,col][1]) < 240) and (int(_img[row,col][2]) < 240) ):
        inverted_image = PIL.ImageOps.invert(img)
        inverted_image.save(imageName)

solvedPuzzles = 0
for i in range (100):
    if not (level % 80):
        print("Waiting for next stage...")
        time.sleep(9)
    elif not (level % 16):
            print("Waiting for next set...")
            time.sleep(2)

    print("Level " + str(level))
    letters = ""
    while (len(letters) < 6):
        letters = ""
        print("Starting loop")
        # Screenshot of ROI
        time.sleep(1) # Allow time for screenshot to load
        image = pag.screenshot("screenshot.png", region=(topLeftX, topLeftY, botRightX-topLeftX, botRightY-topLeftY))
        
        # Read in letters
        #posA = pag.locateOnScreen('Letters/A.png', region=(1823, 1165, 2644-1823, 1716-1165))
        #listOfLetters = ['A','B','D','E','H','K','L','M','N','O','P','R','S','T','U','V','W','Y','I','C','G','X','F','T2','F2','E2','R2','I2']
        #listOfLetters = ['X','B','K','N','Y','M','A','L','V','S','D','E','U','J','F','G','R','H','T','W','Q','O','I','C','P']
        boardLetters = ""
        letterPositions = []

        whiteLettersToBlack.blackLettersToWhite("screenshot.png", "white_letters.png")

        convertLettersToBlack("white_letters.png")

        img = cv2.imread('white_letters.png')

        resizeFactor = 2
        img = cv2.resize(img, None, fx=resizeFactor, fy=resizeFactor)
        img_copy = cv2.resize(img, None, fx=resizeFactor, fy=resizeFactor)

        h, w, _ = img.shape

        letters = pytesseract.image_to_boxes(img)
        letters = letters.split('\n')
        letters = [letter.split() for letter in letters]

        for i, letter in enumerate(letters):
            cv2.rectangle(img, (int(letter[1]), h - int(letter[2])), (int(letter[3]), h - int(letter[4])), (0,0,255), 1)

        cv2.imwrite('output.png', img)

        #input()

        edged = cv2.Canny(img, 175, 200)

        contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(img, contours, -1, (0,255,0), 3)

        #cv2.imshow("Show contour", img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        letter_index = []
        letter_locations = []

        for i,c in enumerate(contours):
            rect = cv2.boundingRect(c)
            x,y,w,h = rect

            #box = cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255), 2)
            cropped = img[y: y+h, x: x+w]
            if (w < 300 and h > 150 and h < 350):
                cv2.imwrite("blobby"+str(i)+".png", cropped)
                letter_locations.append(x+w/2)
                letter_locations.append(y+h/2)
                #print("Blobby "+str(i) + " has size: "+ str(w) + "x" + str(h))
                #print(pytesseract.image_to_string(cropped, lang='eng', config='--psm 10'))
                
                # Add border and read
                originalImage = cv2.imread('blobby'+str(i)+'.png')
                grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
                (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
                cv2.imwrite('contour_removed.png', blackAndWhiteImage)

                old_im = Image.open('contour_removed.png')
                old_size = old_im.size

                new_size = (180, 350)
                new_im = Image.new("RGB", new_size)   ## luckily, this is already black!
                new_im = PIL.ImageOps.invert(new_im)
                new_im.paste(old_im, ((new_size[0]-old_size[0])//2, (new_size[1]-old_size[1])//2))
                new_im
                new_im.save("bordered"+str(i)+".png")
                letter_index.append(i)
                #print(pytesseract.image_to_string("bordered.png", lang='eng', config='--psm 10'))
                #input()

        im1 = cv2.imread("bordered"+str(letter_index[0])+".png")
        im2 = cv2.imread("bordered"+str(letter_index[1])+".png")
        im_h = cv2.hconcat([im1, im2])
        letter_index.pop(0)
        letter_index.pop(0)
        for i in letter_index:
            im = cv2.imread("bordered"+str(i)+".png")
            im_h = cv2.hconcat([im_h, im])

        letter_index.clear()

        cv2.imwrite("concatenated.png", im_h)

        letters = pytesseract.image_to_string("concatenated.png", lang='eng', config="-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 7")
        if len(letters) < 6:
            pag.click(rearrangeButton)
            print("Rearranging letters")
            letter_index.clear()
            letter_locations.clear()

    for i in letters:
        if (i != ' '):
            boardLetters += i
    
    boardLetters = boardLetters.lower()
    print("The board letters are: " + str(boardLetters))
    #print(letter_locations)

    anagrams = scrabbleSolver.solve(boardLetters.lower())
    boardLettersList = list(boardLetters)
    for word in anagrams:
        temp = list.copy(boardLettersList)
        print("New word is: ", word, ".", sep='')
        isMouseDown = False   
        for i in range(len(word)):
            for j in range(len(temp)):
                #print(word[i], temp[j])
                if word[i] == temp[j]:
                    #print('Above was compared')
                    posA = int(letter_locations[2*j]/2)
                    posB = int(letter_locations[2*j+1]/2)
                    pag.moveTo((posA + topLeftX), (posB + topLeftY))
                    if not isMouseDown:
                        pag.mouseDown()
                    temp[j] = '0'
                    break
                    time.sleep(0.1)
        pag.mouseUp()
        time.sleep(1)
        
    solvedPuzzles += 1
    print("Number of solved puzzles this session: ", solvedPuzzles)
    time.sleep(11 + len(anagrams)/5)
    # Press next level button
    pag.click(nextLevelXY)
    level += 1

    # Allow time for next level to load
    time.sleep(2)


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
