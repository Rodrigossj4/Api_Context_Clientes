from flask import Flask
from flask_pydantic_spec import FlaskPydanticSpec
from flask_cors import CORS


class Server():
    def __init__(self,):
        self.app = Flask("__name__")
        self.api = FlaskPydanticSpec('Projeto PUC', title="Api Projeto")
        self.api.register(self.app)
        CORS(self.app)

    def run(self,):
        self.app.run()


server = Server()
