from pathlib import Path


def _file_output_stream_context(filename: str | Path, source_file: File) -> Iterator[TextIO]:
    tmp_file = _tmp_file(source_file)
    with tmp_file.open("w+", encoding=source_file.encoding, newline="") as output_stream:
        shutil.copymode(filename, tmp_file)
        yield output_stream

