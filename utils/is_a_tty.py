
def is_a_tty(stream):
    return StreamWrapper(stream, None).isatty()

