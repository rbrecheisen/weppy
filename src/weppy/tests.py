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

        # Upload script and get its ID and URL
        script = open('weppy/scripts/hello_world.py', 'rb')
        response = self.app.post('http://localhost:5000/loader', data={
            'script': (script, 'hello_world.py'),
        }, content_type='multipart/form-data')
        script.close()
        script_id = response.json['script_id']
        script_url = response.json['script_url']
        print(script_url)

        # Check that a corresponding HTML has been generated for this script
        response = self.app.get(script_url)
        self.assertEqual(response.status_code, 200)

        # # Run uploaded script
        # file_path = quote_plus('/Users/Ralph/file.txt')
        # response = self.app.get(
        #     'http://localhost:5000/runner?script_id={}&in_file={}'.format(script_id, file_path))
        # self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
