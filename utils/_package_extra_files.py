from typing import Any

def _package_extra_files(
    archive_writer: PT2ArchiveWriter, extra_files: dict[str, Any] | None
) -> None:
    if extra_files is None:
        return

    for extra_file_name, content in extra_files.items():
        archive_writer.write_string(f"{EXTRA_DIR}{extra_file_name}", content)

