"""
Module with all drawing configuration
"""

import cmath

# Number of segments in the metal ruler
NR_SEGMENTS = 16

# Minimum segment length in pixels
MIN_SEGMENT_LENGTH = 20

# Maximum segment length in pixels
MAX_SEGMENT_LENGTH = 100

# Width of the metal ruler, in pixels
FAT_WIDTH = 10

# Width of the pencil strokes, in pixels
THIN_WIDTH = 1

# Maximum angle of the firs segment, to ensure that it starts in more or less the correct direction
MAX_FIRST_ANGLE = cmath.pi / 4  # 45 degrees

# Maximum deviation from a perpendicular angle between two subsequent segments, to ensure a proper zigzag pattern
MAX_DEVIATION_FROM_PERPENDICULAR = cmath.pi / 4  # 30 degrees

# Maximum deviation from the original direction, to ensure that the quake continues going in the proper direction
MAX_DEVIATION_FROM_GOING_RIGHT = 2 * cmath.pi / 3  # 120 degrees

# Number of pencil strokes
NR_MIRROR_LINES = 64

# Angle to which to extend the pencil strokes
END_ANGLE_MIRROR_LINES = 2 * cmath.pi / 3  # 120 degrees
