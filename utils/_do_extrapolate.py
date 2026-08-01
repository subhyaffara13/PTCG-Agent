
def _do_extrapolate(fill_value):
    """Helper to check if fill_value == "extrapolate" without warnings"""
    return (isinstance(fill_value, str) and
            fill_value == 'extrapolate')

