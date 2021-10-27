from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from PIL import Image
from qrgen import create_qr_code
import random
import argparse
import math

def get_unique_id():
    return random.randint(0, 1e7)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("X", type=int, help="in mm")
    parser.add_argument("Y", type=int, help="in mm")
    parser.add_argument("Z", type=int, help="in mm")
    parser.add_argument("-output", default="qrcodes.pdf", type=str, help="filename of output")
    parser.add_argument("-qrsize", default=2.9, type=float, help="qrcode size in cm")
    parser.add_argument("-between_margin", default=0.5, type=float, help="dist between qrcodes border")
    return parser.parse_args()

args = get_args()

MIN_MM = 60
def encode_mm(mm: int):
    return math.floor((mm-MIN_MM)/5)

A4_X = 21*cm
A4_Y = 29.7*cm

def draw_qr_code(pdf : canvas.Canvas, x: float, y: float, code: Image):
    pdf.setFillColor("black")
    pdf.rect(x*cm, y*cm, args.qrsize*cm, args.qrsize*cm, stroke=1, fill=1)
    pdf.drawInlineImage(code, (x+0.2)*cm, (y+0.2)*cm, width=(args.qrsize - 0.4)*cm, height=(args.qrsize - 0.4)*cm)

def fill_with_codes(pdf, X, Y, Z):
    x = 0.5*cm
    y = 0.5*cm
    while x < A4_X - args.between_margin*cm - args.qrsize*cm:
        while y < A4_Y - args.between_margin*cm - args.qrsize*cm:
            draw_qr_code(pdf, x/cm, y/cm, create_qr_code(encode_mm(X), encode_mm(Y), encode_mm(Z), get_unique_id()))
            y += args.qrsize*cm + args.between_margin*cm
        y = 0.5*cm
        x += args.qrsize*cm + args.between_margin*cm

documentTitle = "KodyQR"



pdf = canvas.Canvas(args.output)
pdf.setTitle(documentTitle)
pdf.drawString(0, 0, f"X{args.X}mmY{args.Y}mmZ{args.Z}mm")

fill_with_codes(pdf, args.X, args.Y, args.Z)
pdf.save()