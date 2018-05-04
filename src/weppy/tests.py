import io
import unittest
import weppy.server


# http://flask.pocoo.org/docs/0.12/testing/
class ScriptLoaderTest(unittest.TestCase):

    def setUp(self):
        self.app = weppy.server.app.test_client()

    # https://stackoverflow.com/questions/35684436/testing-file-uploads-in-flask
    def test_post(self):
        data = dict(script=(io.BytesIO(b'test.py'), 'test.py'))
        self.app.post('http://localhost:5000/loader', data=data, content_type='multipart/form-data')


class ScriptRunnerTest(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
