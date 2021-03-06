import json
import responses
from base import BaseAPITest
from test_scan import INDEX_RESPONSE, VERSION_RESPONSE

from w3af_api_client import Connection


SCAN_LIST_RESPONSE = json.dumps({'items': [{'id': 0,
                                            'href': '/scans/0',
                                            'target_urls': [''],
                                            'status': 'Running',
                                            'errors': True},

                                           {'id': 1,
                                            'href': '/scans/1',
                                            'target_urls': [''],
                                            'status': 'Stopped',
                                            'errors': False}
                                           ]})


class TestScanListClient(BaseAPITest):

    @responses.activate
    def test_scan_list(self):
        responses.add(responses.GET,
                               self.get_url('/'),
                               body=INDEX_RESPONSE,
                               content_type='application/json')

        responses.add(responses.GET,
                               self.get_url('/version'),
                               body=VERSION_RESPONSE,
                               content_type='application/json')

        responses.add(responses.GET,
                               self.get_url('/scans/'),
                               body=SCAN_LIST_RESPONSE,
                               content_type='application/json')

        conn = Connection(self.api_url)

        scans = conn.get_scans()
        self.assertEqual([s.status for s in scans], ['Running', 'Stopped'])
        self.assertEqual([s.scan_id for s in scans], [0, 1])
