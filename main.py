#!/usr/bin/env python
# Python 2/3 compatibility
import numpy as np
import cv2
from Stereo import Stereo
from PIL import Image

images_folder = "Images/Example1"

stereo = Stereo(images_folder+'/left.png', images_folder+'/right.png', 8)

kernels = [1,5,9]
# print("calculate block matching with SSD")
# for kernel in kernels:
#     depth = stereo.match(kernel,1)  # 6x6 local search kernel, 30 pixel search range
#     # Convert to PIL and save it
#     Image.fromarray(depth).save(images_folder+'/depth_'+str(kernel)+'_SSD.png')

# print("calculate block matching with SAD")
# for kernel in kernels:
#     depth = stereo.match(kernel,2)  # 6x6 local search kernel, 30 pixel search range
#     # Convert to PIL and save it
#     Image.fromarray(depth).save(images_folder+'/depth_'+str(kernel)+'_SAD.png')

depth = stereo.match_dp()
Image.fromarray(depth).save(images_folder+'/depth_DP.png')