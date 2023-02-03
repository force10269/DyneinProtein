from ij import IJ
from ij.measure import ResultsTable
import csv

# Read in the values of paths from paths.csv
# Unfortunately we have to change this too
csv_w_paths = '/Users/korrytunnicliff/Desktop/DyneinProtein/output/paths.csv'

with open(csv_w_paths, 'r') as csvfile:
	reader = csv.reader(csvfile)
	input_path, output_path = next(reader)
	grey_files = next(reader)

grey_paths = [input_path + f for f in grey_files]
csv_ctr = 0

for grey in grey_paths:
    # Open the greyscale image
    IJ.open(grey)

    csv_path = output_path + "output" + str(csv_ctr) + ".csv"

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