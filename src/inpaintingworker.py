import torch
import random
from diffusers import StableDiffusionInpaintPipeline
from dotenv import load_dotenv
from imageworker import ImageWorker
import os

if not load_dotenv("./.env"):
    print("TorchWorker failed to load environment")

MIN_SEED = 1000000000
MAX_SEED = 9999999999

class InpaintingWorker(object):
    """
    A thread-safe worker that wraps a StableDiffusionPipeling.
    In the future this class will expose all possible ways of generating images
    for us.    
    """
    pipeline = None
    model_path = os.getenv("INPAINTING_PATH", "D:/Git/stable-diffusion-v-1-5")
    prompt = "A futuristic pavillon, hyperrealistic octane render"
    image_count = 1
    seeds = [42]
    steps = 51
    images = []
    strength = 0.5
    
    def __init__(self, model_path = None):
        if model_path is not None:
            self.model_path = model_path
        
        self.pipeline = StableDiffusionInpaintPipeline.from_pretrained(self.model_path, torch_dtype = torch.float16, revision="fp16")
        self.pipeline = self.pipeline.to("cuda")
        self.pipeline.enable_attention_slicing()
        
    def execute_prompt(self, image, prompt=None, image_count=None, seeds=None, steps=None, strength=None):
        """
        Execute the given prompt    
        """
        
        mask = ImageWorker(image).create_mask()
        
        if prompt is not None:
            self.prompt = prompt
            
        if image_count is not None:
            self.image_count = image_count
        
        if seeds is not None:
            self.seeds = seeds
            
        if steps is not None:
            self.steps = steps
        
        if strength is not None:
            self.strengths = strength
            
        # clear image buffer
        self.images = []
        
        # make sure we have the correct number of seeds
        if len(self.seeds) != self.image_count:
            self._seed()
         
        # TODO: Use this to implement multiple image generation       
        # https://github.com/pcuenca/diffusers-examples/blob/main/notebooks/stable-diffusion-seeds.ipynb   
            
        # itererate over seeds and create images
        for seed in self.seeds:
                        
            self.images.append(self.pipeline(self.prompt, image=image, mask_image=mask, num_inference_steps=self.steps, strength = self.strength, generator=torch.Generator(device="cuda").manual_seed(seed)).images[0])
        
        return self.images
        
    @staticmethod
    def create_seed():
        return random.randint(MIN_SEED, MAX_SEED)
        
        
    def _seed(self):
        self.seeds = [self.create_seed() for _ in range(self.image_count)]
        
        
if __name__ == "__main__":
    from PIL import Image
    
    worker = InpaintingWorker()
    test_image = Image.open("./images/debug_input.png")
    images = worker.execute_prompt(test_image, prompt="A building on the moon, 8k, photography 55mm lens", steps = 20, strength = 0.8)

    # TODO: Implement this worker in the server-client architecture to finalize it...

    print(f"generated {len(images)} images...")    
        
    for i, image in enumerate(images):
        image.save(f"./images/inpainting_test_{i}.png")

