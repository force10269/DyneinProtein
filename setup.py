import tkinter as tk
from PIL import Image, ImageTk
import time
import os
import cv2
import numpy as np
import csv

import multiprocessing

# Global variable
# Important so that every time we get a user response,
# we can update here since the app will close itself
# down every time
result = None

# Paths for all images
all_images = ['input/subject_404_0_color.tif', 'input/subject_404_1_color.tif', 'input/subject_404_2_color.tif', 'input/subject_404_3_color.tif']
ctr = 0

# Current spot output image path
spot_image_path = 'output/current_spot.jpg'

# These are all variables you can shift around for different images
# You aren't going to get all of the dynein proteins perfectly, but
# with the current settings, you can get most of them accurately

threshold1 = 125
threshold2 = 255
pixelBoxWidth = 2
pixelBoxHeight = 2

if input("Do you want to change the default search values for red spots? (y/n): ") == "y":
    threshold1 = int(input("What do you want the lower threshold to be? (default is 125) (values between 0-255): "))
    threshold2 = int(input("What do you want the higher threshold to be? (default is 255) (values between 0-255): "))
    pixelBoxWidth = int(input("What do you want the pixel box width to be? (default is 2): "))
    pixelBoxHeight = int(input("What do you want the pixel box height to be? (default is 2): "))

filteringGreen = 7

# These are for getting a point nearby in the cell to measure against the dynein protein
minimum_green_intensity = 65
maximum_green_intensity = 100
greenSearchRange = 10

if input("Do you want to change the default search values for green spots? (y/n): ") == "y":
    minimum_green_intensity = int(input("What do you want the minimum intensity of green spots to be? (default is 65) (values between 0-255): "))
    maximum_green_intensity = int(input("What do you want the maximum intensity of green spots to be? (default is 100) (values between 0-255): "))
    greenSearchRange = int(input("What do you want the search range for green spots to be from the red spots? (default is 10 pixels): "))



class App:
    def __init__(self, master=tk.Tk()):
        self.master = master
        self.fig_size = [800, 600]
        self.frame = tk.Frame(master, bg='lightgrey')
        self.canvas = tk.Canvas(self.frame, width=1280, height=800)
        self.canvas.pack()
                    
        self.image_label = tk.Label(self.canvas)
        self.image_label.pack(padx=10, pady=10)

        # Create the question label
        self.question_label = tk.Label(self.frame, text="Is this accurate?")
        self.question_label.pack(pady=10)

        self.button_frame = tk.Frame(self.frame, bg='lightgrey', pady=10)
        self.button_frame.pack()

        # Create the "Yes" button
        self.button_yes = tk.Button(self.button_frame, text="Yes", command=self.updateYes, height=2, font=("Helvetica", 20), width=10)
        self.button_yes.pack(side="left", padx=10)

        # Create the "No" button
        self.button_no = tk.Button(self.button_frame, text="No", command=self.updateNo, height=2, font=("Helvetica", 20), width=10)
        self.button_no.pack(side="left", padx=10)

        self.frame.bind("q", self.close)
        self.frame.bind("<Escape>", self.close)
        self.frame.pack()
        self.frame.focus_set()
        self.is_active = True

    def load_image(self, filename):
        self.fig_image = ImageTk.PhotoImage(Image.open(filename).resize(self.fig_size, Image.BILINEAR))
        self.image_label.config(image=self.fig_image)

    def updateYes(self, *args):
        global result
        result = 'y'
        self.master.withdraw()
        self.frame.pack_forget()
        self.frame.pack()
        self.master.update()
        self.master.deiconify()
        self.close()

    def updateNo(self, *args):
        global result 
        result = 'n'
        self.master.withdraw()
        self.frame.pack_forget()
        self.frame.pack()
        self.master.update()
        self.master.deiconify()
        self.close()

    def close(self, *args):
        self.master.quit()
        self.is_active = False

    def destroy_widgets(self):
        self.frame.destroy()
        self.canvas.destroy()
        self.image_label.destroy()
        self.question_label.destroy()
        self.button_yes.destroy()
        self.button_no.destroy()

    def is_closed(self):
        return not self.is_active

    def mainloop(self):
        self.master.mainloop()

