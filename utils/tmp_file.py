
def tmp_file(dir=None, name=''):
    return NamedTemporaryFile(
    suffix='.png', dir=dir, delete=False).name

