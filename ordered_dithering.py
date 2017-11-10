#!/usr/bin/env python2
# -*- coding:utf-8 -*-

'''


Here we use the base kernel
              |  1  2  |
  I\2(i, j) = |  3  0  |

to produce larger kernels by this transformation:
               |  4 * I\n + 1    4 * I\n + 2  |
  I\2n(i, j) = |  4 * I\n + 3    4 * I\n      |

References:
<1> http://en.wikipedia.org/wiki/Ordered_dithering
<2> Purdue University: Digital Image Processing Laboratory Image Halftoning.
'''

#import Image
from PIL import Image, ImageEnhance
import sys
import os
#from __future__ import unicode_literals

def gen_matrix( e ):
  ''' Generating new matrix.
      @param e The width and height of the matrix is 2^e.
      @return New 2x2 to 2^e x 2^e matrix list.
  '''
  if e < 1: return None
  m_list = [ [[1,2],[3,0]] ]
  _b = m_list[0]
  for n in xrange(1, e):
    m = m_list[ n - 1 ]
    m_list.append( [
      [4*i+_b[0][0] for i in m[0]] + [4*i+_b[0][1] for i in m[0]],
      [4*i+_b[0][0] for i in m[1]] + [4*i+_b[0][1] for i in m[1]],
      [4*i+_b[1][0] for i in m[0]] + [4*i+_b[1][1] for i in m[0]],
      [4*i+_b[1][0] for i in m[1]] + [4*i+_b[1][1] for i in m[1]],
    ] )
  return m_list


def ordered_dithering( pixel, size, matrix ):
  """ Dithering on a single channel.
      @param pixel PIL PixelAccess object.
      @param size A tuple to represent the size of pixel.
      @param matrix Must be NxN, and N == 2^e where e>=1
  """
  X, Y = size
  N = len(matrix)
  
  T = [[255*(matrix[x][y]+0.5)/N/N for x in xrange(N)] for y in xrange(N)]
  for y in xrange(0, Y):
    for x in xrange(0, X):
      pixel[x,y] = 255 if pixel[x,y] > T[x%N][y%N] else 0


if __name__ == "__main__":

  if not os.path.exists("results"):
    os.makedirs("results")

  for file in os.listdir("./"):
    if file.endswith(".png") or file.endswith(".gif") or file.endswith(".jpg"):
      im = Image.open(file).convert('L')
      i = 2
      ordered_dithering(im.load(), im.size, gen_matrix(i)[i-1])
      im.save( "results/"+file+"_.png" )
      
      im = Image.open(file).convert('L')
      scale_value=1.35
      contrast = ImageEnhance.Contrast(im)
      im = contrast.enhance(scale_value)

      brightness = ImageEnhance.Brightness(im)
      im = brightness.enhance(scale_value)

      ordered_dithering(im.load(), im.size, gen_matrix(i)[i-1])
      im.save( "results/"+file+"_contrast.png" )

