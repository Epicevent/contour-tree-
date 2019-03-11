"""
 purpose : To make database of contour tree bifurcation points

  contour tree bifurcation points = joint tree bifurcation points Unions split tree bifurcation points

  how to use :

  there is two option :
    python contour.py [image file name] [directory name to save result]

    python3 contour.py [image file name]

 result :

  txt file : [image file name]
  txt file format :
  [
    title : [image file name] \n
    image size : [# of rows] [# of cols] \n
    [ data of bifurcation points ]
  ]
  data of bifurcation points
    the number in order index order
    0 0 0 0 ...  1 ...  2 ... 3 ...0 0 0 0
    < number of numbers in line = number of index in image = rows * cols >

    0 means "it is not bifurcation point."
    1 means "it is bifurcation point only in joint tree."
    2 means "it is bifurcation point only in split tree."
    3 menas "it is bifurcation point in both joint tree and split tree."

    index order :
     [i th] index means location :: ( i% #ofrows , i/ #of cols)
    so it does like following ... if image size is 4 by 5
    0 4 8  12 16
    1 5 9  13 17
    2 6 10 14 18
    3 7 11 15 19
"""

# libraries
from PIL import Image
import numpy as np

"""
    [index, value]
    ex. [[0, 1], [1, 255], [2, 200], ...]
"""

def image_open(_imgFile):
    """
    Read the img and return PIL Image object
    """
    # Read the image file
    img = Image.open(_imgFile)
    return img

def image_get_width(_img):
    """
    Input: PIL.Image _img
    Output: int imgWidth
    """
    imgWidth = _img.width
    return imgWidth

def image_get_height(_img):
    """
    Input: PIL.Image _img
    Output: int imgHeight
    """
    imgHeight = _img.height
    return imgHeight

def image_to_numpy_array(_img):
    """
    Input: PIL.Image _img
    Description: conver the PIL image into a grey scale image(8-bit pixels, black-and-white)
    Output: numpy array
    """
    img_greyscale = _img.convert('L')
    npImgArr = np.array(img_greyscale)
    return npImgArr