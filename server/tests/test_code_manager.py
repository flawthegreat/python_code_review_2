import os
import sys
import inspect
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())
)))
sys.path.insert(0, parentdir) 

import unittest
from code_manager import CodeType, CodeManager
import string
import PIL
import io


class TestCodeManager(unittest.TestCase):
    def test_generate(self):
        image_data = CodeManager.generate(CodeType.qr, 'jabka')
        self.assertEqual(PIL.Image.open(io.BytesIO(image_data)).format, 'PNG')

        image_data = CodeManager.generate(CodeType.code39, 'JABKA')
        self.assertEqual(PIL.Image.open(io.BytesIO(image_data)).format, 'PNG')

        image_data = CodeManager.generate(CodeType.code128, 'small jabka')
        self.assertEqual(PIL.Image.open(io.BytesIO(image_data)).format, 'PNG')

        image_data = CodeManager.generate(CodeType.ean, '012345678901')
        self.assertEqual(PIL.Image.open(io.BytesIO(image_data)).format, 'PNG')

    def test_read(self):
        with open('test_qr.png', 'rb') as image_data:
            self.assertEqual(CodeManager.read(image_data.read()), 'jabka')

        with open('test_code39.png', 'rb') as image_data:
            self.assertEqual(CodeManager.read(image_data.read()), 'JABKAR')

        with open('test_code128.png', 'rb') as image_data:
            self.assertEqual(CodeManager.read(image_data.read()), 'big jabka')

        with open('test_ean.png', 'rb') as image_data:
            self.assertEqual(CodeManager.read(image_data.read()), '1875904582766')

        self.assertEqual(CodeManager.read(b'stupid data'), '')

    def test_data_is_correct(self):
        self.assertTrue(CodeManager.data_is_correct(
            CodeType.qr,
            string.printable
        ))
        self.assertFalse(CodeManager.data_is_correct(
            CodeType.qr,
            'жабка'
        ))

        self.assertTrue(CodeManager.data_is_correct(
            CodeType.code128,
            string.printable
        ))
        self.assertFalse(CodeManager.data_is_correct(
            CodeType.code128,
            'жабка'
        ))

        self.assertTrue(CodeManager.data_is_correct(
            CodeType.code39,
            'STUPID CODE1245876-.$/+%' + string.ascii_uppercase
        ))
        self.assertFalse(CodeManager.data_is_correct(
            CodeType.code39,
            'even more stupid code'
        ))
        self.assertFalse(CodeManager.data_is_correct(
            CodeType.code39,
            ':^)'
        ))

        self.assertTrue(CodeManager.data_is_correct(
            CodeType.ean,
            '012345678901'
        ))
        self.assertFalse(CodeManager.data_is_correct(
            CodeType.ean,
            '01234567890'
        ))
        self.assertFalse(CodeManager.data_is_correct(
            CodeType.ean,
            '0123456789012'
        ))
        self.assertFalse(CodeManager.data_is_correct(
            CodeType.ean,
            'abc'
        ))


if __name__ == '__main__':
    unittest.main()
