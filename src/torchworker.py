import torch
import random
from diffusers import StableDiffusionPipeline
from dotenv import load_dotenv
import os

if not load_dotenv("./.env"):
    print("TorchWorker failed to load environment")

MIN_SEED = 1000000000
MAX_SEED = 9999999999

class TorchWorker(object):
    """
    A thread-safe worker that wraps a StableDiffusionPipeling.
    In the future this class will expose all possible ways of generating images
    for us.    
    """
    pipeline = None
    model_path = os.getenv("DIFFUSERS_PATH", "D:/Git/stable-diffusion-v-1-5")
    prompt = "A futuristic pavillon, hyperrealistic octane render"
    image_count = 1
    seeds = [42]
    steps = 51
    images = []
    
    def __init__(self, model_path = None):
        if model_path is not None:
            self.model_path = model_path
        
        #self.pipeline = StableDiffusionPipeline.from_pretrained(self.model_path, torch_dtype = torch.float16, revision="fp16", safety_checker=None)
        self.pipeline = StableDiffusionPipeline.from_pretrained(self.model_path, torch_dtype = torch.float16, revision="fp16")
        self.pipeline = self.pipeline.to("cuda")
        self.pipeline.enable_attention_slicing()
        
    def execute_prompt(self, prompt=None, image_count=None, seeds=None, steps=None, size=512):
        """
        Execute the given prompt    
        """
        
        if prompt is not None:
            self.prompt = prompt
            
        if image_count is not None:
            self.image_count = image_count
        
        if seeds is not None:
            self.seeds = seeds
            
        if steps is not None:
            self.steps = steps
            
        # clear image buffer
        self.images = []
        
        # make sure we have the correct number of seeds
        if len(self.seeds) != self.image_count:
            self._seed()
         
        # TODO: Use this to implement multiple image generation       
        # https://github.com/pcuenca/diffusers-examples/blob/main/notebooks/stable-diffusion-seeds.ipynb   
            
        # itererate over seeds and create images
        for seed in self.seeds:
                        
            self.images.append(self.pipeline(self.prompt, height=size, width=size, num_inference_steps=self.steps, generator=torch.Generator(device="cuda").manual_seed(seed)).images[0])
        
        return self.images
        
    @staticmethod
    def create_seed():
        return random.randint(MIN_SEED, MAX_SEED)
        
        
    def _seed(self):
        self.seeds = [self.create_seed() for _ in range(self.image_count)]
        
        
if __name__ == "__main__":
    worker = TorchWorker()
    images = worker.execute_prompt(steps = 10)


    print(f"generated {len(images)} images...")    
        
    for i, image in enumerate(images):
        image.save(f"worker_test_{i}.png")

