import io
from urllib.parse import quote_plus
import unittest
import weppy.server


# http://flask.pocoo.org/docs/0.12/testing/
class ScriptRunnerTest(unittest.TestCase):

    def setUp(self):
        self.app = weppy.server.app.test_client()

    # https://stackoverflow.com/questions/35684436/testing-file-uploads-in-flask
    def test_post(self):

        # Upload script
        script = open('weppy/scripts/hello_world.py', 'rb')
        response = self.app.post('http://localhost:5000/loader', data={
            'script': (script, 'hello_world.py'),
        }, content_type='multipart/form-data')
        script.close()

        # Run uploaded script
        script_id = response.json['script_id']
        script_name = response.json['script_name']
        file_path = quote_plus('/Users/Ralph/file.txt')
        response = self.app.get(
            'http://localhost:5000/runner?script_id={}&script_name={}&in_file={}'.format(
                script_id, script_name, file_path))
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
