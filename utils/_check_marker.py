
def _check_marker(marker):
    if not marker:
        return
    m = Marker(marker)
    m.evaluate()

