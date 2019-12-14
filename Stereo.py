import numpy as np
import math
from PIL import Image

class Stereo:
    def __init__(self,leftI,rightI,disparity_range_):
        self.disparityRange = disparity_range_

        # Load in both images, assumed to be RGBA 8bit per channel images
        self.leftImage = Image.open(leftI).convert('L')
        self.rightImage = Image.open(rightI).convert('L')
        self.left = np.asarray(self.leftImage)
        self.right = np.asarray(self.rightImage)
        
    def match(self,kernel,tp):
        print("calculating disparity matrix for w = ",kernel)
        w, h = self.leftImage.size  # assume that both images are same size   
        
        # Depth (or disparity) map
        depth = np.zeros((w, h), np.uint8)
        depth.shape = h, w
        
        kernel_half = int(kernel / 2)    
        offset_adjust = 255 / self.disparityRange  # this is used to map depth map output to 0-255 range
        
        for y in range(kernel_half, h - kernel_half):      
            print(".", end="", flush=True)  # let the user know that something is happening (slowly!)
            
            for x in range(kernel_half, w - kernel_half):
                best_offset = 0
                prev_ssd = 65534
                
                for offset in range(self.disparityRange):               
                    ssd = 0
                    ssd_temp = 0                            
                    
                    # v and u are the x,y of our local window search, used to ensure a good 
                    # match- going by the squared differences of two pixels alone is insufficient, 
                    # we want to go by the squared differences of the neighbouring pixels too
                    for v in range(-kernel_half, kernel_half):
                        for u in range(-kernel_half, kernel_half):
                            # iteratively sum the sum of squared differences value for this block
                            # left[] and right[] are arrays of uint8, so converting them to int saves
                            # potential overflow, and executes a lot faster   
                            ssd += self.cal_error(tp,int(self.left[y+v, x+u]),int(self.right[y+v, (x+u) - offset]))
                    
                    # if this value is smaller than the previous ssd at this block
                    # then it's theoretically a closer match. Store this value against
                    # this block..
                    if ssd < prev_ssd:
                        prev_ssd = ssd
                        best_offset = offset
                                
                # set depth output for this x,y location to the best match
                depth[y, x] = best_offset * offset_adjust
        print()
        return depth

    def cal_error(self,tp,lf,rt):
        if tp == 1:
            return (lf - rt) * (lf - rt)
        return abs(lf - rt)