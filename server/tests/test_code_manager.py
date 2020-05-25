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
        for code_type, data in [
            (CodeType.QR, 'jabka'), (CodeType.CODE39, 'JABKA'),
            (CodeType.CODE128, 'small jabka'), (CodeType.EAN, '012345678901')
        ]:
            image_data = io.BytesIO(CodeManager.generate(code_type, data))
            self.assertEqual(PIL.Image.open(image_data).format, 'PNG')

    def test_read(self):
        for image_file, data in [
            ('test_qr.png', 'jabka'), ('test_code39.png', 'JABKAR'),
            ('test_code128.png', 'big jabka'), ('test_ean.png', '1875904582766')
        ]:
            with open(image_file, 'rb') as image_data:
                self.assertEqual(CodeManager.read(image_data.read()), data)

        self.assertEqual(CodeManager.read(b'stupid data'), '')

    def test_coding_correctness(self):
        for code_type, data in [
            (CodeType.QR, 'jabka'), (CodeType.CODE39, 'JABKA'),
            (CodeType.CODE128, 'huge jabka'), (CodeType.EAN, '012345678901')
        ]:
            image_data = CodeManager.generate(code_type, data)
            decoded_data = (
                CodeManager.read(image_data)[:-1]
                if code_type in [CodeType.CODE39, CodeType.EAN] else
                CodeManager.read(image_data)
            )
            self.assertEqual(decoded_data, data)

    def test_data_is_correct(self):
        for code_type, data, result in [
            (CodeType.QR, string.printable, True),
            (CodeType.QR, 'жабка', False),
            (CodeType.CODE128, string.printable, True),
            (CodeType.CODE128, 'жабка', False),
            (
                CodeType.CODE39,
                'STUPID CODE1245876-.$/+%' + string.ascii_uppercase,
                True    
            ),
            (CodeType.CODE39, 'even more stupid code', False),
            (CodeType.CODE39, ':^)', False),
            (CodeType.EAN, '012345678901', True),
            (CodeType.EAN, '01234567890', False),
            (CodeType.EAN, '0123456789012', False),
            (CodeType.EAN, 'abc', False)
        ]:
            self.assertEqual(
                CodeManager.data_is_correct(code_type, data),
                result
            )


if __name__ == '__main__':
    unittest.main()
