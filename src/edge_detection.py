#!/usr/bin/env python
"""
Info: This script loads an image, draws a region of interest (ROI) on the image based on the coordinates given, crops the image to only contain the ROI, applies canny edge detection on the image, draws contours around detected letters (edges), and saves output to output directory. 

Parameters:
    (optional) input_image: str <name-of-image-file>, default = "jefferson_memorial.jpeg"
    (required) ROI_coordinates: int <x1 y1 x2 y2>
    (optional) output: str <output-directory>, default = "output"
    (optional) sigma_value: int <value-of-sigma>, default = 0.33
    (optional) OCR: str <perform-ocr-true-or-false>, default = "False"
    
Example:
    $ python edge_detection.py --ROI_coordinates 1400 880 2900 2800 --OCR "True"

Output:
    - image_with_ROI.jpg: the input image with the region of interest (ROI) drawn on top of it.
    - image_cropped.jpg: the input image cropped to only contain the region of interest (ROI).
    - image_letters.jpg: the cropped input image with the detected letters outlined in green.
    - image_OCR_text.txt: the extracted text from the image using pytesseract OCR.
"""

### DEPENDENCIES ###

# core libraries
import os
import sys
sys.path.append(os.path.join(".."))

# OCR utility function
import utils.OCR_utils as ocr

# OpenCV and numpy
import cv2
import numpy as np

# argparse
import argparse

# pytesseract for OCR
import pytesseract

### MAIN FUNCTION ###

def main():
    
    ### ARGPARSE ###
    
    # Initialise ArgumentParser class
    ap = argparse.ArgumentParser()
    
    # Argument 1: Input image
    ap.add_argument("-i", "--input_image", 
                    type = str,
                    required = False, # the argument is not required 
                    help = "Name of input image",
                    default = "jefferson_memorial.jpeg") # default image
    
    # Argument 2: Coordinates of regions of interest (ROI)
    ap.add_argument("-r", "--ROI_coordinates", 
                    required = True, # the argument is required. 
                    help = "Define the coordinates of the region of interest (ROI)", nargs='+')
    
    # Argument 3: Output directory
    ap.add_argument("-o", "--output_dir", 
                    type = str,
                    required = False, # the argument is not required
                    help = "Define output directory",
                    default = "output") # default name of output directory
    
    # Argument 5: Sigma value
    ap.add_argument("-s", "--sigma", 
                    type = float,
                    required = False, # the argument is not required
                    help = "Define the sigma value used for thresholding. A large sigma value will result in tighter thresholds for edge detection, while a small sigma value will result in wider thresholds for edge detection.",
                    default = 0.33) # default sigma value
    
    # Argument 6: OCR
    ap.add_argument("-oc", "--OCR", 
                    type = str,
                    required = False, # the argument is not required
                    help = "True/False. Indicates whether you want to perform OCR.",
                    default = "False") # default; OCR will not be performed
                    
    # Parse arguments
    args = vars(ap.parse_args())

    # Save input parameters
    input_image = args["input_image"]
    ROI_coordinates = args["ROI_coordinates"]
    output_dir = args["output_dir"]
    sigma_value = args["sigma"]
    OCR = args["OCR"]
    
    # Create output directory if it does not exist already
    if not os.path.exists(os.path.join("..", output_dir)):
        os.mkdir(os.path.join("..", output_dir))
        
    # Instantiating the EdgeDetection class
    print("\n[INFO] Initiating edge detection...")
    edgedetection = EdgeDetection(input_image, output_dir)
    
    # Draw region of interest, ROI, on the image 
    print("\n[INFO] Drawing region of interest (ROI) on the image based on input coordinates...")
    top_left, bottom_right, image = edgedetection.draw_ROI(ROI_coordinates)
    
    # Crop image to only include ROI
    print("\n[INFO] Cropping image to only include the region of interest (ROI)...")
    image_cropped = edgedetection.crop_image(image, top_left, bottom_right)
    
    # Convert image to greyscale and peform Gaussian blurring
    print("\n[INFO] Converting the cropped image to greyscale and performing Gaussian blurring...")
    greyscale_image, blurred_image = edgedetection.greyscale_and_blur(image_cropped)
    
    # Finding lower and upper thresholds for canny edge detection
    print("\n[INFO] Estimating upper and lower threshold for canny edge detection...")
    lower_threshold, upper_threshold = edgedetection.find_thresholds(image, sigma_value)
    
    # Perform canny edge detection
    print(f"\n[INFO] Performing canny edge detection with a lower threshold of {lower_threshold} and an upper threshold of {upper_threshold}...")
    edged_image = edgedetection.perform_canny_edge_detection(blurred_image, lower_threshold, upper_threshold, greyscale_image)
    
    # Draw countours around edges (letters)
    print(f"\n[INFO] Finding edges and drawing countours around them...")
    edgedetection.draw_contours(edged_image, image_cropped)
    
    # Perform OCR if the user has chosen to through the command line
    edgedetection.perform_OCR(OCR, greyscale_image, lower_threshold, upper_threshold)
    
    # Message to user
    print(f"\n[INFO] Done! {input_image}_with_ROI.jpg, {input_image}_cropped.jpg, and {input_image}_letters.jpg have now been saved in {output_dir}.\n")
    
    
