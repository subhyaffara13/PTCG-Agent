import math


def _alignment_transformation(segment):
    # Returns a transformation which aligns a segment horizontally at the
    # origin. Apply this transformation to curves and root-find to find
    # intersections with the segment.
    start = segment[0]
    end = segment[-1]
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    return Identity.rotate(-angle).translate(-start[0], -start[1])

