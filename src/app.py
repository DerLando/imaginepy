from flask import Flask
from flask_restful import Resource, Api, reqparse
from torchworker import TorchWorker
from PIL import Image
import base64
from io import BytesIO, StringIO

# Define the main app and api
app = Flask(__name__)
api = Api(app)

# define a parser for the arguments to the api
parser = reqparse.RequestParser()
# parser.add_argument("prompt", type=str, help="The prompt to execute", required=True)
parser.add_argument("steps", type=int, help="The number of steps to execute", default=50)
parser.add_argument("size", type=int, help="The size of the finished image, size x size", default=512)

# worker disabled for testing purposes
# worker = TorchWorker()

def encode_image(image):
    """
    encodes an image as a base64 string    
    """
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    
    img_str = str(base64.b64encode(buffered.getvalue()))
    # print(img_str)
    return img_str

class Imagination(Resource):
    def get(self, prompt):
        args = parser.parse_args(strict=True)
        # return {prompt: worker.execute_prompt(prompt, steps=10[0])
        return args

    def put(self, prompt):
        args = parser.parse_args(strict=True)
        args['prompt'] = prompt
        args['image'] = encode_image(Image.new('RGB', (args['size'], args['size'])))
        # args['image'] = "my_image"      
        # return {'test': prompt}
        return args

# Add endpoint for our prompt resource
api.add_resource(Imagination, '/<string:prompt>')

if __name__ == '__main__':
    app.run(debug=True)