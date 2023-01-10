from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from torchworker import TorchWorker
from inpaintingworker import InpaintingWorker
from PIL import Image
import base64
from io import BytesIO, StringIO
import logging
import sys
from flask_lt import run_with_lt
import argparse
from imageworker import encode_image, decode_image

DEBUG = False
WORKER = None

# Define the main app and api
app = Flask(__name__)
api = Api(app)

# define a parser for the arguments to the api
req_parser = reqparse.RequestParser()
# parser.add_argument("prompt", type=str, help="The prompt to execute", required=True)
req_parser.add_argument("steps", type=int, help="The number of steps to execute", default=50)
req_parser.add_argument("size", type=int, help="The size of the finished image, size x size", default=512)
req_parser.add_argument("seed", type=int, help="The seed to initialize the random generator", default=42)
req_parser.add_argument("image", help="Base64 encoded input image, optional")
req_parser.add_argument("strength", help="The strength of an input image", default=0.5)

def create_image_filename(prompt, seed):
    return f"{prompt.replace(' ', '_')}_{seed}_.png"
    
def inpaint_image(prompt, image, steps=10, seed=42, debug=False, strength=0.5):
    if debug:
        image = Image.open("./images/debug_image.png")
    else:
        image = WORKER.execute_prompt(image, prompt, seeds=[seed], steps=steps, strength=strength)[0]
        
    return encode_image(image)
        
def generate_image(prompt, steps=10, seed=42, debug=False, size=512):
    if debug:
        image = Image.open("./images/debug_image.png")
        
    else:
        image = WORKER.execute_prompt(prompt, steps=steps, seeds=[seed], size=size)[0]
        
    return encode_image(image)
    
class Inpaintination(Resource):
    def put(self, prompt):
        args = req_parser.parse_args()
        args['prompt'] = prompt
        
        # actually parse the input image
        args['image'] = decode_image(args['image'])
        args['image'] = inpaint_image(prompt, args['image'], steps=args['steps'], seed=args['seed'], debug=DEBUG, strength=args['strength'])
        args['filename'] = create_image_filename(prompt, args['seed'])
        return args

class Imagination(Resource):
    def get(self, prompt):
        args = req_parser.parse_args(strict=True)
        return args

    def put(self, prompt):
        args = req_parser.parse_args()
        args['prompt'] = prompt
        args['image'] = generate_image(prompt, steps=args['steps'], seed=args['seed'], debug=DEBUG, size=args['size'])
        args['filename'] = create_image_filename(prompt, args['seed'])
        return args

# Add endpoint for our prompt resource
api.add_resource(Imagination, '/<string:prompt>')
api.add_resource(Inpaintination, '/inpaint/<string:prompt>')

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', help="Run server in debug mode", default=False, action='store_true')
    parser.add_argument('-lt', help="Run server with localtunnel", default=False, action='store_true')
    parser.add_argument('-p', '--inpaint', help="Use inpainting Api", default=False, action='store_true')
    args = parser.parse_args()
    
    # any cmd arg is explicity parsed as running in debug mode
    if args.debug:
        DEBUG = True
    else:
        if args.inpaint:
            WORKER = InpaintingWorker()
        else:
            WORKER = TorchWorker()

    if args.lt:
        run_with_lt(app, "Lando")

    app.run(debug=DEBUG)