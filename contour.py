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
import PIL

# libraries
import sys
from PIL import Image
import numpy as np

# if 0 argument is given
if len(sys.argv) is 1:
    print("Usage: python contour.py [image file name] [directory name to save result] or python3 contour.py [image file name]")

# if more than 3 arguments are given
if len(sys.argv) >= 4:
    print("Usage: python contour.py [image file name] [directory name to save result] or python3 contour.py [image file name]")

# if 2 argument is given
# python contour.py [image file name] [directory name to save result]
if len(sys.argv) is 3:
    pass

# if 1 argument is given
# python3 contour.py [image file name]
if len(sys.argv) is 2:
    img = Image.open(sys.argv[1])
    imgHeight = img.height
    imgWidth = img.width
    # img.convert('L')
    npImgArr = np.array(img)
    print(img.size)
    print(npImgArr)
    print(npImgArr.size)
    # To-Be Implemented
    # flatten the 2D matrix to 1D matrix in columnwise order
    # Use ravel instead of flatten because ravel does not copy the ndarray so it is faster.
    arr=npImgArr.ravel('F')
    print(arr)
    print(arr.size)
    # Calculate bifurcation points

    # file output
    f=open(sys.argv[1]+'.txt','w')
    f.write('title : '+sys.argv[1]+'\n')
    f.write('image size : ['+str(imgHeight)+' of rows] ['+str(imgWidth)+' of cols]')
    # [data of bifucation points]

    f.close()
