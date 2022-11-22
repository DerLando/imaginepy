from requests import get, put

class Consumer(object):
    """
    A consumer of our API    
        
    """

    url = "http://127.0.0.1:5000/" # localhost on port 5000

    def __init__(self, url=None):
        if url is not None:
            self.url = url

    def _prompt_url(self, prompt):
        return f"{self.url}{prompt}"

    def generate_image(self, prompt):
        return put(self._prompt_url(prompt), json={'steps': 10}).json()
        
if __name__ == "__main__":

    consumer = Consumer()
    result =  consumer.generate_image("A photo of an astronaut in mars")
    
    print(result)
    