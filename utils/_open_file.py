
def _open_file(file_like, appendmat, mode='rb'):
    """
    Open `file_like` and return as file-like object. First, check if object is
    already file-like; if so, return it as-is. Otherwise, try to pass it
    to open(). If that fails, and `file_like` is a string, and `appendmat` is true,
    append '.mat' and try again.
    """
    reqs = {'read'} if set(mode) & set('r+') else set()
    if set(mode) & set('wax+'):
        reqs.add('write')
    if reqs.issubset(dir(file_like)):
        return file_like, False

    try:
        return open(file_like, mode), True
    except OSError as e:
        # Probably "not found"
        if isinstance(file_like, str):
            if appendmat and not file_like.endswith('.mat'):
                file_like += '.mat'
            return open(file_like, mode), True
        else:
            raise OSError(
                'Reader needs file name or open file-like object'
            ) from e

