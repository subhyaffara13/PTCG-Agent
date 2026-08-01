
def _print_on_nosuchfile(e):
    """Print helpful troubleshooting message

    e is an exception raised by subprocess.check_call()

    """
    if e.errno == 2:
        logging.error(
            "Could not find zic. Perhaps you need to install "
            "libc-bin or some other package that provides it, "
            "or it's not in your PATH?")

