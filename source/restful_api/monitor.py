from flask import Flask, request, jsonify
import os
from flask_restful import Resource, Api
from datetime import datetime
import random
import json
import os, sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
ROOT = os.getcwd()
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

app = Flask(__name__)
api = Api(app)
class HelloWorld(Resource):
    def get(self):
        return {'message': "hello world!"}
    

        


api.add_resource(HelloWorld, '/')


if __name__ == '__main__':
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-port", type=str, default="1412", help="port")
    args = vars(parser.parse_args())
    app_port = args["port"]

    app.run(debug=True, host='0.0.0.0', port=app_port)