
def write_file(path: str, contents: str) -> None:
    """Write data into a file.

    If the file already exists and has the same contents we
    want to write, skip writing so as to preserve the mtime
    and avoid triggering recompilation.
    """
    # We encode it ourselves and open the files as binary to avoid windows
    # newline translation
    encoded_contents = contents.encode("utf-8")
    try:
        with open(path, "rb") as f:
            old_contents: bytes | None = f.read()
    except OSError:
        old_contents = None
    if old_contents != encoded_contents:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as g:
            g.write(encoded_contents)

        # Fudge the mtime forward because otherwise when two builds happen close
        # together (like in a test) setuptools might not realize the source is newer
        # than the new artifact.
        # XXX: This is bad though.
        new_mtime = os.stat(path).st_mtime + 1
        os.utime(path, times=(new_mtime, new_mtime))


def write_file(file, content):
    with open(file, "w") as f:
        f.write(content)


def write_file(filename, contents) -> None:
    """Create a file with the specified name and write 'contents' (a
    sequence of strings without line terminators) to it.
    """
    contents = "\n".join(contents)

    # assuming the contents has been vetted for utf-8 encoding
    contents = contents.encode("utf-8")

    with open(filename, "wb") as f:  # always write POSIX-style manifest
        f.write(contents)


def write_file(filename, contents):
    """Create a file with the specified name and write 'contents' (a
    sequence of strings without line terminators) to it.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(line + '\n' for line in contents)

