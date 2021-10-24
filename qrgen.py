import qrcode
from PIL import Image

QRCode = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=20,
    border=4,
)

def encode_data(X: int, Y: int, Z: int, ID: int):
    if X<10:
        X += 90
    X = str(X).zfill(2)
    Y = str(Y).zfill(2)
    Z = str(Z).zfill(2)
    ID = str(ID).zfill(8)
    data = int(X+Y+Z+ID)
    return data

def create_qr_code(X: int, Y: int, Z: int, ID: int) -> Image:
    data = encode_data(X, Y, Z, ID)
    QRCode.clear()
    QRCode.add_data(data)
    QRCode.make(fit=True)
    return QRCode.make_image(fill_color="black", back_color="white").convert("RGB")

if __name__ == "__main__":
    code: Image = create_qr_code(8, 15, 8, 1)
    code.save("img.png")