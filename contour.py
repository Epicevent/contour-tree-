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


from PIL import Image ,ImageDraw
import numpy as np
import jstree

def image_vectorize(gray_image_object):
   image_array = np.asarray(gray_image_object)
   N,M = np.shape(image_array)[0:2]
   vectorized = image_array.flatten('F')[0:N*M]
   return vectorized



def draw_points( image_object, joint_bifurcation_vector):
    pass

def increasing_arg_sorting(im_vector):
    sorted_index_list = np.argsort(im_vector)
    size = np.size(im_vector)
    # check cond1 and cond2
    cond1 = (size == len(sorted_index_list))
    cond2 = set(sorted_index_list) == set([i for i in range(size)])
    return sorted_index_list






def center_to_xy(center):
    return (100,100)

def xy_representing_circle(center,radius):
    return (200,99,300,101)


def draw_filled_circle (imgae_object,xy_of_center,radius,color = 'red'):
    draw = ImageDraw.Draw(imgae_object)
    xy = xy_representing_circle(xy_of_center,radius)
    draw.ellipse(xy,  fill=color,outline=color)


if __name__ =="__main__":
    im = Image.open('IM-0001-0001.jpeg')
    grayimg = im.convert('LA')
    v = image_vectorize(grayimg)
    number_of_cols , number_of_rows = grayimg.size
    jointsplittree = jstree.JStree(number_of_rows,number_of_cols)
    increasing_indices = increasing_arg_sorting(v)
    jointsplittree.make(increasing_indices)
    joint_bifurcation_point = jointsplittree.get_bifurcation_point()
    print(jointsplittree.max_n_comp)
    jointsplittree.make(increasing_indices[::-1]) #reverse
    split_bifurcation_point = jointsplittree.get_bifurcation_point()

    print (np.sum(joint_bifurcation_point))
    print(np.sum(split_bifurcation_point))
    representing_img = grayimg.convert('RGBA')
    draw_filled_circle(representing_img,1001,1)
    representing_img.show()
