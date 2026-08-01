
def series_via_frame_from_scalar(x, **kwargs):
    return DataFrame(x, **kwargs)[0]

