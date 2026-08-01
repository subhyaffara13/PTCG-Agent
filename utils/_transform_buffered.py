
def _transform_buffered(node):
    return _generic_io_transform(node, name="raw", cls=FileIO)