def zoom_in(img, center, size):
    # Zooms into image and onto a specific region
    x, y = center
    h, w = img.shape[:2]
    xmin = max(0, x - size[0]//2)
    xmax = min(w, x + size[0]//2)
    ymin = max(0, y - size[1]//2)
    ymax = min(h, y + size[1]//2)
    return img[ymin:ymax, xmin:xmax]

def show_popup(img, red_spot, green_spot):
    # Function to display a popup with the zoomed-in image

    # This is the image with the markers
    zoomed_in_img = img.copy()

    # This is the comparison image
    side_img = img.copy()

    # Draw all the positions with the lines between them
    cv2.line(zoomed_in_img, red_spot, green_spot, (0, 255, 255), 1)
    cv2.arrowedLine(zoomed_in_img, red_spot, red_spot, (0, 0, 255), 2)
    cv2.drawMarker(zoomed_in_img, green_spot, (0, 255, 0), cv2.MARKER_STAR, markerSize=3, thickness=1, line_type=cv2.LINE_AA)

    zoomed_in_img = zoom_in(zoomed_in_img, red_spot, (200, 200))
    side_img = zoom_in(side_img, red_spot, (200,200))

    height = max(zoomed_in_img.shape[0], side_img.shape[0])
    combined_img = np.zeros((height, zoomed_in_img.shape[1]+side_img.shape[1]+5, 3), dtype=np.uint8)
    combined_img[:, :zoomed_in_img.shape[1]] = zoomed_in_img
    combined_img[:, zoomed_in_img.shape[1]+5:] = side_img

    # Add white bar
    combined_img[:, zoomed_in_img.shape[1]:zoomed_in_img.shape[1]+5] = 255

    return combined_img

# Input: img
# Process: Loop through possible, show confirmation popup
# Output: (red_positions, green_positions)
def process_image(contours, color_image):
    # This is the big function. Here, we look through all
    # the contours of the image, and the program then finds
    # all spots it considers to be valid dynein and cell spots.
    # On top of this, we also get confirmation from the user as to whether
    # the spot is accurate or not

    # Store the red center positions
    red_positions = []

    # Store the green positions
    green_positions = []

    # Loop through the contours
    for contour in contours:
        # Get the minimum bounding rectangle for the contour
        x, y, w, h = cv2.boundingRect(contour)
        if w >= pixelBoxWidth and h >= pixelBoxHeight and green_component[x,y] > filteringGreen:
            # Calculate the center of the bounding rectangle
            center_x = x + w // 2
            center_y = y + h // 2

            # Find the nearby green position
            for i in range(center_x-greenSearchRange, center_x+greenSearchRange):
                for j in range(center_y-greenSearchRange, center_y+greenSearchRange):
                    if i >= 0 and i < color_image.shape[1] and j >= 0 and j < color_image.shape[0]:
                        if color_image[j, i, 1] > minimum_green_intensity and color_image[j, i, 1] < maximum_green_intensity:
                            green_position = (i, j)
                            break
                else:
                    continue
                break

            # If we can't find a corresponding green position, go to the next contour
            if 'green_position' not in locals():
                continue

            # Here, get user input. If the user denies, go to next contour
            # In order to get this right, we have to create an individual App to show
            # the image popup along with an option for the user to either say "Yes" or "No" to a spot

            # Get combined image to load in app screen
            curr_img = show_popup(color_image, (center_x, center_y), green_position)
            cv2.imwrite(spot_image_path, curr_img)

            # Instantiate the app
            # The reason we have to reinstantiate it every time is because we need to come
            # out of the mainloop with the app and continue to work with the contours
            app = App()
            app.load_image(spot_image_path)
            app.mainloop()
            app.destroy_widgets()

            if result != 'y':
                continue

            # Append the red center position to the red_positions list
            red_positions.append((center_x, center_y)) 

            # Append the green center positions to the green_positions list
            green_positions.append(green_position)

            # Draw a yellow line between the red position and the green position
            cv2.line(output_image, (center_x, center_y), green_position, (0, 255, 255), 1)

            # Draw an arrow on the output image pointing to the center
            cv2.arrowedLine(output_image, (center_x, center_y), (center_x, center_y), (0, 0, 255), 5)

            # Draw a pink star on the output image for each green position
            cv2.drawMarker(output_image, green_position, (0, 255, 0), cv2.MARKER_STAR, markerSize=3, thickness=2, line_type=cv2.LINE_AA)

    return red_positions, green_positions

if __name__ == "__main__":
    header = ['x_dynein', 'y_dynein', 'x_cell', 'y_cell', 'Dynein Intensity', 'Cell Intensity']

    for image_path in all_images:
        csv_path = 'output/output' + str(ctr) + '.csv' # This can just be relative, meaning it's just going to be in the same folder
        if not os.path.exists(csv_path):
            with open(csv_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)

        # Load the colored image
        color_image = cv2.imread(image_path)

        # Extract the red component of the colored image
        red_component = color_image[:,:,2]
        green_component = color_image[:,:,1]

        # Threshold the red component to create a binary image
        _, binary_image = cv2.threshold(red_component, threshold1, threshold2, cv2.THRESH_BINARY)

        # Find the contours in the binary image
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Create a copy of the colored image to display the arrows and lines
        output_image = color_image.copy()

        red_positions, green_positions = process_image(contours, color_image)

        # Write the data to a CSV file
        with open(csv_path, 'a', newline='') as file:
            writer = csv.writer(file)
            for red_position, green_position in zip(red_positions, green_positions):
                xRed, yRed = red_position
                xGreen, yGreen = green_position
                writer.writerow([xRed, yRed, xGreen, yGreen])

        # Display the output image with arrows pointing to the centers and yellow lines connecting the red centers to green positions
        cv2.imshow('Output Image', output_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite('output/output' + str(ctr) + '.jpg', output_image)

        ctr += 1
        
