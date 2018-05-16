from PIL import Image, ImageFont, ImageDraw
import textwrap

def write_text(text_to_write, image_size):
    """Writes text to an RGB image. Automatically line wraps
    text_to_write: the text to write to the image
    """
    image_text = Image.new("RGB", image_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)

    #Text wrapping. Change parameters for different text formatting
    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin,offset), line, font=font)
        offset += 10
    return image_text

def encode(secret_image, master_image):
    """ Encodes a image using LSB algorithm."""
    filename = master_image

    master_image = Image.open(master_image)
    channel = master_image.split()

    red, green, blue = channel[0], channel[1], channel[2]
    width = master_image.size[0]
    height = master_image.size[1]

    # load the secret image as black and white
    bw = Image.open(secret_image).convert('1')
    bw = bw.resize((width, height), Image.ANTIALIAS)

    # load an encoded image
    encoded_image = Image.new("RGB", (width, height))
    pixels = encoded_image.load()

    for i in range(width):
        for j in range(height):
            red_pix = bin(red.getpixel((i, j)))
            old_pix = red.getpixel((i, j))
            encoded_pixel = bin(bw.getpixel((i, j)))

            if encoded_pixel[-1] == '1':
                red_pix = red_pix[:-1] + '1'
            else:
                red_pix = red_pix[:-1] + '0'

            pixels[i, j] = (int(red_pix, 2), green.getpixel((i, j)), blue.getpixel((i, j)))
    encoded_image.save(filename+"encoded.png")

def decode(encoded_image):
    addr = encoded_image
    encoded_image = Image.open(encoded_image)
    red = encoded_image.split()[0]

    width, height = encoded_image.size
    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()

    for i in range(width):
        for j in range(height):
            if bin(red.getpixel((i, j)))[-1] == '0':
                pixels[i, j] = (255, 255, 255)
            else:
                pixels[i, j] = (0, 0, 0)
    decoded_image.save(addr+"decoded.png")

