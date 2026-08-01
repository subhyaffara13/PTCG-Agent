
def _export_file(
    model_bytes: bytes,
    f: io.BytesIO | str,
    export_map: Mapping[str, bytes],
) -> None:
    """export/write model bytes into directory/protobuf/zip"""
    if len(export_map) != 0:
        raise AssertionError(f"export_map must be empty, got {len(export_map)} items")
    with torch.serialization._open_file_like(f, "wb") as opened_file:
        opened_file.write(model_bytes)

