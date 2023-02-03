### How to Run
To run these scripts, you need:
- Both a grayscale and a colored image to analyze in tandem
- ImageJ (or Fiji)
- Python installed on your computer
- Upgrade Python package manager to the latest version:
-- python3 -m pip install --upgrade pip
- To have installed a few python libraries:
-- `pip install opencv-python`
-- `pip install tkinter`
-- `pip install Pillow`
-- Any other libraries that you need to install that are included as import statements at the top of either `setup.py` or `macro.py`, you should run a `pip install <library-name>` command

Here is the order of operations for running these scripts:
0a) ONLY IF YOU DONT NEED THE FILES IN THE OUTPUT DIRECTORY, perform `python reset.py`. We need to have a fresh directory so that we can produce a new dataset.
0b) Look in `setup.py` and `macro.py` by using a text editor. There is one in ImageJ, but you can also use other text editors (most commonly Visual Studio Code). You will want to change paths to file names here. If you want `setup.py` to run through multiple images, you are going to have to change the `all_images` array in `setup.py` (note that this array only contains colored images, whereas macro.py will be going through the respective grayscale images).  
1) Run `setup.py` by running `python setup.py` in your terminal once you have gotten into the correct directory (in this case, the DyneinProtein directory)
2) Once `setup.py` is up and running, a window is going to pop up. This window has two images side by side with each other: on one side, we have the image with the marker(s) attached, and on the other side, we have the same portion of the original image. Both of these images, side by side, are zoomed in. The user here will need to press "Yes" or "No" to indicate whether this marker has been pinned correctly to a spot on the original image. If "Yes" is pressed, that data point will be kept; otherwise, the data point will be removed. After the user responds, another set will be shown, and this process repeats until all images put in the `all_images` array are analyzed. 
3) When the `setup.py` script is finished, we are going to have a number of files written to the `output` directory. In here, we will have a bunch of output images and CSV files. In the images, we have the colored images with the new markers on them. In the CSV files, we have all of the coordinates of the markers put onto the images.
4) Open ImageJ. Click on Plugins > Macros > Edit > ... and then pick the macro.py script. Once this script is open, assuming that all of the paths are correct, you should be able to run script by pressing the run button in the ImageJ macro text editor. After this script has successfully finished, you will now have all of the intensity data written to each of the CSV files in the `output` directory. Note that when the script finishes, there isn't a message currently to indicate that it has finished, so pay attention to the ImageJ terminal area.

### Information
This is still a WIP! I will be adding tutorial videos soon and will be hopefully updating this to look better.

### TODO List:
- Create tutorial videos on how to prepare to run the scripts, running the scripts, and miscellaneous information
- Adding an interface where the user can decide on what colors are being thresholded, how big the area has to be, threshold values, etc. Here, every time an option is changed, all marked spots would be previewed in a window
- Adding an option for # of spots to be found nearby a primary spot (in this case, the dynein protein)
- Housekeeping: More comments, modularizing more, reordering, possibly combining both scripts at some point down the road

