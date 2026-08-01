
def read_wheel_metadata_file(source: ZipFile, path: str) -> bytes:
    try:
        return source.read(path)
        # BadZipFile for general corruption, KeyError for missing entry,
        # and RuntimeError for password-protected files
    except (BadZipFile, KeyError, RuntimeError) as e:
        raise UnsupportedWheel(f"could not read {path!r} file: {e!r}")

