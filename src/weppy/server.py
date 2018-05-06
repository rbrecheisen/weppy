import os
import uuid
from werkzeug.datastructures import FileStorage
from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp/weppy/scripts'
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
                script_name = secure_filename(script.filename)
                d = os.path.join(app.config['UPLOAD_FOLDER'], script_id)
                os.makedirs(d, exist_ok=False)
                f = os.path.join(d, script_name)
                script.save(f)
                return {'script_id': script_id, 'script_name': script_name}, 200
            else:
                abort(400, message='Script file extension not in {}'.format(app.config['ALLOWED_EXTENSIONS']))
        else:
            abort(500, message='Error uploading script {}'.format(script.filename))


class ScriptRunner(Resource):

    @staticmethod
    def get():

        parser = reqparse.RequestParser()
        parser.add_argument('script_id', type=str)
        parser.add_argument('script_name', type=str)
        args = parser.parse_args()

        # Any other parameters of the script need to be extracted here. We don't know beforehand
        # which parameters, unless we stored that information when the script was uploaded.
        # Perhaps we should also upload a parameter definition list together with the script or
        # have the ScriptLoader extract this information from the Script interface.

        script_file = os.path.join(app.config['UPLOAD_FOLDER'], args['script_id'], args['script_name'])
        os.system('python {}'.format(script_file))

        return 'OK', 200


api.add_resource(ScriptLoader, '/loader')
api.add_resource(ScriptRunner, '/runner')


if __name__ == '__main__':
    app.run(debug=True)
