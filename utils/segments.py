
def segments(snapshot, format_flamegraph=format_flamegraph):
    f = io.StringIO()
    for seg in snapshot["segments"]:
        prefix = f"stream_{seg['stream']};seg_{seg['address']}"
        _write_blocks(f, prefix, seg["blocks"])
    return format_flamegraph(f.getvalue())

