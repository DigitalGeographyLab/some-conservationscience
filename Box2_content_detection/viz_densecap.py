import argparse
import os
import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches

# Set up argument parser
ap = argparse.ArgumentParser()

# Define arguments
ap.add_argument("-i", "--images", required=True,
                help="Path to the directory with images.")
ap.add_argument("-j", "--json", required=True,
                help="Path to the JSON file containing the results.")
ap.add_argument("-b", "--boxes", required=True, default=5, type=int,
                help="Number of boxes to draw.")

# Parse arguments
args = vars(ap.parse_args())

# Get a qualitative colourmap from matplotlib
colours = matplotlib.cm.Set1.colors

# Define a font dictionary for labels
fontdict = {'family': 'sans-serif',
            'color': 'white',
            'weight': 'normal',
            'size': 8,
            }

# Open the file containing DenseCap results
with open(args['json']) as res_json:

    # Load data and assign into variable
    data = json.load(res_json)

# Loop over the results
for i in data['results']:

    # Fetch filename, captions and bounding boxes
    filename = i['img_name']
    captions = i['captions'][:args['boxes']]
    boxes = i['boxes'][:args['boxes']]

    # Zip captions and boxes; cast into list
    capboxes = list(zip(captions, boxes))

    # Load image using matplotlib
    try:
        image = mpimg.imread(os.path.join(args['images'], filename))

    except FileNotFoundError:
        continue

    # Create a figure
    fig, ax = plt.subplots(1)

    # Hide grid & axes
    plt.axis('off')
    plt.tight_layout(pad=1)

    # Add the image on the axis
    plot = ax.imshow(image)

    # Loop over the region descriptions
    for x in range(0, args['boxes']):

        # Round the coordinates
        coords = [round(x) for x in capboxes[x][1]]

        # Remove negative coordinates
        coords = [0 if x < 0 else x for x in coords]

        # Assign coordinates to variables
        startx, starty, width, height = coords[0], coords[1], coords[2], coords[3]

        # Add a rectangle patch
        rect = patches.Rectangle((startx, starty),
                                 width, height,
                                 fill=True,
                                 alpha=0.2,
                                 color=colours[x])

        # Put the description text
        desc = capboxes[x][0]

        # Add the text to the image
        text = ax.text(startx + 12, np.random.uniform(starty, starty+height),
                       desc,
                       fontdict=fontdict,
                       bbox=dict(facecolor=colours[x],
                                 alpha=0.4)
                       )

        # Add the rectangle to the visualization
        ax.add_patch(rect)

    # Save the plot
    plt.savefig("{}_boxes.png".format(filename), dpi=300)
