
def check_entry_points(dist, attr, value):
    """Verify that entry_points map is parseable"""
    try:
        _entry_points.load(value)
    except Exception as e:
        raise DistutilsSetupError(e) from e

