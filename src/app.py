import io
import re

from fastapi import FastAPI, File, UploadFile
from PIL import Image, ImageColor

from colors import count_black_and_white, count_color

HEX_COLOR_PATTERN = re.compile("^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")

api = FastAPI()


@api.post("/dominant_color/")
def find_dominant_color(image: UploadFile = File(...)):
    image_extensions = (".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif")
    if not image.filename.endswith(image_extensions):
        return {"result": "fail", "reason": "File should be image"}

    image_bytes = io.BytesIO(image.file.read())
    image_file = Image.open(image_bytes).convert("RGB")
    blacks, whites = map(int, count_black_and_white(image_file))

    dominant_color = "black" if blacks > whites else "white"
    dominant_count = blacks if blacks > whites else whites
    return {"color": dominant_color, "count": dominant_count}


@api.post("/count_color/")
def get_color_count(searched_color: str, image: UploadFile = File(...)):
    is_hex = re.search(HEX_COLOR_PATTERN, searched_color)
    if is_hex is None:
        return {"result": "fail", "reason": "Color should be heximal!"}

    image_extensions = (".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif")
    if not image.filename.endswith(image_extensions):
        return {"result": "fail", "reason": "File type must be image!"}

    image_bytes = io.BytesIO(image.file.read())
    image_file = Image.open(image_bytes).convert("RGB")
    color_count = int(count_color(image_file, searched_color))
    return {"color": searched_color, "count": color_count}
