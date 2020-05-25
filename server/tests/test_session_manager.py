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
        self.session_manager.create_new_session()

    def test_terminate_session(self):
        session_id = self.session_manager.create_new_session()

        self.session_manager.terminate_session(session_id)

        with self.assertRaises(ValueError):
            self.session_manager.terminate_session(-1)

    def test_add_request_to_history(self):
        session_id = self.session_manager.create_new_session()

        self.session_manager.add_request_to_history(session_id, Request(
            Request.Type.generate,
            CodeType.QR,
            'jabka'
        ))

    def test_clear_session_history(self):
        session_id = self.session_manager.create_new_session()

        self.session_manager.add_request_to_history(session_id, Request(
            Request.Type.generate,
            CodeType.QR,
            'jabka'
        ))
        history = self.session_manager.session_history(session_id)
        self.assertNotEqual(history, '')

        self.session_manager.clear_session_history(session_id)

        history = self.session_manager.session_history(session_id)
        self.assertEqual(history, '')


if __name__ == '__main__':
    unittest.main()
