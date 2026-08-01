
def _adjust_range_header(original_range: str | None, resume_size: int) -> str | None:
    """
    Adjust HTTP Range header to account for resume position.
    """
    if not original_range:
        return f"bytes={resume_size}-"

    if "," in original_range:
        raise ValueError(f"Multiple ranges detected - {original_range!r}, not supported yet.")

    match = RANGE_REGEX.match(original_range)
    if not match:
        raise RuntimeError(f"Invalid range format - {original_range!r}.")
    start, end = match.groups()

    if not start:
        if not end:
            raise RuntimeError(f"Invalid range format - {original_range!r}.")

        new_suffix = int(end) - resume_size
        new_range = f"bytes=-{new_suffix}"
        if new_suffix <= 0:
            raise RuntimeError(f"Empty new range - {new_range!r}.")
        return new_range

    start = int(start)
    new_start = start + resume_size
    if end:
        end = int(end)
        new_range = f"bytes={new_start}-{end}"
        if new_start > end:
            raise RuntimeError(f"Empty new range - {new_range!r}.")
        return new_range

    return f"bytes={new_start}-"

