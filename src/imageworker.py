from PIL import Image, ImageFilter

ALPHA_TOLERANCE = 10

class ImageWorker():
    image: Image = None
    
    def __init__(self, image):
        self.image = image

    def create_mask(self) -> Image:
        """
        Generates a mask from an image with transparency.
        Stable diffusion inpainting wants a mask where black pixels
        are kept and white pixels are re-drawn, so we transform the original
        image pixels accordingly    
        """
        width, height = self.image.size
        mask = self.image.copy()
        data = mask.load()
        for y in range(height):
            for x in range(width):
                color = data[x, y]
                alpha = color[-1]
                if alpha > ALPHA_TOLERANCE:
                   color = (0, 0, 0, alpha)
                else:
                   color = (255, 255, 255, 255)
                data[x, y] = color
                
        mask = mask.filter(ImageFilter.GaussianBlur(13))
        return mask
        
if __name__ == "__main__":
    
    img = Image.open("./images/debug_input.png")
    worker = ImageWorker(img)
    
    mask = worker.create_mask()
    
    mask.save("./images/debug_mask_generated.png")    
    