import os
from typing import Tuple

from PIL import Image, ImageColor
import numpy as np

WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)


def count_black_and_white(image) -> Tuple[int, int]:
    image_array = np.array(image).reshape(-1, 3)
    colors, frequencies = np.unique(image_array, axis=0, return_counts=1)
    has_black = (colors == np.array(BLACK_COLOR)).all(1).any()
    has_white = (colors == np.array(WHITE_COLOR)).all(1).any()
    if not has_black or not has_white:
        return (-1, -1)
    blacks, whites = frequencies[0], frequencies[-1]
    return blacks, whites


def count_color(image, color_hex: Tuple[int, int, int]) -> int:
    image_array = np.array(image).reshape(-1, 3)
    colors, frequencies = np.unique(image_array, axis=0, return_counts=1)
    color_rgb = np.array(ImageColor.getrgb(color_hex))
    final_count = -1
    for color, frequency in zip(colors, frequencies):
        if (color == color_rgb).all():
            final_count = frequency
    return final_count
