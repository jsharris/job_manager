__author__ = 'jon'

# make available all the common modules
import sys
sys.path.append('../libs')

import requests
import ujson
import unittest
import logging


def build_logging():
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    fh = logging.FileHandler('job_manager.log')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter(' %(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    log.addHandler(fh)


class TestJobManagerAPI(unittest.TestCase):
    def setUp(self):
        # This also covers the case of successfully setting up a job
        self.base_url = 'http://localhost:9989'
        self.email = 'myemail@mydomain.com'
        self.job_type = 'Sample'
        self.notify = False
        self.auth_key = 'makeThisHardToGuess'
        self.job = None

        build_logging()
        # log = logging.getLogger()

        url = '%s/new' % self.base_url
        params = {'email': self.email, 'job_type': self.job_type, 'notify': self.notify}
        results = self._call_api_url(url, params)
        self.assertEqual(results['status'], 'Success')
        self.job = results['data']['job_id']

    def tearDown(self):
        # This also covers the case of successfully purging a job
        if self.job is not None:
            url = '%s/purge' % self.base_url
            params = {'id': self.job, 'auth_key': self.auth_key}
            results = self._call_api_url(url, params)
            self.assertEqual(results['status'], 'Success')

    def _call_api_url(self, url, params=None):
        print ("params: ", params)
        session = requests.Session()
        resp = session.get(url, params=params)
        print "resp: ", resp.text
        return ujson.loads(resp.text)

    #
    # Test functions for the "new" action
    #
    def test_new_failure_missing_email(self):
        url = '%s/new' % self.base_url
        params = {'notify': self.notify, 'job_type': self.job_type}
        results = self._call_api_url(url, params)
        self.assertEqual(results['status'], 'Failure')
        self.assertIn("['email']", results['message'])

    def test_new_failure_missing_job_type(self):
        url = '%s/new' % self.base_url
        params = {'notify': self.notify, 'email': self.email}
        results = self._call_api_url(url, params)
        self.assertEqual(results['status'], 'Failure')
        self.assertIn("['job_type']", results['message'])

    def test_new_failure_missing_notify(self):
        url = '%s/new' % self.base_url
        params = {'email': self.email, 'job_type': self.job_type}
        results = self._call_api_url(url, params)
        self.assertEqual(results['status'], 'Failure')
        self.assertIn("['notify']", results['message'])

    def test_new_failure_bad_job_type(self):
        url = '%s/new' % self.base_url
        params = {'email': self.email, 'job_type': 'bogus', 'notify': self.notify}
        results = self._call_api_url(url, params)
        self.assertEqual(results['status'], 'Failure')
        self.assertIn('job_type', results['message'])

    #
    # Test functions for the "status" action
    #
    def test_status_success_by_id(self):
        url = '%s/status' % self.base_url
        params = {'id': self.job}
        results = self._call_api_url(url, params)
        self.assertEqual(results['status'], 'Success')
        self.assertEqual(results['data'][0]['job_type'], self.job_type)
        self.assertEqual(results['data'][0]['email'], self.email)
        self.assertEqual(results['data'][0]['notify'], self.notify)
        self.assertEqual(results['data'][0]['percentage'], 0)
        self.assertEqual(results['data'][0]['id'], self.job)

    def test_status_success_by_email(self):
        url = '%s/status' % self.base_url
        params = {'email': self.email}
        results = self._call_api_url(url, params)
        self.assertEqual(results['status'], 'Success')
        self.assertGreater(len(results['data']), 0)

    def test_status_failure_bad_id(self):
        url = '%s/status' % self.base_url
        params = {'id': -1}
        results = self._call_api_url(url, params)
        self.assertEqual(results['status'], 'Failure')
        self.assertIn("Unable to find job", results['message'])

    def test_status_failure_bad_email(self):
        url = '%s/status' % self.base_url
        params = {'email': 'nobody@home'}
        results = self._call_api_url(url, params)
        self.assertEqual(results['status'], 'Failure')
        self.assertIn("Unable to find job", results['message'])

    #
    # Test functions for the "update" action
    #
    def test_update_failure_bad_id(self):
        url = '%s/update' % self.base_url
        params = {'id': -1, 'percentage': 50}
        results = self._call_api_url(url, params)
        self.assertEqual(results['status'], 'Failure')

    def test_update_failure_bad_percentage_low(self):
        url = '%s/update' % self.base_url
        params = {'id': self.job, 'percentage': -1}
        results = self._call_api_url(url, params)
        self.assertEqual(results['status'], 'Failure')
        self.assertEqual(results['message'], 'Percentage not between 0 and 100')

    def test_update_failure_bad_percentage_high(self):
        url = '%s/update' % self.base_url
        params = {'id': self.job, 'percentage': 200}
        results = self._call_api_url(url, params)
        self.assertEqual(results['status'], 'Failure')
        self.assertEqual(results['message'], 'Percentage not between 0 and 100')

    def test_update_success(self):
        url = '%s/update' % self.base_url
        params = {'id': self.job, 'percentage': 50}
        results = self._call_api_url(url, params)
        self.assertEqual(results['status'], 'Success')
        # check update really happened
        url = '%s/status' % self.base_url
        params = {'id': self.job}
        results = self._call_api_url(url, params)
        self.assertEqual(results['data'][0]['percentage'], 50)

    #
    # Test functions for "completed" action
    #
    def test_complete_failure_bad_id(self):
        url = '%s/completed' % self.base_url
        params = {'id': -1, 'message': 'completed'}
        results = self._call_api_url(url, params)
        self.assertEqual(results['status'], 'Failure')

    def test_complete_failure_missing_id(self):
        url = '%s/completed' % self.base_url
        params = {'message': 'completed'}
        results = self._call_api_url(url, params)
        self.assertEqual(results['status'], 'Failure')
        self.assertIn("['id']", results['message'])

    def test_complete_failure_missing_message(self):
        url = '%s/completed' % self.base_url
        params = {'id': self.job}
        results = self._call_api_url(url, params)
        self.assertEqual(results['status'], 'Failure')
        self.assertIn("['message']", results['message'])

    def test_complete_success(self):
        url = '%s/completed' % self.base_url
        params = {'id': self.job, 'message': 'completed'}
        results = self._call_api_url(url, params)
        self.assertEqual(results['status'], 'Success')

    def test_complete_success_with_email(self):
        url = '%s/flip_notify' % self.base_url
        params = {'id': self.job, 'notify': True}
        results = self._call_api_url(url, params)
        self.assertEqual(results['status'], 'Success', msg='Unable to turn on notification')
        url = '%s/completed' % self.base_url
        msg = ['Test Framework', 'Test is Completed']
        params = {'id': self.job, 'message': msg}
        # params = {'id': self.job, 'message': ['Test Framework', 'Test is Completed']}
        results = self._call_api_url(url, params)
        # self.assertEqual(results['status'], 'Failure')
        self.assertEqual(results['status'], 'Success')

    #
    # Test Functions for "error" action
    #
    def test_error_failure_missing_id(self):
        url = '%s/error' % self.base_url
        params = {'message': 'completed'}
        results = self._call_api_url(url, params)
        self.assertEqual(results['status'], 'Failure')
        self.assertIn("['id']", results['message'])

    def test_error_failure_missing_message(self):
        url = '%s/error' % self.base_url
        params = {'id': self.job}
        results = self._call_api_url(url, params)
        self.assertEqual(results['status'], 'Failure')
        self.assertIn("['message']", results['message'])

    def test_error_success(self):
        url = '%s/error' % self.base_url
        params = {'id': self.job, 'message': 'error'}
        results = self._call_api_url(url, params)
        self.assertEqual(results['status'], 'Success')

    #
    # Test Functions for "delete" action
    #
    def test_delete_failure_missing_id(self):
        url = '%s/delete' % self.base_url
        params = {'message': 'delete'}
        results = self._call_api_url(url, params)
        self.assertEqual(results['status'], 'Failure')
        self.assertIn("['id']", results['message'])

    def test_delete_failure_missing_message(self):
        url = '%s/delete' % self.base_url
        params = {'id': self.job}
        results = self._call_api_url(url, params)
        self.assertEqual(results['status'], 'Failure')
        self.assertIn("['message']", results['message'])

    def test_delete_success(self):
        url = '%s/delete' % self.base_url
        params = {'id': self.job, 'message': 'delete'}
        results = self._call_api_url(url, params)
        self.assertEqual(results['status'], 'Success')

if __name__ == '__main__':
    unittest.main()
