import pyaztec
from PIL import Image

def generate_aztec(data, filename):
    aztec = pyaztec.encode(data)
    img = Image.fromarray(aztec)
    img.save(filename)

# Example usage:
# generate_aztec("https://quickaid.com/view/12345", "static/qrcode.png")