
def _load_extra_files(
    archive_reader: PT2ArchiveReader, file_names: list[str]
) -> dict[str, Any]:
    extra_files = [file for file in file_names if file.startswith(EXTRA_DIR)]

    extra_file_contents: dict[str, Any] = {}
    for file in extra_files:
        contents = archive_reader.read_string(file)
        extra_file_contents[file[len(EXTRA_DIR) :]] = contents

    return extra_file_contents

