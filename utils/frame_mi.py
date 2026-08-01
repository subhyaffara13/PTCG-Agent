
def frame_mi(frame):
    frame.index = MultiIndex.from_product([range(5), range(2)])
    return frame

