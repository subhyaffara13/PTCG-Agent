
def _move_overlapping_to_stream(
    trace: dict, default_stream: int = 7, overlap_stream: int = 8
) -> int:
    """Move graphed kernels that overlap with their predecessor to a separate stream.

    Perfetto cannot display overlapping (non-nested) events on the same
    stream -- they get hidden.  This pass detects graphed kernel events on
    *default_stream* whose start timestamp falls before the previous
    kernel's end, and moves them to *overlap_stream* so they're visible.

    Returns the number of events moved.
    """
    graphed_on_default = [
        e
        for e in trace["traceEvents"]
        if e.get("cat") == "kernel"
        and e.get("tid") == default_stream
        and e.get("args", {}).get("graph node id", 0) != 0
    ]
    graphed_on_default.sort(key=lambda e: e["ts"])

    moved = 0
    prev_end = 0.0
    for event in graphed_on_default:
        ts = event["ts"]
        dur = event.get("dur", 0)
        if ts < prev_end:
            event["tid"] = overlap_stream
            event.get("args", {})["stream"] = overlap_stream
            moved += 1
        else:
            prev_end = ts + dur

    return moved

