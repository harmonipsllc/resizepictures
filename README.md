# Image Resizer App

## Overview

The Image Resizer App is a desktop application built using Python, PyQt5 for the graphical user interface, and OpenCV for image processing. The application allows users to drag and drop a folder or individual image files, resize them to a specified resolution, and save the resized images with a "_resized" suffix in PNG format.

The Image Resizer App is available in two versions:
1. A desktop application built using Python, PyQt5 for the graphical user interface, and OpenCV for image processing.
2. A web-based application built using Python, Dash for the graphical user interface, and OpenCV for image processing.

Both versions allow users to drag and drop image files, resize them to a specified resolution, and save the resized images with a "_resized" suffix in PNG format.


## Features

- Drag and drop image files.
- Resize images to a specified resolution while maintaining the aspect ratio.
- Crop images from the center if they are larger than the specified resolution.
- Save resized images with a "_resized" suffix in PNG format.
- Display the original and resized images side by side (web-based version).
- Download all resized images as a zip file (web-based version).
- Display the number of files being processed and a progress bar (desktop version).

## Requirements

- Python 3.x
- For the desktop version: PyQt5, OpenCV
- For the web-based version: Dash, OpenCV

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/harmonipsllc/resizepictures.git
    cd resizepictures
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

## Desktop Version

1. Run the application:
    ```sh
    python src/main.py
    ```

2. The main window will appear with a label indicating to drop image files.

3. Drag and drop image files into the main window.

4. A dialog will appear asking for the desired width and height in pixels. The default resolution is set to 1920x1080.

5. The application will process the images, displaying the number of files being processed and updating the progress bar.

6. The resized images will be saved in the same directory as the original images with a "_resized" suffix and in PNG format.

### Web-Based Version

1. Run the application:
    ```sh
    python launch_dash.py
    ```

2. The web browser will open with the Image Resizer App.

3. Drag and drop image files into the upload area.

4. Enter the desired width and height in pixels. The default resolution is set to 1920x1080.

5. Select whether to crop or resize the images.

6. Click the "Resize" button to process the images.

7. The original and resized images will be displayed side by side.

8. Click the "Save" button to download all resized images as a zip file.

## Code Structure

- [launch_dash.py]: The launcher script that starts the Dash server and opens the web browser.
- [app.py]: The main application file for the web-based version that sets up the Dash interface and handles image processing.
- [main.py]: The main application file for the desktop version that sets up the GUI and handles drag-and-drop events.
- [main_controller.py]: The controller that handles image processing and saving.
- [file_utils.py]: Utility functions for file operations.

# Example

### Desktop Version

1. Drag and drop image files into the application window.
2. Enter the desired resolution (e.g., 1920x1080).
3. The application will resize the images and save them with a "_resized" suffix in PNG format.

### Web-Based Version

1. Drag and drop image files into the upload area.
2. Enter the desired resolution (e.g., 1920x1080).
3. Select whether to crop or resize the images.
4. Click the "Resize" button to process the images.
5. The original and resized images will be displayed side by side.
6. Click the "Save" button to download all resized images as a zip file.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact
For any questions or inquiries, please contact [arnaudjeanvoine@gmail.com].

