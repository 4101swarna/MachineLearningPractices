from functools import reduce
from PIL import ImageChops, Image
import math, operator


im1 = Image.open("lotus.png")
im2 = Image.open("lotus-1.png")

def rmsdiff(im1, im2):
    print("Calculate the root-mean-square difference between two images")
    h = ImageChops.difference(im1, im2).histogram()

    #calculate rms
    return math.sqrt(reduce(operator.add, map(lambda h, i: h*(i**2), h, range(256))) / (float(im1.size[0]) * im1.size[1]))
def equal(im1, im2):
    return ImageChops.difference(im1, im2).getbbox() is None
rmsdiff(im1, im2)
equal(im1, im2)