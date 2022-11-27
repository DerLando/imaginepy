from flask import Flask
from flask_restful import Resource, Api, reqparse
from torchworker import TorchWorker
from PIL import Image
import base64
from io import BytesIO, StringIO
import logging
import sys

DEBUG = False
WORKER = None

# Define the main app and api
app = Flask(__name__)
api = Api(app)

# define a parser for the arguments to the api
parser = reqparse.RequestParser()
# parser.add_argument("prompt", type=str, help="The prompt to execute", required=True)
parser.add_argument("steps", type=int, help="The number of steps to execute", default=50)
parser.add_argument("size", type=int, help="The size of the finished image, size x size", default=512)
parser.add_argument("seed", type=int, help="The seed to initialize the random generator", default=42)

def encode_image(image):
    """
    encodes an image as a base64 string    
    """
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    
    img_str = str(base64.b64encode(buffered.getvalue()))
    # print(img_str)
    return img_str

def create_image_filename(prompt, seed):
    return f"{prompt.replace(' ', '_')}_{seed}_.png"
    
def generate_image(prompt, steps=10, seed=42, debug=False):
    if debug:
        image = Image.open("./images/debug_image.png")
        
    else:
        image = WORKER.execute_prompt(prompt, steps=steps, seeds=[seed])[0]
        
    return encode_image(image)

class Imagination(Resource):
    def get(self, prompt):
        args = parser.parse_args(strict=True)
        return args

    def put(self, prompt):
        args = parser.parse_args()
        args['prompt'] = prompt
        args['image'] = generate_image(prompt, steps=args['steps'], seed=args['seed'], debug=DEBUG)
        args['filename'] = create_image_filename(prompt, args['seed'])
        return args

# Add endpoint for our prompt resource
api.add_resource(Imagination, '/<string:prompt>')

if __name__ == '__main__':

    # any cmd arg is explicity parsed as running in debug mode
    if len(sys.argv) > 1:
        DEBUG = True
    else:
        WORKER = TorchWorker()

    app.run(debug=DEBUG)