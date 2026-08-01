
def _transform_text_io_wrapper(node):
    # This is not always correct, since it can vary with the type of the descriptor,
    # being stdout, stderr or stdin. But we cannot get access to the name of the
    # stream, which is why we are using the BufferedWriter class as a default
    # value
    return _generic_io_transform(node, name="buffer", cls=BufferedWriter)

