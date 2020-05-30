from PIL import Image

def whiteLettersToBlack(fileIn, fileOut):
    # Separate RGB arrays
    im = Image.open(fileIn, 'r')
    R, G, B = im.convert('RGB').split()
    r = R.load()
    g = G.load()
    b = B.load()
    w, h = im.size

    # Convert non-black pixels to white
    threshold = 180
    for i in range(w):
        for j in range(h):
            if(r[i, j] > threshold and g[i, j] > threshold and b[i, j] > threshold):
                r[i, j] = 0
                g[i, j] = 0
                b[i, j] = 0
            else:
                r[i, j] = 255
                g[i, j] = 255
                b[i, j] = 255

    # Merge just the R channel as all channels
    im = Image.merge('RGB', (R, G, B))
    im.save(fileOut)