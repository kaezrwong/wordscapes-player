import pytesseract
import cv2
from PIL import Image
import PIL.ImageOps  

# Invert image to always be black
def convertLettersToBlack(imageName):
    img = Image.open(imageName)
    _img = img.load()
    row = img.size[0]/2
    col = img.size[1]/2
    if ((int(_img[row,col][0]) < 240) and (int(_img[row,col][1]) < 240) and (int(_img[row,col][2]) < 240) ):
        inverted_image = PIL.ImageOps.invert(img)
        inverted_image.save(imageName)

convertLettersToBlack("test6.png")

img = cv2.imread('test6.png')

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
    if (w < 300 and h > 250 and h < 350):
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

        new_size = (600, 600)
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

letters = pytesseract.image_to_string("concatenated.png", lang='eng', config='--psm 7')
print(letters)
print(letter_locations)