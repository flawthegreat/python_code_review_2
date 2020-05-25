from enum import Enum
import io
import qrcode
from pyzbar.pyzbar import decode
import barcode
import PIL
import string


class CodeType(Enum):
    QR = 'qr'
    CODE39 = 'code39'
    CODE128 = 'code128'
    EAN = 'ean'


class CodeManager:
    __MAX_DATA_SIZE = 4096

    @staticmethod
    def generate(code_type: CodeType, data: str) -> bytes:
        byte_array = io.BytesIO()

        if code_type == CodeType.QR:
            image = qrcode.make(data)
            image.save(byte_array, format='PNG')
        elif code_type in (CodeType.CODE39, CodeType.CODE128, CodeType.EAN):
            code = barcode.get_barcode_class(code_type.value)
            image = code(data, writer=barcode.writer.ImageWriter())
            image.write(byte_array)
        else:
            raise NotImplementedError(f'Unsupported code type: {code_type}')

        return byte_array.getvalue()

    @staticmethod
    def read(image_data: bytes) -> str:
        try:
            decoded_data = decode(
                PIL.Image.open(io.BytesIO(image_data))
            )[0].data

            return str(decoded_data, encoding='utf-8')
        except:
            return ''

    @classmethod
    def data_is_correct(cls, code_type: CodeType, data: str) -> bool:
        if len(data) > cls.__MAX_DATA_SIZE:
            return False

        if code_type in (CodeType.QR, CodeType.CODE128):
            for char in data:
                if char not in string.printable:
                    return False

            return True
        elif code_type == CodeType.CODE39:
            return set(data).issubset(set(
                string.ascii_uppercase +
                string.digits +
                '-.$/+% '
            ))
        elif code_type == CodeType.EAN:
            return set(data).issubset(set(string.digits)) and len(data) == 12
        else:
            raise NotImplementedError(f'Unsupported code type: {code_type}')
