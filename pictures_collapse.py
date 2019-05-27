from PIL import Image
import os


def collapse_image(main_image, additional_image, cords):

    image_main = Image.open(main_image)
    image_additional = Image.open(additional_image)

    image_main.paste(image_additional, cords)

    if os.path.isfile('./Pictures/meme_out_image/out.jpg'):

        os.remove('./Pictures/meme_out_image/out.jpg')

    image_main.save("./Pictures/meme_out_image/out.jpg")

    del image_additional

    return image_main
