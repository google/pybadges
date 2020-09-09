from typing import Optional, List, Tuple

import drawSvg as draw
import numpy as np

import pybadges

HEIGHT = 13
WIDTH = 107
X_OFFSET = 7
Y_OFFSET = 1


def normalize(arr: np.ndarray) -> np.ndarray:
    max_arr = np.max(arr)
    if max_arr != 0:
        arr /= max_arr
    return arr


def fit_data(samples: List[int]) -> Tuple[List[int], List[int]]:
    width = WIDTH - X_OFFSET
    N = int(width / len(samples))
    y = np.repeat(samples, N)
    xp = np.linspace(start=X_OFFSET, stop=width, num=len(y))
    yp = normalize(np.poly1d(np.polyfit(xp, y, 15))(xp))
    yp[yp > 0] *= (HEIGHT - 2)
    return xp, yp


def trend(samples: List[int], stroke_color: str, stroke_width: int) -> str:
    canvas = draw.Drawing(WIDTH, HEIGHT, origin=(0, -Y_OFFSET))
    path = draw.Path(
        fill="transparent",
        stroke=pybadges._NAME_TO_COLOR.get(stroke_color, stroke_color),
        stroke_width=stroke_width,
        stroke_linejoin="round",
    )

    xp, yp = fit_data(samples)
    path.M(xp[0], yp[0])
    for x, y in zip(xp[1:], yp[1:]):
        path.L(x, y)
    canvas.append(path)

    return canvas.asDataUri()
