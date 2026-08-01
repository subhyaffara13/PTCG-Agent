
def _resolve_auto_map_class_ref(auto_map, backend):
    """Extract the class reference string from an auto_map entry based on backend preference.

    Returns:
        A string that may be:
        - A simple class name (e.g. `"MyImageProcessor"`)
        - A Hub reference in the form `upstream_repo--path/to/file.py::ClassName`, where the part before
          `--` is the upstream repo ID (used for trust_remote_code resolution).
    """
    if isinstance(auto_map, dict):
        return auto_map.get(backend) or next(iter(auto_map.values()))
    if isinstance(auto_map, (list, tuple)):
        if backend == "torchvision" and len(auto_map) > 1 and auto_map[1] is not None:
            return auto_map[1]
        return auto_map[0]
    # Single string (legacy)
    return auto_map

