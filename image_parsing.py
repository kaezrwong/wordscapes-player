import pyautogui as pag
import time

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

# Read in letters
#posA = pag.locateOnScreen('Letters/A.png', region=(1823, 1165, 2644-1823, 1716-1165))
for posA in pag.locateAll('Letters/A.png', "screenshot.png", grayscale=True, confidence=0.9):
    print(posA)
    posA = pag.center(posA)
    pag.click((posA[0]+topLeftX),(posA[1]+topLeftY))
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