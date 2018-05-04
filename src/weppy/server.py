import os
from werkzeug.datastructures import FileStorage
from flask import Flask
from flask_restful import Resource, Api, reqparse
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp/weppy/scripts'
app.config['ALLOWED_EXTENSIONS'] = '.py'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
api = Api(app)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


class ScriptLoader(Resource):

    @staticmethod
    def post():

        parser = reqparse.RequestParser()
        parser.add_argument('script', type=FileStorage, location='files')
        args = parser.parse_args()

        script = args['script']
        if script and allowed_file(script.filename):
            script.save(
                os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(script.filename)))
            return {'uploaded': script.filename}
        else:
            print('Error uploading script {}'.format(script.filename))


class ScriptRunner(Resource):

    def get(self):
        return {'script': 'runner'}


api.add_resource(ScriptLoader, '/loader')
api.add_resource(ScriptRunner, '/runner')


if __name__ == '__main__':
    app.run(debug=True)
