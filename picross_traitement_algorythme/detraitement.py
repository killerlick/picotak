import cv2 as cv
import sys
import os
import json
import numpy as np


def print_usage():
    print("Usage: python detraitement.py <input_json> [picross_size]")
    print("  <input_json>: Path to the input json file.")
    print("  [image_size]: Optional size of the image to display(default is 500).")

def validate_arguments(args):
    if len(args) < 2:
        print("Error: Missing input json file.")
        print_usage()
        sys.exit(1)
    
    input_path = args[1]

    if not os.path.isfile(input_path):
        print(f"Error: The file '{input_path}' does not exist.")
        sys.exit(1)
    
    if len(args) > 2:
        try:
            image_size = int(args[2])
            if image_size <= 0:
                raise ValueError
        except ValueError:
            print("Error: Image size must be a positive integer.")
            sys.exit(1)
    else:
        image_size = 500    
    return input_path, image_size

if __name__ == "__main__":
    input_path , image_size = validate_arguments(sys.argv)

    with open(input_path, 'r') as jsonFile:
        json_data = json.load(jsonFile)
    grid = json_data['grid']
    size = json_data['size']  

    image = np.array(grid , dtype=np.uint8) * 255
    image = cv.bitwise_not(image)
    
    if image is None:
        print("Could not create the image.")
        sys.exit(1)

    image = cv.resize(image , (image_size,image_size) , interpolation = cv.INTER_NEAREST)

    cv.imshow('output', image)
    cv.waitKey(0)
