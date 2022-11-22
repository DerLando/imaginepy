from requests import get, put
from io import BytesIO
from PIL import Image
import base64
import os
import sys
from dotenv import load_dotenv

if not load_dotenv("./.env"):
    print("Consumer failed to load environment")

def decode_image(img_str):
    # remove message fluff
    img_str = img_str.split('\'')[1]
    buffer = BytesIO(base64.b64decode(img_str))
    print(buffer)
    # TODO: Fix image loading issue
    try:
        image = Image.open(buffer)
    except e:
        print("Failed to decode image string")
        print(type(img_str))
        print(img_str)
        raise e
    return image

class Consumer(object):
    """
    A consumer of our API. This exposes high-level helper methods
    to request images from our imagine api.
    """

    ip = os.getenv("SERVER_IP", "http://127.0.0.1")
    port = os.getenv("SERVER_PORT", "5000")
    url = f"{ip}:{port}/" # localhost on port 5000

    def __init__(self, url=None):
        if url is not None:
            self.url = url

    def _prompt_url(self, prompt):
        return f"{self.url}{prompt}"

    def generate_image(self, prompt, steps=10):
        """
        Generate an image with the given number of generation steps  
        """
        return put(self._prompt_url(prompt), json={'steps': steps}).json()
        
if __name__ == "__main__":

    args = sys.argv
    if len(args) == 2:
        prompt = args[1]
    else:
        print(args)
        prompt = "A photo of an astronaut on mars"

    consumer = Consumer()
    result = consumer.generate_image(prompt, steps=20)
    for k,v in result.items():
        if k == 'image':
            image = decode_image(v)
            filepath = f"./generated/{result['prompt'].replace(' ', '_')}.png"
            filepath = os.path.abspath(filepath)
            print(filepath)
            image.save(filepath)
        else:
            print(k, ": ", v)
    