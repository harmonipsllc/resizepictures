# Image Resizer App

## Overview

The Image Resizer App is a desktop application built using Python, PyQt5 for the graphical user interface, and OpenCV for image processing. The application allows users to drag and drop a folder or individual image files, resize them to a specified resolution, and save the resized images with a "_resized" suffix in PNG format.

## Features

- Drag and drop a folder or individual image files.
- Resize images to a specified resolution while maintaining the aspect ratio.
- Crop images from the center if they are larger than the specified resolution.
- Save resized images with a "_resized" suffix in PNG format.
- Display the number of files being processed and a progress bar.

## Requirements

- Python 3.x
- PyQt5
- OpenCV

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

1. Run the application:
    ```sh
    python src/main.py
    ```

2. The main window will appear with a label indicating to drop a folder or files.

3. Drag and drop a folder or individual image files into the main window.

4. A dialog will appear asking for the desired width and height in pixels. The default resolution is set to 1920x1080.

5. The application will process the images, displaying the number of files being processed and updating the progress bar.

6. The resized images will be saved in the same directory as the original images with a "_resized" suffix and in PNG format.

## Code Structure

- [main.py]: The main application file that sets up the GUI and handles drag-and-drop events.
- `src/controllers/main_controller.py`: The controller that handles image processing and saving.
- `src/utils/file_utils.py`: Utility functions for file operations.

## Example

1. Drag and drop a folder or image files into the application window.
2. Enter the desired resolution (e.g., 1920x1080).
3. The application will resize the images and save them with a "_resized" suffix in PNG format.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact

<<<<<<< HEAD
For any questions or inquiries, please contact [arnaudjeanvoine@gmail.com].
=======
For any questions or inquiries, please contact [arnaudjeanvoine@gmail.com].
>>>>>>> 192f00e80a40e30683220beec8a703d6d2e7199f
