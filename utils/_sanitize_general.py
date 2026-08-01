
def _sanitize_general(s):
    s = s.strip()
    s = s.replace("pybind11_tests.", "m.")
    return _long_marker.sub(r"\1", s)

