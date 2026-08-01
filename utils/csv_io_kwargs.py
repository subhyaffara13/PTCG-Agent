
def csv_io_kwargs(mode: str) -> dict[str, Any]:
    """Return keyword arguments to properly open a CSV file
    in the given mode.
    """
    return {"mode": mode, "newline": "", "encoding": "utf-8"}

