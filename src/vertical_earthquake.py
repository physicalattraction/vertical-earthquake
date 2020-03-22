import os.path
import random
from datetime import datetime
from time import sleep
from typing import List

from PIL import Image, ImageDraw

from config import *


def now() -> str:
    """
    Return the current date and timestamp in second precision
    """

    return datetime.now().strftime('%y%m%d%H%M%S')


class VerticalEarthquake:
    src_dir = os.path.dirname(__file__)
    root_dir = os.path.dirname(src_dir)
    img_dir = os.path.join(root_dir, 'img')

    width: int
    height: int
    img: Image
    draw: ImageDraw

    def __init__(self):
        self.width = 2000
        self.height = self.width
        self.img = Image.new('RGB', (self.width, self.height), 'white')
        self.draw = ImageDraw.Draw(self.img)

    @staticmethod
    def draw_multiple_quakes(nr_quakes: int):
        for _ in range(nr_quakes):
            start_time = now()
            vertical_earthquake = VerticalEarthquake()
            quake = vertical_earthquake.get_quake()
            vertical_earthquake.draw_quake(quake)
            vertical_earthquake.save_img()
            while now() == start_time:
                # Since we have seconds in the filename, we shouldn't continue
                # drawing the next earthquake until the second is over
                sleep(0.01)

    def get_quake(self) -> List[complex]:
        """
        Determine a quake which is visually pleasing
        """

        points = [0]  # We start from the center (0, 0)
        for _ in range(NR_SEGMENTS):
            last_point = points[-1]
            penultimate_point = points[-2] if len(points) > 1 else None
            next_point = self._get_next_point(last_point, penultimate_point)
            points.append(next_point)
        return points

    def draw_quake(self, quake: List[complex]):
        """
        Draw the quake and its mirror lines
        """

        for index in range(-NR_MIRROR_LINES, NR_MIRROR_LINES):
            if index == 0:
                width = FAT_WIDTH
                nodes = quake
            else:
                width = THIN_WIDTH
                phi_shift = END_ANGLE_MIRROR_LINES * index / NR_MIRROR_LINES
                nodes = [self._get_shifted_point(p, phi_shift) for p in quake]
            self._draw_line_segments(nodes, width)

    def save_img(self):
        """
        Save the image to the image directory with a predefined filename, based on the current timestamp
        """

        self.img = self.img.rotate(270)
        filename = f'amorales_{now()}.png'
        full_path = os.path.join(self.img_dir, filename)
        self.img.save(full_path)

    def _get_next_point(self, last_point: complex, penultimate_point: complex = None) -> complex:
        """
        Given the last point and optionally the penultimate point, determine a visually pleasing next point

        Criteria:
        - The first segment should point right (i.e. between -45 and 45 degrees)
        - Segments should be almost perpendicular (i.e. between 60 and 120 degrees w.r.t. the previous angle)
        - Segments can "turn left" or "turn right" (i.e. be either positive or negative w.r.t. the previous angle)
        - Segments should always point (almost) towards the right (i.e. between -120 and 120 degrees)
        """

        r = random.uniform(MIN_SEGMENT_LENGTH, MAX_SEGMENT_LENGTH)

        if penultimate_point:
            previous_phi = cmath.phase(penultimate_point - last_point)
            phi = self._get_next_angle(previous_phi)
        else:
            # The first segment should point right (i.e. between -45 and 45 degrees)
            phi = random.uniform(-MAX_FIRST_ANGLE, MAX_FIRST_ANGLE)

        return last_point + cmath.rect(r, phi)

    def _get_next_angle(self, previous_phi: float) -> float:
        """
        Given the previous angle, determine a visually pleasing next angle
        """

        # Segments should be almost perpendicular (i.e. between 60 and 120 degrees w.r.t. the previous angle)
        phi_shift = random.uniform(cmath.pi / 2 - MAX_DEVIATION_FROM_PERPENDICULAR,
                                   cmath.pi / 2 + MAX_DEVIATION_FROM_PERPENDICULAR)

        # Segments can "turn left" or "turn right" (i.e. be either positive or negative w.r.t. the previous angle)
        sign = random.sample([1, -1], 1)[0]

        phi = previous_phi + sign * phi_shift

        # Segments should always point (almost) towards the right (i.e. between -120 and 120 degrees)
        if not -MAX_DEVIATION_FROM_GOING_RIGHT < phi < MAX_DEVIATION_FROM_GOING_RIGHT:
            # If the new angle would point too much towards the left, try again
            phi = self._get_next_angle(previous_phi)

        return phi

    def _draw_line_segments(self, nodes: [complex], width: int):
        """
        Draw the given nodes with the given width

        Note: We shift the nodes first, such that point (0,0) coincides with the center of the canvas
        """

        nodes = [n + complex(self.width / 2, self.height / 2) for n in nodes]
        nodes = [(n.real, n.imag) for n in nodes]
        self.draw.line(nodes, fill='black', width=width)

    @staticmethod
    def _get_shifted_point(point: complex, phi_shift: float) -> complex:
        """
        Given a complex point, return the complex point shifted by the given angle (in radians)
        """

        r, phi = cmath.polar(point)
        return cmath.rect(r, phi + phi_shift)


if __name__ == '__main__':
    VerticalEarthquake.draw_multiple_quakes(1)
