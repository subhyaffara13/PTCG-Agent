
def _is_buffered(iterator):
    try:
        iterator.itviews
    except ValueError:
        return True
    return False

