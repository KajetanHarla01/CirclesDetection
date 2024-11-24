from os import listdir
import os
from os.path import isfile, join
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Function to choose an image from a specified directory
def get_image(dir):
    # List all files in the directory
    files = [f for f in listdir(dir) if isfile(join(dir, f))]
    
    # If the directory is empty, print an error and exit
    if len(files) == 0:
        print("Error: \"" + dir + "\" directory is empty")
        exit()
    
    # Display the list of files and prompt the user to choose one
    print("Choose file: ")
    counter = 1
    for f in files:
        print(str(counter) + " - " + str(f))  # Display file options
        counter += 1
    
    # Input the file number
    file_choose = int(input("File number: "))
    
    # If the input is invalid, exit
    if file_choose > len(files):
        print("Error: invalid file number")
        exit()
    
    # Return the full path to the chosen image file
    return dir + "/" + files[file_choose - 1]

# Function to smooth a contour by averaging points
def smooth_contour(contour, n):
    smoothed_contour = []
    contour_len = len(contour)
    
    # Iterate through the contour points to average them
    for i in range(contour_len):
        # Gather the n points around the current one, considering cyclicity
        points_to_avg = [contour[(i + j) % contour_len][0] for j in range(n)]
        
        # Calculate the average of these points
        avg_point = np.mean(points_to_avg, axis=0)
        
        # Append the averaged point to the smoothed contour list
        smoothed_contour.append(np.array([avg_point], dtype=np.int32))

    return np.array(smoothed_contour, dtype=np.int32)

# Function to resize an image while maintaining its aspect ratio
def normalize_image(image, target_width=800):
    (height, width) = image.shape[:2]
    
    # Calculate the aspect ratio
    aspect_ratio = width / height
    
    # Calculate the target height based on the new width
    target_height = int(target_width / aspect_ratio)
    
    # Resize the image to the target width and height
    resized_image = cv2.resize(image, (target_width, target_height))
    
    return resized_image, width / target_width  # Return the resized image and scale factor

# Function to scale a contour by a given scale factor
def scale_contour(contour, scale_factor):
    scaled_contour = contour * scale_factor  # Scale all points by the factor
    return scaled_contour.astype(np.int32)  # Return the scaled contour in integer type

# Function to detect circles in an image
def detect_circles(image_path):
    # Read the image and convert it to grayscale
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Resize the image while keeping the aspect ratio
    resized, scale = normalize_image(gray)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(resized, (5, 5), 0)

    # Detect edges using the Canny edge detector
    edges = cv2.Canny(blurred, 5, 50)

    # Apply dilation to enhance the edges
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (12, 12))
    dilated = cv2.dilate(edges, kernel, iterations=1)

    # Find contours in the dilated image
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Filter out only the internal contours (those with a parent)
    internal_contours = []
    for i, h in enumerate(hierarchy[0]):
        if h[3] != -1:  # Check if it has a parent
            internal_contours.append(contours[i])

    # Initialize an empty list for complete circles
    complete_circles = []

    # Process each contour
    for contour in internal_contours:
        contour = smooth_contour(contour, 50)  # Smooth the contour
        contour = scale_contour(contour, scale)  # Scale the contour
        if len(contour) > 2:
            # Calculate the area and perimeter of the contour
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            
            # Calculate the circularity of the contour (measure of how circular the shape is)
            circularity = 4 * np.pi * (area / (perimeter ** 2)) if perimeter > 0 else 0
            
            # If the circularity is close to 1, consider it a circle
            if 0.9 < circularity <= 1.1:
                complete_circles.append(contour)  # Add it to the list of circles

    # Create a copy of the original image to draw the circles on
    result_image = image.copy()
    cv2.drawContours(result_image, complete_circles, -1, (0, 0, 0), int(10*scale))  # Draw the contours

    return image, result_image, len(complete_circles)  # Return the original image, result image, and the number of circles found

# Function to display the original and result images side by side
def show_result(original, result, circle_count):
    fig, axes = plt.subplots(1, 2)  # Create a subplot with two columns

    # Display the original image on the first axis
    axes[0].imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    axes[0].set_title("Oryginal image")  # Set the title for the original image
    axes[0].axis("off")  # Turn off axis lines and labels

    # Display the result image (with detected circles) on the second axis
    axes[1].imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    axes[1].set_title(f"Detection result (circles: {circle_count})")  # Set the title with the number of circles
    axes[1].axis("off")  # Turn off axis lines and labels

    plt.tight_layout()  # Adjust the layout to prevent overlap
    plt.show()  # Display the plot

# Function to save the output image (with detected circles) to a file
def save_output(result, filename):
    # Save the result image in RGB format (plt.imsave uses RGB, while OpenCV uses BGR)
    plt.imsave(filename, cv2.cvtColor(result, cv2.COLOR_BGR2RGB))

# Get the image path from the user
image_path = get_image("Input")

# Process the image to detect circles
original, result, circle_count = detect_circles(image_path)

# Print the number of circles detected
print(f"The number of circles: {circle_count}")

# Show the results
show_result(original, result, circle_count)

# Extract the base filename (without path and extension) from the image path
base_filename = os.path.splitext(os.path.basename(image_path))[0]

# Save the output result image to the Output folder with a new filename
save_output(result, f"Output/{base_filename}-output.png")
