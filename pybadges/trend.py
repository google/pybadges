from typing import Optional, List, Tuple

import drawSvg as draw
import itertools
import numpy as np

import pybadges

HEIGHT = 13
WIDTH = 110
X_OFFSET = 7
Y_OFFSET = 1


def normalize(arr: np.ndarray) -> np.ndarray:
    max_arr = np.max(arr)
    if max_arr != 0:
        arr /= max_arr
    return arr


def repeat(samples: List[int], n: int) -> List[int]:
    """Repeats a value n times in an array.

    Args:
        samples: The list of all elements to be repeated.
        n: Number of times to repeat each element in samples.
    """
    return list(
        itertools.chain.from_iterable(
            itertools.repeat(sample, n) for sample in samples))


def fit_data(samples: List[int]) -> Tuple[List[int], List[int]]:
    y = list(
        itertools.chain.from_iterable(
            itertools.repeat(sample, 10) for sample in samples))
    xp = np.arange(len(y))
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
    path.M(X_OFFSET + xp[0], yp[0])
    for x, y in zip(xp[1:], yp[1:]):
        path.L(X_OFFSET + x, y)
    canvas.append(path)

    return canvas.asDataUri()
