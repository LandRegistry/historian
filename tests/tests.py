import calendar
import datetime
from application import server
from application.storage import MemoryStore, S3Store
import unittest
import json

test_creation_time = calendar.timegm(datetime.datetime.utcnow().timetuple())
the_past = datetime.datetime.now() - datetime.timedelta(days=30)
some_past_timestamp = calendar.timegm(the_past.timetuple())

class ApplicationTestCase(unittest.TestCase):

    def setUp(self):

        server.app.config['TESTING'] = True
        self.app = server.app.test_client()
        #make sure we're running against in memory store
        if type(server.storage) == S3Store:
            server.storage = MemoryStore()
            print "S3 was used, switched to memory store"

    def tearDown(self):
        server.storage.clear()

    def test_empty_store(self):
        response = self.app.get('/titles')
        self.assertEqual(json.loads(response.data),  {'titles': []})

    def test_add_title(self):
        title_number = "TN1234567"
        self.app.post('/titles/last', data=json.dumps(
            {
                "title_number": title_number,
                "address": "The Hovel, Moletown",
                "created_ts": test_creation_time,
                "predecessor": None
            }), content_type='application/json')

        response = self.app.get('/titles/last')

        self.assertEqual(json.loads(response.data), {
                    "title_number": title_number,
                    "address": "The Hovel, Moletown",
                    "created_ts": test_creation_time,
                    "predecessor": None

            })

    def test_get_last_title(self):
        title_number = "TN1234567"

        #create two records
        self.app.post('/titles/last', data=json.dumps(
            {
                "title_number": "ANUMB3R",
                "address": "The Hovel, Moletown",
                "created_ts": some_past_timestamp
            }), content_type='application/json')

        #add another - this will be last now
        self.app.post('/titles/last', data=json.dumps(
            {
                "title_number": title_number,
                "address": "The Palace, Kings Landing",
                "created_ts": test_creation_time
            }), content_type='application/json')

        # get the last record
        response = self.app.get('/titles/last')

        self.assertEqual(json.loads(response.data), {
               "title_number": title_number,
                "address": "The Palace, Kings Landing",
                "created_ts": test_creation_time
        })



if __name__ == '__main__':
    unittest.main()
