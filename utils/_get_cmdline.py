
def _get_cmdline(pid):
    path = os.path.join("/proc", str(pid), "cmdline")
    encoding = sys.getfilesystemencoding() or "utf-8"
    with io.open(path, encoding=encoding, errors="replace") as f:
        # XXX: Command line arguments can be arbitrary byte sequences, not
        # necessarily decodable. For Shellingham's purpose, however, we don't
        # care. (pypa/pipenv#2820)
        # cmdline appends an extra NULL at the end, hence the [:-1].
        return tuple(f.read().split("\0")[:-1])

