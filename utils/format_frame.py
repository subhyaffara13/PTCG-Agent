
def format_frame(frame, *, base=None, line=False) -> str:
    """
    Format a FrameSummary in a short way, without printing full absolute path or code.

    The idea is the result fits on a single line.
    """
    extra_line = ""
    if line:
        extra_line = f"{frame.line}  # "
    return f"{extra_line}{shorten_filename(frame.filename, base=base)}:{frame.lineno} in {frame.name}"


def format_frame(frame: dict[str, str]) -> str:
    name = frame["name"]
    filename = frame["filename"]
    line = frame["line"]
    return f"{name} at {filename}:{line}"

