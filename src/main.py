from flask import Flask
from flask_restx import Api, Resource

class App():
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app, version='1.0.0', doc='/docs', title='Reports API', description='Reports API')

    def run(self):
        self.app.run(debug=True)

app = App()

reports_namespace = app.api.namespace('reports', description='Reports operations')

@reports_namespace.route('/')
class Reports(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)

    def get(self,):
        return ["abcde"], 200

if __name__ == '__main__':
    app.run()