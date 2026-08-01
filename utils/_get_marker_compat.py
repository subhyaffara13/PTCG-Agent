
def _get_marker_compat(marker):
    if marker not in mpl.lines.lineMarkers:
        return "o"
    return marker

