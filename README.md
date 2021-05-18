# Assignment 3: Edge Detection

### Description of task: Finding text using edge detection <br>
This assignment was assigned by the course instructor as “Assignment 3 – Edge Detection”. The purpose of the assignment was to use the tools and methods introduced during class to identify and draw contours around the letters in an image of an excerpt from the Declaration of Independence engraved on the interior wall of the Jefferson Memorial in Washington D.C. This task included first drawing a green rectangular box around the region of interest (ROI) which for this particular image was the body of text in the middle of the image. Then the task was to crop the original image to create a new image containing only the region of interest (ROI). Using Canny edge detection, the task was then to identify and draw green contours around every letter in the image. Thus, the purpose of this assignment was to use the image processing methods we had been introduced to during class to identify specific features, i.e., letters, in a specified image. 
In addition to the compulsory requirements of the task, I chose to experiment with making the script more generalizable with regard to how the edge detection thresholds are estimated and implement optical character recognition (OCR) to the pipeline. 


### Content and Repository Structure <br>

The repository follows the overall structure presented below. The python ```edgedetection.py``` script is located in the ```src``` folder. The image on which the edge detection has been performed is provided in the data folder, and the outputs produced when running the script can be found within the ```output``` folder. In the ```utils``` folder a utility script for OCR is stored. The README file contains a detailed run-through of how to engage with the code and reproduce the contents.

| Folder | Description|
|--------|:-----------|
| ```data``` | A folder containing the data for the particular assignment.
| ```src``` | A folder containing the python script(s) for the particular assignment.
| ```output``` | A folder containing the outputs produced when running the python script(s) within the src folder.
| ```utils``` | A folder containing utility scripts that store functions that are used within the main python script.
| ```requirements.txt```| A file containing the dependencies necessary to run the python script.
| ```create_edgedetection_venv.sh```| A bash-file that creates a virtual environment in which the necessary dependencies listed in the requirements.txt are installed. This script should be run from the command line.
| ```LICENSE``` | A file declaring the license type of the repository.


### Usage and Technicalities <br>
If the user wishes to engage with the code and reproduce the obtained results, this section includes the necessary instructions to do so. It is important to remark that all the code that has been produced has only been tested in Linux and MacOS. Hence, for the sake of convenience, I recommend using a similar environment to avoid potential problems. <br>

To reproduce the results of this assignment, the user will have to create their own version of the repository by cloning it from GitHub. This is done by executing the following from the command line: 

```
$ git clone https://github.com/sofieditmer/edgedetection.git 
```

Once the user has cloned the repository, a virtual environment must be set up in which the relevant dependencies can be installed. To set up the virtual environment and install the relevant dependencies, a bash-script is provided, which creates a virtual environment and installs the dependencies listed in the ```requirements.txt``` file when executed. To run the bash-script that sets up the virtual environment and installs the relevant dependencies, the user must first navigate to the edgedetection repository. 

```
$ cd edgedetection
$ bash create_edgedetection_venv.sh 
```

Once the virtual environment has been set up and the relevant dependencies listed in the ```requirements.txt``` have been installed within it, the user is now able to run the ```edgedetection.py``` script provided in the ```src``` folder directly from the command line. In order to run the script, the user must first activate the virtual environment in which the script can be run. Activating the virtual environment is done as follows.

```
$ source edgedetection_venv/bin/activate
```

Once the virtual environment has been activated, the user is now able to run the ```edgedetection.py``` script within it. When running the script, the user needs to specify the coordinates of the region of interest within the image. An example has been provided below. These coordinates correspond to the region of interest on the Jefferson Memorial image provided in the data folder. The user has the option of specifying additional arguments, however, this is not required to run the script.
```
(edgedetection_venv) $ cd src
(edgedetection_venv) $ python edgedetection.py –-ROI_coordinates 1400 880 2900 2800 --OCR "True"
```

The user is able to modify the following parameters, however, as mentioned this is not compulsory:
```
-i, --input_image, str <name-of-image-file>, default = "jefferson_memorial.jpeg"
-o, --output_dir, str <output-directory>, default = "output"
-s, --sigma, int <value-of-sigma>, default = 0.33
-oc, --ocr, str <perform-ocr-true-or-false>, default = "False"
```
The abovementioned parameters allow the user to adjust the analysis of the input image, if necessary, but default parameters have been set making the script run without explicitly specifying these arguments.  

Example: <br>
```
$ python edgedetection.py –-ROI_coordinates 1400 880 2900 2800 --OCR "True"
```

### Output <br>
When running the edge_detection.py script you will get four outputs saved in the specified output directory:
1. ```image_with_ROI.jpg```: the input image with the region of interest (ROI) drawn on top of it.
2. ```image_cropped.jpg```: the input image cropped to only contain the region of interest (ROI).
3. ```image_letters.jpg```: the cropped input image with the detected letters outlined in green.
4. ```image_OCR_text.txt```: the extracted text from the image using pytesseract OCR.


### License <br>
This project is licensed under the MIT License - see the [LICENSE](https://github.com/sofieditmer/edgedetection/blob/main/LICENSE) file for details.

### Contact details <br>
If you have any questions feel free to contact me on [201805308@post.au.dk](201805308@post.au.dk)

