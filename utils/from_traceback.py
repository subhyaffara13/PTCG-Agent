
def from_traceback(tb: Sequence[traceback.FrameSummary]) -> list[dict[str, Any]]:
    # dict naming convention here coincides with
    # python/combined_traceback.cpp
    r = [
        {
            "line": frame.lineno,
            "name": frame.name,
            "filename": intern_string(frame.filename),
            "loc": frame.line,
        }
        for frame in tb
    ]
    return r

