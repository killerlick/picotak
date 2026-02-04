import cv2 as cv
import sys
import os
import json


def print_usage():
    print("Usage: python traitement.py <input_image> [picross_size]")
    print("  <input_image>: Path to the input image file.")
    print("  [picross_size]: Optional size of the picross grid (default is 12).")

def validate_arguments(args):
    if len(args) < 2:
        print("Error: Missing input image.")
        print_usage()
        sys.exit(1)
    
    input_path = args[1]
    if not os.path.isfile(input_path):
        print(f"Error: The file '{input_path}' does not exist.")
        sys.exit(1)
    
    if len(args) > 2:
        try:
            picross_size = int(args[2])
            if picross_size <= 0:
                raise ValueError
        except ValueError:
            print("Error: Picross size must be a positive integer.")
            sys.exit(1)
    else:
        picross_size = 12
    
    return input_path, picross_size

def picrossed_image(image, size):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    _, gray = cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    pixelated = cv.resize(gray, (size, size), interpolation=cv.INTER_NEAREST)
    return pixelated

def pixelised_to_json(pixelised , size):
    json_data = {}
    json_data['size'] = size
    json_data['grid'] = []

    for i in range(size):
        row = []
        for j in range(size):
            row.append(int(pixelised[i][j]) == 0)
        json_data['grid'].append(row)
    
    return json_data

def file_to_result():
    pass

if __name__ == "__main__":
    input_path , picrossSize = validate_arguments(sys.argv)
    input_name = os.path.splitext(os.path.basename(input_path))[0]
    input_name = os.path.basename(input_name)

    img = cv.imread(input_path)

    if img is None:
        print("Could not read the image.")
        sys.exit(1)

    defaultH, defaultW = img.shape[:2]
    pixelised = picrossed_image(img, picrossSize)
    json_data = pixelised_to_json(pixelised, picrossSize) 

    os.makedirs(f"output/{input_name}", exist_ok=True) 

    with open(f'output/{input_name}/{input_name}.json', 'w') as jsonFile:
        json.dump(json_data, jsonFile, indent=4)

    output = cv.resize(pixelised , (defaultW,defaultH) , interpolation = cv.INTER_NEAREST)
    cv.imwrite(f'output/{input_name}/{input_name}.jpg', output)