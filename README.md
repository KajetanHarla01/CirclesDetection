<h1>Overview</h1>
    <p>
        This script is designed to detect and count circular pieces in thermographic images using Python. 
        It uses image processing techniques such as contour detection and circularity measurement to identify complete circles. 
        The results are visualized and saved for further analysis.
    </p>
    <hr>
  <h1>Features</h1>
    <ul>
        <li>Detects and quantifies circular objects in thermographic images.</li>
        <li>Displays the original and processed images side by side for easy visualization.</li>
        <li>Saves the output image with detected circles to a specified directory.</li>
    </ul>
    <hr>
  <h1>Requirements</h1>
    <h2>Dependencies</h2>
    <p>The following Python libraries are required to run the script:</p>
    <ul>
        <li><strong>OpenCV</strong>: For image processing operations.</li>
        <li><strong>NumPy</strong>: For numerical operations on image data.</li>
        <li><strong>Matplotlib</strong>: For displaying and saving results.</li>
    </ul>
    <p>Install the required libraries using:</p>
    <pre>
        <code>pip install opencv-python-headless numpy matplotlib</code>
    </pre>
    <h2>Directory Structure</h2>
    <ul>
        <li><strong>Input:</strong> Folder containing input thermographic images.</li>
        <li><strong>Output:</strong> Folder to save the processed output images.</li>
    </ul>
    <hr>
  <h1>Usage</h1>
    <h2>Steps to Run the Script</h2>
    <ol>
        <li><strong>Prepare the Environment:</strong>
            <ul>
                <li>Place the input thermographic images in the <code>Input</code> folder.</li>
                <li>Ensure the <code>Output</code> folder exists to save results.</li>
            </ul>
        </li>
        <li><strong>Run the Script:</strong>
            <code>python main.py</code>
        </li>
        <li><strong>Choose an Image:</strong> 
            The script will list all images in the <code>Input</code> directory. Select an image by entering its corresponding number.
        </li>
        <li><strong>View the Results:</strong> 
            The script will display the original and processed images side by side. It will also print the number of circles detected in the image.
        </li>
        <li><strong>Check the Output Folder:</strong> 
            The processed image with detected circles is saved in the <code>Output</code> folder with the filename <code>&lt;original_name&gt;-output.png</code>.
        </li>
    </ol>
    <hr>
  <h1>Functions</h1>
    <ul>
        <li><strong><code>get_image(dir)</code>:</strong> Lists files in the specified directory and allows the user to select one.</li>
        <li><strong><code>smooth_contour(contour, n)</code>:</strong> Smoothens a contour by averaging <code>n</code> neighboring points.</li>
        <li><strong><code>normalize_image(image, target_width)</code>:</strong> Resizes the image while maintaining the aspect ratio.</li>
        <li><strong><code>scale_contour(contour, scale_factor)</code>:</strong> Scales a contour by the resizing scale factor.</li>
        <li><strong><code>detect_circles(image_path)</code>:</strong> Detects complete circles in the input image and returns:
            <ul>
                <li>Original image</li>
                <li>Processed image with detected circles</li>
                <li>Count of detected circles</li>
            </ul>
        </li>
        <li><strong><code>show_result(original, result, circle_count)</code>:</strong> Displays the original and processed images side by side.</li>
        <li><strong><code>save_output(result, filename)</code>:</strong> Saves the processed image with detected circles.</li>
    </ul>
    <hr>
