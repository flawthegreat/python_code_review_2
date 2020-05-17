import os
import sys
import inspect
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())
)))
sys.path.insert(0, parentdir) 

import unittest
from code_manager import CodeType, CodeManager
import io
import string
import PIL


class TestCodeManager(unittest.TestCase):
    def test_generate(self):
        for code_type, data in zip(
            [CodeType.QR, CodeType.CODE39, CodeType.CODE128, CodeType.EAN],
            ['jabka', 'JABKA', 'small jabka', '012345678901']
        ):
            image_data = CodeManager.generate(code_type, data)
            self.assertEqual(
                PIL.Image.open(io.BytesIO(image_data)).format,
                'PNG'
            )

    def test_read(self):
        for image_file, data in zip(
            ['test_qr.png', 'test_code39.png', 'test_code128.png',
                'test_ean.png'],
            ['jabka', 'JABKAR', 'big jabka', '1875904582766']
        ):
            with open(image_file, 'rb') as image_data:
                self.assertEqual(CodeManager.read(image_data.read()), data)

        self.assertEqual(CodeManager.read(b'stupid data'), '')

    def test_coding_correctness(self):
        for code_type, data in zip(
            [CodeType.QR, CodeType.CODE39, CodeType.CODE128, CodeType.EAN],
            ['jabka', 'JABKA', 'huge jabka', '012345678901']
        ):
            image_data = CodeManager.generate(code_type, data)
            decoded_data = (
                CodeManager.read(image_data)[:-1]
                if code_type in [CodeType.CODE39, CodeType.EAN] else
                CodeManager.read(image_data)
            )
            self.assertEqual(decoded_data, data)

    def test_data_is_correct(self):
        for code_type, data, result in zip(
            [CodeType.QR, CodeType.QR, CodeType.CODE128,
                CodeType.CODE128, CodeType.CODE39, CodeType.CODE39,
                CodeType.CODE39, CodeType.EAN, CodeType.EAN, CodeType.EAN,
                CodeType.EAN],
            [string.printable, 'жабка', string.printable, 'жабка',
                'STUPID CODE1245876-.$/+%' + string.ascii_uppercase,
                'even more stupid code', ':^)', '012345678901', '01234567890',
                '0123456789012', 'abc'],
            [True, False, True, False, True, False, False, True, False, False,
                False]
        ):
            self.assertEqual(
                CodeManager.data_is_correct(code_type, data),
                result
            )


if __name__ == '__main__':
    unittest.main()
