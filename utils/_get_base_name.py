
def _get_base_name(trace_path: str) -> str:
    """Get the base name of a trace file, stripping known extensions."""
    base_name = os.path.basename(trace_path)
    for ext in [".trace.json.gz", ".chrome_trace", ".json.gz", ".json"]:
        if base_name.endswith(ext):
            return base_name[: -len(ext)]
    return os.path.splitext(base_name)[0]

