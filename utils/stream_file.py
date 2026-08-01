
def stream_file(path: os.PathLike) -> Iterator[IO[str]]:
    """
    Open a file and yield the corresponding (decoded) stream.

    Exits with error code 2 if the file cannot be opened.
    """

    try:
        with open(path) as stream:
            yield stream
    except OSError as exc:
        print(f"Error opening env file: {exc}", file=sys.stderr)
        sys.exit(2)

