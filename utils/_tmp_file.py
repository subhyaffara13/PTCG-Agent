
def _tmp_file(source_file: File) -> Path:
    return source_file.path.with_suffix(source_file.path.suffix + ".isorted")

