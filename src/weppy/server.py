import os
from werkzeug.datastructures import FileStorage
from flask import Flask
from flask_restful import Resource, Api, reqparse
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp/weppy/scripts'
app.config['ALLOWED_EXTENSIONS'] = '.py'

api = Api(app)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


class ScriptLoader(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('script', type=FileStorage, location='files')
        args = parser.parse_args()
        if args['script'] and allowed_file(args['script'].filename):
            args['script'].save(
                os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(args['script'].filename)))
            return {'script': args['script'].filename}
        else:
            print('Error')


class ScriptRunner(Resource):

    def get(self):
        return {'script': 'runner'}


api.add_resource(ScriptLoader, '/loader')
api.add_resource(ScriptRunner, '/runner')


if __name__ == '__main__':
    app.run(debug=True)
