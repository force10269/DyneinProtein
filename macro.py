from ij import IJ
from ij.measure import ResultsTable
import csv

# These have to be absolute paths
grey_paths = [
    "/Users/korrytunnicliff/Desktop/DyneinProtein/input/subject_404_0_grey.tif",
    "/Users/korrytunnicliff/Desktop/DyneinProtein/input/subject_404_1_grey.tif",
    "/Users/korrytunnicliff/Desktop/DyneinProtein/input/subject_404_2_grey.tif",
    "/Users/korrytunnicliff/Desktop/DyneinProtein/input/subject_404_3_grey.tif",
]

csv_ctr = 0

for grey in grey_paths:
    # Open the greyscale image
    IJ.open(grey)

    csv_path = "/Users/korrytunnicliff/Desktop/DyneinProtein/output/output" + str(csv_ctr) + ".csv"

    green_intensities = []
    red_intensities = []

    # First read all the data
    with open(csv_path, 'r') as csvfile:
        coordinates = csv.reader(csvfile)
        data = [row for row in coordinates]

    # Now perform all measurements
    with open(csv_path, 'r') as csvfile:
        coordinates = csv.reader(csvfile)
        
        # Skip the first line since it's just headers
        next(coordinates)

        rt = ResultsTable()
        ctr = 0

        # Loop over all of the coordinates
        for row in coordinates:
            red_x, red_y, green_x, green_y = int(row[0]), int(row[1]), int(row[2]), int(row[3])

            # Set the measurements to the red coordinate
            IJ.makeRectangle(red_x, red_y, 3, 3)
            IJ.run("Measure")
            rt = ResultsTable.getResultsTable()
            red_intensities.append(rt.getValue("Mean", ctr))
            ctr += 1

            # Set the measurements to the green coordinate
            IJ.makeRectangle(green_x, green_y, 3, 3)
            IJ.run("Measure")
            green_intensities.append(rt.getValue("Mean", ctr))
            ctr += 1

        # Append the data to the csv with the corresponding coordinates
        with open(csv_path, 'w') as outputfile:
            writer = csv.writer(outputfile)
            writer.writerow(data[0])
            for i in range(0, len(green_intensities)):
                data[i+1] = data[i+1] + [red_intensities[i], green_intensities[i]]
                writer.writerow(data[i+1])

        csv_ctr += 1
        IJ.run("Close")