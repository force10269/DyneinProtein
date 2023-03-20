### Dynein Protein Analysis
![Dynein protein application modal](https://raw.githubusercontent.com/force10269/DyneinProtein/master/assets/README_1.png)
![Dynein protein markers](https://raw.githubusercontent.com/force10269/DyneinProtein/master/assets/README_2.png)

### How to Run
To run these scripts, you need:
- Both a grayscale and a colored image to analyze in tandem
- ImageJ (or Fiji)
- Python installed on your computer
- Upgrade Python package manager to the latest version:
    - python3 -m pip install --upgrade pip
- To have installed a few python libraries:
    - `pip install opencv-python`
    - `pip install tkinter`
    - `pip install pillow`
    - `pip install python-dotenv`
    - `pip install ast`
    - `pip install numpy`
    - `pip install csv`
    - `pip install multiprocessing`
    - Any other libraries that you need to install that are included as import statements at the top of either `setup.py` or `macro.py`, you should run a `pip install <library-name>` command

Here is the order of operations for running these scripts:

0. ONLY IF YOU DONT NEED THE FILES IN THE OUTPUT DIRECTORY, perform `python reset.py`. We need to have a fresh directory so that we can produce a new dataset.

1. You will notice that there is a .env.sample file in the directory. This is a crucial folder! First, perform `copy .env.sample .env` if you are on Windows, or `cp .env.sample .env` if you are on Mac. This will copy the file with all of the path variables in it. Now, you can go into .env, and replace all of the paths with the ones on your computer in the format that they currently are in. If you are wondering why we do this, it is because we don't want our paths or any sensitive information on our computers to be published to GitHub. .env.sample shows a template for how to put your paths in, and then you put your actual paths in .env, where they will never reach GitHub because of our .gitignore file. After you have set this file up, you will then go to macro.py and change just the `csv_w_paths` variable to get an absolute path all the way to the paths.csv file which will be produced by `setup.py`. Unfortunately, ImageJ does not work well with dotenv (the library supporting the .env file), so we have to change just this one path here. Paths from .env will be written to paths.csv in the output directory after `setup.py` runs, so all the proper paths can be read in by `macro.py`. Lots of information, I know, but look to the tutorials video folder for more info on this! 

2. Run `setup.py` by running `python setup.py` in your terminal once you have gotten into the correct directory (in this case, the DyneinProtein directory)

3. Once `setup.py` is up and running, a window is going to pop up. This window has two images side by side with each other: on one side, we have the image with the marker(s) attached, and on the other side, we have the same portion of the original image. Both of these images, side by side, are zoomed in. The user here will need to press "Yes" or "No" to indicate whether this marker has been pinned correctly to a spot on the original image. If "Yes" is pressed, that data point will be kept; otherwise, the data point will be removed. After the user responds, another set will be shown, and this process repeats until all images put in the `all_images` array are analyzed. 

4. When the `setup.py` script is finished, we are going to have a number of files written to the `output` directory. In here, we will have a bunch of output images and CSV files. In the images, we have the colored images with the new markers on them. In the CSV files, we have all of the coordinates of the markers put onto the images.

5. Open ImageJ. Click on Plugins > Macros > Edit > ... and then pick the macro.py script. Once this script is open, assuming that all of the paths are correct, you should be able to run script by pressing the run button in the ImageJ macro text editor. After this script has successfully finished, you will now have all of the intensity data written to each of the CSV files in the `output` directory. Note that when the script finishes, there isn't a message currently to indicate that it has finished, so pay attention to the ImageJ terminal area.

### Information
This is still a WIP! I will be adding tutorial videos soon and will be hopefully updating this to look better.

### TODO List:
- Create tutorial videos on how to prepare to run the scripts, running the scripts, and miscellaneous information
- Adding an interface where the user can decide on what colors are being thresholded, how big the area has to be, threshold values, etc. Here, every time an option is changed, all marked spots would be previewed in a window
- Adding an option for # of spots to be found nearby a primary spot (in this case, the dynein protein)
- Housekeeping: More comments, modularizing more, reordering, possibly combining both scripts at some point down the road
- Add a system image finder, where images are automatically detected in the input directory and added to the scripts
- Confidence interval to show % of how sure the program is that a spot is correct? If the difference between red and green is big, then we might be more confident
- Express server, call endpoint that endpoint runs the python script to transition to a website
- Host a website with React and Express which will be hosting the application and running the python scripts in the backend. Might be difficult with running the script in ImageJ (macro.py)?
