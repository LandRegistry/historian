import unittest
from application import server, app
import json


class ApplicationTestCase(unittest.TestCase):

    def setUp(self):
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()

        headers = {'content-type': 'application/json; charset=utf-8'}
        history_data = '{"title_number": "TEST1412258807231" }'
        self.app.post('/TEST1412853022495', data=history_data, headers=headers)


    def test_that_get_root_fails(self):
        self.assertEqual((self.app.get('/')).status, '400 BAD REQUEST')

    def test_that_post_root_fails(self):
        self.assertEqual((self.app.post('/')).status, '405 METHOD NOT ALLOWED')

    def test_that_post_successful(self):
        headers = {'content-type': 'application/json; charset=utf-8'}
        history_data = '{"title_number": "TEST1412258807231" }'
        app.logger.info(history_data)
        app.logger.info(json.dumps(history_data, encoding='utf-8'))
        res = self.app.post('/TEST1412853022495', data=history_data, headers=headers)
        self.assertEqual(res.status, '200 OK')

    def test_that_get_list_successful(self):
        self.assertEqual((self.app.get('/TEST1412853022495?version=list')).status, '200 OK')
        data = json.loads(self.app.get('/TEST1412853022495?version=list').data)
        self.assertEqual(json.dumps(data, encoding='utf-8'), '{"versions": []}')

    def test_that_get_version_successful(self):
        self.assertEqual((self.app.get('/TEST1412853022495?version=0')).status, '404 NOT FOUND')
