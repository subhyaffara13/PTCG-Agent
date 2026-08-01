
def _package_executorch_files(
    archive_writer: PT2ArchiveWriter, executorch_files: dict[str, bytes] | None
) -> None:
    if executorch_files is None:
        return

    for file_name, content in executorch_files.items():
        archive_writer.write_bytes(f"{EXECUTORCH_DIR}{file_name}", content)

