import os
import uuid
import importlib
from werkzeug.datastructures import FileStorage
from flask import Flask, request, Response, render_template
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


def import_script(script_id):
    return importlib.import_module('weppy.scripts.upload.{}'.format(script_id[:-3]))


def create_and_save_html(script_id, args, arg_types):
    html_file = '{}.html'.format(script_id[:-3])
    f = open('weppy/templates/{}'.format(html_file), 'w')
    f.write('<html>\n')
    f.write('  <b>{}</b>\n'.format(script_id))
    f.write('  <form action="http://localhost:5000/runner" method="get">\n')
    f.write('    <table>\n')
    for k in args.keys():
        f.write('      <tr>\n')
        f.write('        <td>{}</td>\n'.format(k))
        f.write('        <td><input type="text" value=""/></td>\n')
        f.write('      </tr>\n')
    f.write('    </table>\n')
    f.write('    <input type="hidden" name="script_id" value="{}"/>\n'.format(script_id))
    f.write('    <input type="submit" value="Run script"/>\n')
    f.write('  </form>\n')
    f.write('</html>\n')
    f.close()
    return 'http://localhost:5000/{}'.format(html_file)


def output_html(data, code, headers=None):
    resp = Response(data, mimetype='text/html', headers=headers)
    resp.status_code = code
    return resp


class ScriptHtmlRenderer(Resource):

    @staticmethod
    def get(html):
        return output_html(render_template(html), 200)


class ScriptLoader(Resource):

    @staticmethod
    def post():
        # Parse request parameters
        parser = reqparse.RequestParser()
        parser.add_argument('script', type=FileStorage, location='files')
        args = parser.parse_args()
        # Get uploaded script
        script = args['script']
        if script:
            if allowed_file(script.filename):
                # Save script file to upload folder
                script_id = secure_filename(script.filename)
                f = os.path.join(app.config['UPLOAD_FOLDER'], script_id)
                script.save(f)
                # Import the script and get its parameters
                script_module = import_script(script_id)
                args = script_module.arg_parser.get_args()
                arg_types = script_module.arg_parser.get_arg_types()
                # Generate an HTML page that allows setting these parameters
                script_url = create_and_save_html(script_id, args, arg_types)
                return {'script_id': script_id, 'script_url': script_url}, 200
            else:
                abort(400, message='Script file extension not in {}'.format(app.config['ALLOWED_EXTENSIONS']))
        else:
            abort(500, message='Error uploading script {}'.format(script.filename))


class ScriptRunner(Resource):

    @staticmethod
    def get():

        args = request.args

        # Get script ID and import it
        script_id = args['script_id']
        script_module = importlib.import_module('weppy.scripts.upload.{}'.format(script_id[:-3]))

        # Get parameters
        params = []
        for k in args.keys():
            if k == 'script_id':
                continue
            params.append('--{}={}'.format(k, args[k]))

        # Build command and run it
        print('Running script {}'.format(script_id))
        script_module.run(params)

        return 'OK', 200


api.add_resource(ScriptHtmlRenderer, '/<string:html>')
api.add_resource(ScriptLoader, '/loader')
api.add_resource(ScriptRunner, '/runner')


if __name__ == '__main__':
    app.run(debug=True)
