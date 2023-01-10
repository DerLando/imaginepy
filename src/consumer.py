from requests import put
from io import BytesIO
from PIL import Image
import base64
import os
import sys
from dotenv import load_dotenv
from torchworker import TorchWorker
from PIL import Image
import argparse
from imageworker import encode_image, decode_image

if not load_dotenv("./.env"):
    print("Consumer failed to load environment")


class Consumer(object):
    """
    A consumer of our API. This exposes high-level helper methods
    to request images from our imagine api.
    """

    ip = os.getenv("SERVER_IP", "http://127.0.0.1")
    port = os.getenv("SERVER_PORT", "5000")
    url = f"{ip}:{port}/"  # localhost on port 5000

    def __init__(self, url=None, inpaint=False):
        if url is not None:
            self.url = url
        if inpaint:
            self.url += "inpaint/"

    def _prompt_url(self, prompt):
        return f"{self.url}{prompt}"

    def generate_image(self, prompt, steps=10, seed=None, size=512, image_path=None, strength=0.8):
        """
        Generate an image with the given number of generation steps
        """
        args = {}
        if seed is None:
            seed = TorchWorker.create_seed()
        args['seed'] = seed
        args['steps'] = steps
        args['size'] = size
        args['strength'] = strength

        print(f"Consumer putting {self._prompt_url(prompt)} with args {args}")

        if image_path is not None:
            args['image'] = encode_image(Image.open(image_path))            
        
        return put(self._prompt_url(prompt), json=args).json()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-p', '--prompt', help="The text prompt to generate an image for", required=True)
    parser.add_argument('-s', '--seed', help="The initial seed to use")
    parser.add_argument('-n', '--steps', type=int, help="The number of steps to run the generation for", choices=range(10, 120), default=20)
    parser.add_argument('-c', '--count', type=int, help="The number of images to generate", choices=[1, 2, 3, 4], default=1)
    parser.add_argument('-lt', '--local-tunnel', help="Connect to local tunnel address", type=str, required=False)
    parser.add_argument('-w', '--size', type=int, help="Size of the final image, must be divisible by 8", default=512)
    parser.add_argument('-i', '--image', help="An optional image to inpaint the prompt into", required=False)
    parser.add_argument('-f', '--strength', help="The strength of the image input", default = 0.8, type=float)

    args = parser.parse_args()

    inpaint = args.image is not None

    if args.__contains__("local_tunnel"):
        consumer = Consumer(args.local_tunnel, inpaint=inpaint)
    else:
        consumer = Consumer(inpaint=inpaint)
    
    for _ in range(args.count):
    
        result = consumer.generate_image(args.prompt, args.steps, args.seed, args.size, args.image, args.strength)
        for k, v in result.items():
            if k == 'image':
                image = decode_image(v)
                filepath = f"./generated/{result['filename']}"
                filepath = os.path.abspath(filepath)
                print(filepath)
                image.save(filepath)
            else:
                print(k, ": ", v)
