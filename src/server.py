from torchworker import TorchWorker
from inpaintingworker import InpaintingWorker
import sys


class Server(object):
    worker = None

    def __init__(self):
        self.worker = TorchWorker()

    def generate(self, prompt):
        self.worker.execute_prompt(prompt=prompt, steps=10)

    def run(self):

        while True:
            prompt = input("Input image prompt: ")
            if prompt == "q" or not prompt:
                break
            print(f"Generating image for prompt '{prompt}'")

            self.generate(prompt)
            for image in self.worker.images:
                image.save(f"generated/{prompt}.png".replace(' ', '_'))


if __name__ == "__main__":
    
    # create a server instance
    server = Server()
    
    # run the server
    server.run()


