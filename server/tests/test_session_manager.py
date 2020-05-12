import os
import sys
import inspect
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())
)))
sys.path.insert(0, parentdir) 

import unittest
from session_manager import Request, SessionManager
from code_manager import CodeType


class TestSessionManager(unittest.TestCase):
    def setUp(self):
        self.session_manager = SessionManager()

    def test_create_new_session(self):
        try:
            self.session_manager.create_new_session()
        except:
            self.assertTrue(False, 'Could not create session')

    def test_terminate_session(self):
        session_id = self.session_manager.create_new_session()
        try:
            self.session_manager.terminate_session(session_id)
        except:
            self.assertTrue(False, 'Could not terminate session')

        with self.assertRaises(ValueError):
            self.session_manager.terminate_session(-1)

    def test_add_request_to_history(self):
        session_id = self.session_manager.create_new_session()
        try:
            self.session_manager.add_request_to_history(session_id, Request(
                Request.Type.generate,
                CodeType.qr,
                'jabka'
            ))
        except:
            self.assertTrue(False, 'Could not update history')

    def test_session_history(self):
        session_id = self.session_manager.create_new_session()
        try:
            history = self.session_manager.session_history(session_id)
            self.assertEqual(history, '')

            self.session_manager.add_request_to_history(session_id, Request(
                Request.Type.generate,
                CodeType.qr,
                'jabka'
            ))
            history = self.session_manager.session_history(session_id)
            self.assertNotEqual(history, '')
        except:
            self.assertTrue(False, 'Could not get session history')

    def test_clear_session_history(self):
        session_id = self.session_manager.create_new_session()
        try:
            self.session_manager.add_request_to_history(session_id, Request(
                Request.Type.generate,
                CodeType.qr,
                'jabka'
            ))
            history = self.session_manager.session_history(session_id)
            self.assertNotEqual(history, '')

            self.session_manager.clear_session_history(session_id)

            history = self.session_manager.session_history(session_id)
            self.assertEqual(history, '')
        except:
            self.assertTrue(False, 'Could not clear history')


if __name__ == '__main__':
    unittest.main()
