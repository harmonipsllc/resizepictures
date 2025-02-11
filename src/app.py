import os
import cv2
import base64
import numpy as np
import zipfile
import io
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from flask import Flask, send_file
from utils.file_utils import FileUtils
from controllers.main_controller import MainController

# Initialize Flask server and Dash app
server = Flask(__name__)
app = Dash(__name__, server=server)

# Initialize FileUtils and MainController
file_utils = FileUtils()
main_controller = MainController(None, file_utils, None)

# Store resized images in memory
resized_images_store = {}

# Layout of the Dash app
app.layout = html.Div([
    html.H1("Image Resizer App"),
    dcc.Upload(
        id='upload-image',
        children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=True
    ),
    html.Div(id='output-image-upload'),
    dcc.Input(id='input-width', type='number', placeholder='Width (default: 1920)', value=1920),
    dcc.Input(id='input-height', type='number', placeholder='Height (default: 1080)', value=1080),
    html.Button('Resize', id='resize-button', n_clicks=0),
    dcc.RadioItems(
        id='crop-or-resize',
        options=[
            {'label': 'Crop', 'value': 'crop'},
            {'label': 'Resize', 'value': 'resize'}
        ],
        value='resize',
        labelStyle={'display': 'inline-block'}
    ),
    html.Button('Save', id='save-button', n_clicks=0),
    html.Div(id='output-images'),
    html.Div(id='file-list', style={'marginTop': '20px'}),
    dcc.Download(id="download-zip")
])

def parse_contents(contents, filename):
    print(f"Parsing contents of file: {filename}")
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    np_arr = np.frombuffer(decoded, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return image, filename

@app.callback(
    Output('output-images', 'children'),
    Output('file-list', 'children'),
    Input('resize-button', 'n_clicks'),
    State('upload-image', 'contents'),
    State('upload-image', 'filename'),
    State('input-width', 'value'),
    State('input-height', 'value'),
    State('crop-or-resize', 'value')
)
def resize_images(n_clicks, contents, filenames, width, height, crop_or_resize):
    print(f"Resize button clicked {n_clicks} times")
    if n_clicks > 0 and contents is not None:
        try:
            images = [parse_contents(c, f) for c, f in zip(contents, filenames)]
            crop = (crop_or_resize == 'crop')
            output_images = []
            file_list = []

            for image, filename in images:
                print(f"Processing image: {filename}")
                resized_image = main_controller.process_image(image, width, height, crop)
                _, buffer = cv2.imencode('.png', resized_image)
                encoded_resized_image = base64.b64encode(buffer).decode('utf-8')
                encoded_original_image = base64.b64encode(cv2.imencode('.png', image)[1]).decode('utf-8')
                output_images.append(html.Div([
                    html.H5(filename),
                    html.Div([
                        html.Img(src='data:image/png;base64,{}'.format(encoded_original_image), style={'marginRight': '10px'}),
                        html.Img(src='data:image/png;base64,{}'.format(encoded_resized_image))
                    ], style={'display': 'flex'})
                ]))
                file_list.append(html.Div(filename))
                resized_images_store[filename] = buffer.tobytes()

            return output_images, file_list
        except Exception as e:
            print(f"Error processing images: {e}")
            return [html.Div(f"Error processing images: {e}")], []
    return [], []

@app.callback(
    Output("download-zip", "data"),
    Input("save-button", "n_clicks"),
    prevent_initial_call=True,
)
def save_images(n_clicks):
    if n_clicks > 0 and resized_images_store:
        # Create a zip file in memory
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for filename, buffer in resized_images_store.items():
                zip_file.writestr(filename, buffer)
        zip_buffer.seek(0)
        return dcc.send_bytes(zip_buffer.getvalue(), "resized_images.zip")
    return None

if __name__ == '__main__':
    print("Starting Dash server...")
    try:
        app.run_server(debug=True)
    except Exception as e:
        print(f"Error starting Dash server: {e}")