from requests import put
from io import BytesIO
from PIL import Image
import base64
import os
import sys
from dotenv import load_dotenv
from torchworker import TorchWorker
import argparse

if not load_dotenv("./.env"):
    print("Consumer failed to load environment")


def decode_image(img_str):
    """
    Decode a base64 encoded image string back into an image
    """
    # remove message fluff
    img_str = img_str.split('\'')[1]
    buffer = BytesIO(base64.b64decode(img_str))
    try:
        image = Image.open(buffer)
    except:
        print("Failed to decode image string")
        print(type(img_str))
        print(img_str)
        raise
    return image


class Consumer(object):
    """
    A consumer of our API. This exposes high-level helper methods
    to request images from our imagine api.
    """

    ip = os.getenv("SERVER_IP", "http://127.0.0.1")
    port = os.getenv("SERVER_PORT", "5000")
    url = f"{ip}:{port}/"  # localhost on port 5000

    def __init__(self, url=None):
        if url is not None:
            self.url = url

    def _prompt_url(self, prompt):
        return f"{self.url}{prompt}"

    def generate_image(self, prompt, steps=10, seed=None):
        """
        Generate an image with the given number of generation steps
        """
        args = {}
        if seed is None:
            seed = TorchWorker.create_seed()
        args['seed'] = seed
        args['steps'] = steps

        print(f"Consumer putting {args} for prompt {prompt}")

        return put(self._prompt_url(prompt), json=args).json()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-p', '--prompt', help="The text prompt to generate an image for", required=True)
    parser.add_argument('-s', '--seed', help="The initial seed to use")
    parser.add_argument('-n', '--steps', type=int, help="The number of steps to run the generation for", choices=range(10, 120), default=20)
    parser.add_argument('-c', '--count', type=int, help="The number of images to generate", choices=[1, 2, 3, 4], default=1)
    parser.add_argument('-lt', '--local-tunnel', help="Connect to local tunnel address", type=str, required=False)

    args = parser.parse_args()

    if args.__contains__("local_tunnel"):
        consumer = Consumer(args.local_tunnel)
    else:
        consumer = Consumer()
    
    result = consumer.generate_image(args.prompt, args.steps, args.seed)
    for k, v in result.items():
        if k == 'image':
            image = decode_image(v)
            filepath = f"./generated/{result['filename']}"
            filepath = os.path.abspath(filepath)
            print(filepath)
            image.save(filepath)
        else:
            print(k, ": ", v)
