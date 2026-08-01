
def iter_files():
    return lambda *a, **kw: list(tools.iter_filenames(*a, **kw))

