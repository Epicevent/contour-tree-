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






def center_to_xy(center,num_of_cols,num_of_rows):
    # center is represented by jstree. (
    # xy coordinate
    x = center / num_of_rows # if center 0 then x =0 ,if center
    y = center % num_of_cols
    return (x,y)

def xy_representing_circle(centerxy,radius):
    x,y = centerxy

    return (x-radius,y-radius,x + radius,y+radius)


def draw_filled_circle (imgae_object,xy_of_center,radius,color = 'red'):
    draw = ImageDraw.Draw(imgae_object)
    if radius > 0:
        xy = xy_representing_circle(xy_of_center,radius)
        draw.ellipse(xy,  fill=color,outline=color)
    else:
        draw.point(xy_of_center, fill=color)
def draw_all_bifurcation_point(image_object,number_of_rows_im , number_of_cols_im,joint_point,split_point):

    radius_of_contour_point = max(int((number_of_rows_im + number_of_cols_im)*0.001),1)
    radius =0
    for i in range(len(joint_point)):
        xycenter = center_to_xy(i, number_of_cols_im, number_of_rows_im)
        if joint_point[i] and split_point[i]:
            draw_filled_circle(image_object,xycenter,radius_of_contour_point,'red')
        if joint_point[i] and not split_point[i]:
            draw_filled_circle(image_object, xycenter, radius, 'blue')
        if split_point[i] and not joint_point[i]:
            draw_filled_circle(image_object, xycenter, radius, 'green')
def get_bifurcation_points(imagefilename):
    im = Image.open(imagefilename)
    grayimg = im.convert('LA')
    v = image_vectorize(grayimg)
    number_of_cols, number_of_rows = grayimg.size
    jointsplittree = jstree.JStree(number_of_rows, number_of_cols)
    increasing_indices = increasing_arg_sorting(v)
    jointsplittree.make(increasing_indices)
    joint_bifurcation_point = jointsplittree.get_bifurcation_point()

    jointsplittree.make(increasing_indices[::-1])  # reverse
    split_bifurcation_point = jointsplittree.get_bifurcation_point()

    representing_img = grayimg.convert('RGB')
    draw_all_bifurcation_point(representing_img, number_of_rows, number_of_cols,
                               joint_bifurcation_point, split_bifurcation_point)
    txtdata = "title : " + imagefilename +"\n"
    txtdata += "size : " +str(number_of_rows)+" " +str(number_of_cols)+"\n"
    for i in range(len(joint_bifurcation_point)):
        if joint_bifurcation_point[i] and split_bifurcation_point[i]:
            txtdata+="3"
        elif joint_bifurcation_point[i] and not split_bifurcation_point[i]:
            txtdata+="1"
        elif not joint_bifurcation_point[i] and split_bifurcation_point[i]:
            txtdata+="2"
        else:
            txtdata+="0"
        txtdata+=" "
    return representing_img , txtdata

import sys
import glob, os
if __name__ =="__main__":
    argc =len(sys.argv)
    if argc == 1:
        arg1='IM-0001-0001.jpeg'

    if argc <= 2:
        arg2 =os.curdir
    else:
        arg2 = sys.argv[2]
    if arg1=='*.jpeg':# all JPEG images in the current directory.
        for infile in glob.glob("*.jpeg"):
            file, ext = os.path.splitext(infile)
            rep_img, txt = get_bifurcation_points(infile)
            rep_img.save(arg2+"/B"+infile,"JPEG")
            with open(arg2 + "/B" + file+".txt", "w") as f:
                f.write(txt)

    else:
        file, ext = os.path.splitext(arg1)
        rep_img, txt =get_bifurcation_points(arg1)
        rep_img.save(arg2+"/B"+arg1,"JPEG")
        with open(arg2 + "/B" + file + ".txt", "w") as f:
            f.write(txt)