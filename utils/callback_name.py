
def callback_name(callback):
    if isinstance(callback, str):
        return callback

    try:
        return callback.__name__
    except AttributeError:
        try:
            return callback.__class__.__name__
        except AttributeError:
            return str(callback)

