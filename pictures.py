from PIL import Image, ImageOps
import math



def resize(pic, width = 0, height = 0):
    limitx = 54
    limity = 71
    ox, oy = pic.size
    if width == 0 or height == 0:
        if ox > limitx or oy > limity:
            ratio = ox/float(oy)
            nx = limitx
            ny = int(round(nx/ratio))
        else:
            nx = ox
            ny = oy

    else:
        nx = width
        ny = height
    pic = pic.resize((nx,ny))
    return pic

def distance(c1, c2):
    (r1,g1,b1) = c1
    (r2,g2,b2) = c2
    return math.sqrt((r1 - r2)**2 + (g1 - g2) ** 2 + (b1 - b2) **2)

def colorize(pic, inverted = 0, black = 0):
    colors = {"black" : (0,0,0), "white" : (255,255,255), "red" : (255,0,0),
                "blue" : (0,0,255), "yellow" : (255,255,0), "cyan" : (0,255,255),
                "magenta" : (255,0,255), "green" : (0,255,0)}
    width, height = pic.size
    print(pic.mode)
    if inverted and pic.mode != "RGBA":
        pic = ImageOps.invert(pic)
    elif inverted:
        r,g,b,a = pic.split()
        rgb_image = Image.merge('RGB', (r,g,b))

        inverted_image = ImageOps.invert(rgb_image)

        r2,g2,b2 = inverted_image.split()

        pic = Image.merge('RGBA', (r2,g2,b2,a))

    img = pic.load()
    picArray = []

    for y in range(height):
        line = []
        for x in range(width):
            pixel = img[x,y][:3]
            distances = {}
            for color in colors:
                distances[color]  = (distance(colors[color], pixel))
            if black:
                if distances["black"] > 60:
                    #print(distances["black"])
                    smallest = "white"
                else:
                    smallest = min(distances, key=distances.get)
            else:
                smallest = min(distances, key=distances.get)
            line.append(smallest)
            img[x,y] = (colors[smallest] +  (255, ))
        picArray.append(line)
    #pic.show()
    return picArray



if __name__ == "__main__":
    pic = Image.open("otit3.png")
    #pic.show()
    pic = resize(pic)
    colorize(pic, 0 ,1)
