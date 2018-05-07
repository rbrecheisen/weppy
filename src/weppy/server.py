import os
import uuid
from werkzeug.datastructures import FileStorage
from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'weppy/scripts/upload'
app.config['ALLOWED_EXTENSIONS'] = '.py'
app.config['BUNDLE_ERRORS'] = True

api = Api(app)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def generate_uuid():
    return str(uuid.uuid4())


class ScriptLoader(Resource):

    @staticmethod
    def post():

        parser = reqparse.RequestParser()
        parser.add_argument('script', type=FileStorage, location='files')
        args = parser.parse_args()

        script = args['script']
        if script:
            if allowed_file(script.filename):
                script_id = generate_uuid()
                # Open script and inspect its parameters
                # Create params.txt file where you store the scripts parameter definitions
                f = os.path.join(app.config['UPLOAD_FOLDER'], '{}.py'.format(script_id))
                script.save(f)
                return {'script_id': script_id}, 200
            else:
                abort(400, message='Script file extension not in {}'.format(app.config['ALLOWED_EXTENSIONS']))
        else:
            abort(500, message='Error uploading script {}'.format(script.filename))


class ScriptRunner(Resource):

    @staticmethod
    def get():

        parser = reqparse.RequestParser()
        parser.add_argument('script_id', type=str)
        # Get parameters as JSON string and convert to Python dictionary
        parser.add_argument('params', type=str)
        args = parser.parse_args()

        # Any other parameters of the script need to be extracted here. We don't know beforehand
        # which parameters, unless we stored that information when the script was uploaded.
        # Perhaps we should also upload a parameter definition list together with the script or
        # have the ScriptLoader extract this information from the Script interface.

        # Properly import the script using importlib
        script_file = os.path.join(app.config['UPLOAD_FOLDER'], args['script_id'] + '.py')
        os.system('python {}'.format(script_file))
        return 'OK', 200


api.add_resource(ScriptLoader, '/loader')
api.add_resource(ScriptRunner, '/runner')


if __name__ == '__main__':
    app.run(debug=True)
