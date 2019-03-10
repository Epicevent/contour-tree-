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

def image_open(filedir):
    pass