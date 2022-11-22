# ImaginePy

An app to run stable-diffusion backed imaginative prompts on your phone

## Installation

We depend on quite a few libraries to make this work. The following dependencies need to available in your environment:

  - `pytorch` with cuda enabled
  - `diffusers`
  - `flask`
  - `flask-restful`

Additionally we also use a few cli utilities

  - `just` as a easy-to-use command runner, **not** mandatory
  - `localtunnel` to expose our flask app to the web, **mandatory**
  
### Python libraries

To install the missing python libraries, use the following pip commands in your project environment

```sh
pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117
pip install --upgrade diffusers[torch]
pip install flask
pip install flask-restful
```
  
