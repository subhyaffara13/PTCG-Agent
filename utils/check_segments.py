
def check_segments(coll, positions, linelength, lineoffset, orientation):
    """
    Test helper checking that all values in the segment are correct, given a
    particular set of inputs.
    """
    segments = coll.get_segments()
    if (orientation.lower() == 'horizontal'
            or orientation.lower() == 'none' or orientation is None):
        # if horizontal, the position in is in the y-axis
        pos1 = 1
        pos2 = 0
    elif orientation.lower() == 'vertical':
        # if vertical, the position in is in the x-axis
        pos1 = 0
        pos2 = 1
    else:
        raise ValueError("orientation must be 'horizontal' or 'vertical'")

    # test to make sure each segment is correct
    for i, segment in enumerate(segments):
        assert segment[0, pos1] == lineoffset + linelength / 2
        assert segment[1, pos1] == lineoffset - linelength / 2
        assert segment[0, pos2] == positions[i]
        assert segment[1, pos2] == positions[i]

