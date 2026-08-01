
def get_string(dump_fn, routines, prefix="file", **kwargs):
    """Wrapper for dump_fn. dump_fn writes its results to a stream object and
       this wrapper returns the contents of that stream as a string. This
       auxiliary function is used by many tests below.

       The header and the empty lines are not generator to facilitate the
       testing of the output.
    """
    output = StringIO()
    dump_fn(routines, output, prefix, **kwargs)
    source = output.getvalue()
    output.close()
    return source


def get_string(dump_fn, routines, prefix="file", header=False, empty=False):
    """Wrapper for dump_fn. dump_fn writes its results to a stream object and
       this wrapper returns the contents of that stream as a string. This
       auxiliary function is used by many tests below.

       The header and the empty lines are not generated to facilitate the
       testing of the output.
    """
    output = StringIO()
    dump_fn(routines, output, prefix, header, empty)
    source = output.getvalue()
    output.close()
    return source

