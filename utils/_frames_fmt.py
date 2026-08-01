
def _frames_fmt(frames, full_filename=False, reverse=False):
    if reverse:
        frames = reversed(frames)
    return [
        _frame_fmt(f, full_filename)
        for f in frames
        if _frame_filter(f["name"], f["filename"])
    ]