# Creating EdgeDetection class
class EdgeDetection:
    
    # Initialize class
    def __init__(self, input_image, output_dir):
        
        # Receiving input parameters
        self.input_image = input_image
        self.output_dir = output_dir
        
    def draw_ROI(self, ROI_coordinates):
        """
        This method draws the regions of interest (ROI) on the input image based on the coordinates provided by the user or the default coordinates. 
        """
        # Load image
        image = cv2.imread(os.path.join("..", "data", self.input_image))
        
        # Define top left point of ROI
        top_left = (int(ROI_coordinates[0]), int(ROI_coordinates[1]))
    
        # Define bottom right point of ROI
        bottom_right = (int(ROI_coordinates[2]), int(ROI_coordinates[3]))
   
        # Draw green ROI rectangle on copy of image
        ROI_image = cv2.rectangle(image.copy(), top_left, bottom_right, (0, 255, 0), (2)) # (0, 255, 0) = green following the BGR color model
    
        # Save image with ROI drawn on it
        cv2.imwrite(os.path.join(self.output_dir, f"{self.input_image}_with_ROI.jpg"), ROI_image)
        
        return top_left, bottom_right, image
    

    def crop_image(self, image, top_left, bottom_right):
        """
        This method crops the image to only contain the region of interest (ROI). 
        """
        # Crop image to include ROI using slicing. The first entry is the length and the second entry is the height.
        image_cropped = image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    
        # Save the cropped image
        cv2.imwrite(os.path.join(self.output_dir, f"{self.input_image}_cropped.jpg"), image_cropped)
    
        return image_cropped


    def greyscale_and_blur(self, image_cropped):
        """
        This method converts the cropped image into a greyscale image and performs Gaussian blurring.
        """
        # Convert the cropped image to greyscale
        greyscale_image = cv2.cvtColor(image_cropped, cv2.COLOR_BGR2GRAY)
    
        # Perform Gaussian blurring
        blurred_image = cv2.GaussianBlur(greyscale_image, (3,3), 0) # I use a 3x3 kernel to perform the blurring
        # 0 indicates the amount of variation from the mean that we take into account (i.e. standard deviation). The higher the standard deviation, the more variation, and therefore the more blurring. I use 0 to not get too much blurring (distortion) in the image. 
        return greyscale_image, blurred_image


    def find_thresholds(self, blurred_image, sigma_value):
        """
        This method automatically finds the upper and lower thresholds to be used when performing canny edge detection. This method was highly inspired by this article: https://www.pyimagesearch.com/2015/04/06/zero-parameter-automatic-canny-edge-detection-with-python-and-opencv/. The sigma value can be varied, but this article found that 0.33 tends to give good results. A lower value of sigma gives a *tighter* threshold, while a larger sigma gives a *wider* threshold.
        """
        # Compute the median of the single channel pixel intensities
        v = np.median(blurred_image)
    
        # Compute lower threshold
        lower_threshold = int(max(0, (1.0 - sigma_value) * v))
    
        # Compute upper threshold 
        upper_threshold = int(min(255, (1.0 + sigma_value) * v))
    
        return lower_threshold, upper_threshold
    

    def perform_canny_edge_detection(self, blurred_image, lower_threshold, upper_threshold, greyscale_image):
        """
        This method performs Canny edge detection on the blurred image.
        """
        # Perform canny edge detection on the blurred image using the lower and upper threshold
        edged_image = cv2.Canny(blurred_image,
                                lower_threshold,
                                upper_threshold)
            
        return edged_image
            

    def draw_contours(self, edged_image, image_cropped):
        """
        This method finds the edges (i.e. letters) and draws green countours around them.
        """    
        # Find contours. Since we are only intersted in the list of contours we use a dummy variable for the second thing that is also returned (hierarchy)
        (contours, _) = cv2.findContours(edged_image.copy(), # using a copy of the image
                                         cv2.RETR_EXTERNAL, # contour retrieval mode. RETR_EXTERNAL has to do with how contours are structured hierarchically. It performs a hierarchical structuring, which means that internal structures are filtered out leaving only external contours. Hence, if there are contours inside the object we filter those out, and only focus on the contours that surrounds the object itself. 
                                         cv2.CHAIN_APPROX_SIMPLE) # contours approximation method. This method only saves the most important boundary points of the contours rather than all of them in order to save memory. 
    
        # Draw green contours around the letters on the cropped image
        image_letters = cv2.drawContours(image_cropped.copy(), # using a copy of the image
                                         contours, # list of contours
                                         -1, # draw all contours
                                         (0,255,0), # green following the BGR-color model of openCV
                                         2) # thickness of contours
    
        # Save cropped image with contours
        cv2.imwrite(os.path.join(self.output_dir, f"{self.input_image}_letters.jpg"), image_letters)
        

    def perform_OCR(self, OCR, greyscale_image, lower_treshold, upper_threshold):
        """
        This method performs object-character recognition (OCR) using Pytesseract and saves the text in a txt-file to the output directory. 
        """
        # If the user has chosen to perform OCR
        if OCR == "True":
            # Since pytesseract expects black text on a white background, I perform binarization thresholding on the image
            (T, edged_image) = cv2.threshold(greyscale_image,
                                             110, # threshold value used to classify the pixel values
                                             255, # maximum pixel value assigned to values above 110
                                             cv2.THRESH_BINARY) # binary thresholding - everything above 110 in pixel intensity will be set to white (255)
            
            # Below I am tweaking tesseract parameters. I use a combination of the original tesseract model and the neural network approach, which is indicated by --oem 2, and I tell it to "assume a single column of text of variable sizes", which is indicated by --psm 4
            custom_oem_psm_config = r'--oem 2 --psm 4'
        
            # Perform the OCR on the edged image
            text_string = pytesseract.image_to_string(edged_image)
        
            # Perform some manual cleanup of the text 
            processed_text_string = ocr.replace(text_string)
        
            # Save text as txt-file to output directory
            with open(os.path.join("..", self.output_dir, f"{self.input_image}_OCR_text.txt"), "w") as f:
                      f.write(f"Below you can see the result of the OCR run on {self.input_image}:\n \n {processed_text_string}")
        
            # User message
            print(f"\n[INFO] OCR is done! {self.input_image}_OCR_text.txt has been saved in {self.output_dir}.")       
            
        # If the user has not specified that they want to perform OCR on the input image
        if OCR == "False":
            return None
                      

# Define behaviour when called from command line
if __name__=="__main__":
    main()