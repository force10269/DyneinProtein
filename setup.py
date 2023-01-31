# Make sure that before you run this script, you delete any previous output.jpg or output.csv
# The output.csv file will become larger than you want it to be if you run this script multiple times in a row

import cv2
import os
import numpy as np
import csv

csv_path = 'output.csv' # This can just be relative, meaning it's just going to be in the same folder
image_path = 'color.tif' # Same as above

# These are all variables you can shift around for different images
# You aren't going to get all of the dynein proteins perfectly, but
# with the current settings, you can get most of them accurately
threshold1 = 125
threshold2 = 255
pixelBoxWidth = 2
pixelBoxHeight = 2

# When we're picking spots that are dynein proteins, we want to make sure we're not
# picking a spot that is particularly bright. These values don't follow the same values as
# RGB 0 < x < 255, they are usually lower
filteringGreen = 17
filteringRed = 10

# This is for getting a point nearby in the cell to measure against the dynein protein
minimum_green_intensity = 65

header = ['x_dynein', 'y_dynein', 'x_cell', 'y_cell', 'Dynein Intensity', 'Cell Intensity']

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

cv2.imshow('Red Image', red_component)

# Find the contours in the binary image
contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create a copy of the colored image to display the arrows and lines
output_image = color_image.copy()

# Store the red center positions
red_positions = []

# Store the green positions
green_positions = []

# Loop through the contours
for contour in contours:
    # Get the minimum bounding rectangle for the contour
    x, y, w, h = cv2.boundingRect(contour)
    if w >= pixelBoxWidth and h >= pixelBoxHeight and (green_component[x,y] > filteringGreen or red_component[x,y] > filteringRed):
        # Calculate the center of the bounding rectangle
        center_x = x + w // 2
        center_y = y + h // 2

        # Append the red center position to the red_positions list
        red_positions.append((center_x, center_y))

        # Find the nearby green position
        for i in range(center_x-10, center_x+10):
            for j in range(center_y-10, center_y+10):
                if i >= 0 and i < color_image.shape[1] and j >= 0 and j < color_image.shape[0]:
                    if color_image[j, i, 1] > color_image[j, i, 0] and color_image[j, i, 1] > color_image[j, i, 2] and color_image[j, i, 1] > minimum_green_intensity:
                        green_position = (i, j)
                        green_positions.append(green_position)
                        break
            else:
                continue
            break

        # Draw a yellow line between the red position and the green position
        cv2.line(output_image, (center_x, center_y), green_position, (0, 255, 255), 1)

        # Draw an arrow on the output image pointing to the center
        cv2.arrowedLine(output_image, (center_x, center_y), (center_x, center_y), (0, 0, 255), 5)

        for green_position in green_positions:
            # Draw a pink star on the output image for each green position
            cv2.drawMarker(output_image, green_position, (0, 255, 0), cv2.MARKER_STAR, markerSize=3, thickness=2, line_type=cv2.LINE_AA)

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
cv2.imwrite('output.jpg', output_image)
