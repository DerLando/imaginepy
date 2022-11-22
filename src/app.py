from flask import Flask
from flask_restful import Resource, Api, reqparse
from torchworker import TorchWorker


# Define the main app and api
app = Flask(__name__)
api = Api(app)

# define a parser for the arguments to the api
parser = reqparse.RequestParser()
# parser.add_argument("prompt", type=str, help="The prompt to execute", required=True)
parser.add_argument("steps", type=int, help="The number of steps to execute", default=50)
# worker = TorchWorker()

class Imagination(Resource):
    def get(self, prompt):
        args = parser.parse_args(strict=True)
        # return {prompt: worker.execute_prompt(prompt, steps=10[0])
        return args


api.add_resource(Imagination, '/<string:prompt>')
# api.add_resource(Imagination, '/')

if __name__ == '__main__':
    app.run(debug=True)