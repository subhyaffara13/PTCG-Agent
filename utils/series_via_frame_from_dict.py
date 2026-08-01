
def series_via_frame_from_dict(x, **kwargs):
    return DataFrame({"a": x}, **kwargs)["a"]

