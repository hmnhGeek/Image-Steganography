import argparse as ap
from steganographer import steganographer
from PIL import Image
import os

parser = ap.ArgumentParser()
parser.add_argument("text", type=str, help="Type the secret message.", nargs="?")
parser.add_argument("-i", "--image", dest='i', type=str, help="Pass image to hold this message.")
parser.add_argument("-e", "--encode", dest='e', action="store_true", help="Pass this to encode.")
parser.add_argument("-d", "--decode", dest='d', action="store_true", help="Pass this to decode image.")
args = parser.parse_args()

if args.text and args.i and args.e:
    loadedImage = Image.open(args.i)
    text_image = steganographer.write_text(args.text, loadedImage.size)

    # save the temp image
    text_image.save("temp.png")
    steganographer.encode("temp.png", args.i)
    os.remove("temp.png")

elif args.d and args.i:
    steganographer.decode(args.i)
