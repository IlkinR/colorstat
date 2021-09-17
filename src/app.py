import io
import string
import re
from fastapi import FastAPI, File, UploadFile
from PIL import Image
from services import count_black_and_white, count_color

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
    image_extensions = (".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif")
    if not image.filename.endswith(image_extensions):
        return {"file": image.filename, "reason": "File should be image"}

    image_bytes = io.BytesIO(image.file.read())
    image_file = Image.open(image_bytes).convert("RGB")
    color_count = int(count_color(image_file, searched_color))

    return {"color": searched_color, "count": color_count}
