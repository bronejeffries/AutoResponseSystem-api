# Import QR Code library
import os
import qrcode


class GenerateQrCode(object):
    """docstring for GenerateQrCode."""

    def __init__(self, data, name):
        self.data = data
        self.name = name
        self.generateqr(self.data, self.name)

    def generateqr(self, data, name):
        qr = qrcode.QRCode(version=1,
                           error_correction=qrcode.constants.ERROR_CORRECT_H,
                           box_size=10,
                           border=4)

# # Add data
        qr.add_data(data)
        qr.make(fit=True)

# # Create an image from the QR Code instance
        img = qr.make_image()
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        storage_path = os.path.join(BASE_DIR, 'media/qrcodes')

# # Save it somewhere, change the extension as needed:
        img.save(os.path.join(storage_path, name + ".png"))
        print("DONE")
        return qr
