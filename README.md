# ImaginePy

An app to run stable-diffusion backed imaginative prompts on your phone

## Installation

We depend on quite a few libraries to make this work. The following dependencies need to available in your environment:

  - `pytorch` with cuda enabled
  - `diffusers`
  - `flask`
  - `flask-restful`
  - `python-dotenv`

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
pip install python-dotenv
```
  
## Usage

This library depends on some environment variables, which are **not** included in this repository.
To make this work, create a `.env` file at the root level and have it expose the following environment variables

```dotenv
# ip and port of the server to run
SERVER_IP = http://127.0.0.1
SERVER_PORT = 5000

# path to your local version of the diffursers model
DIFFUSERS_PATH = C:/path_to_your_diffusers_folder
``` 

If everything is setup correctly, you can just run the server in one command prompt and send requests to it in another one

```sh
# run in one cmd prompt
python src/app.py  

# run from another cmd prompt
just test-api-custom "My cool prompt that I want to test"
```
