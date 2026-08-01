
def get_data_from_filepath(
    filepath_or_buffer: FilePath | ReadBuffer[bytes] | ReadBuffer[str],
    encoding: str | None,
    compression: CompressionOptions,
    storage_options: StorageOptions,
):
    """
    Extract raw XML data.

    The method accepts two input types:
        1. filepath (string-like)
        2. file-like object (e.g. open file object, StringIO)
    """
    filepath_or_buffer = stringify_path(filepath_or_buffer)
    with get_handle(
        filepath_or_buffer,
        "r",
        encoding=encoding,
        compression=compression,
        storage_options=storage_options,
    ) as handle_obj:
        return (
            preprocess_data(handle_obj.handle.read())
            if hasattr(handle_obj.handle, "read")
            else handle_obj.handle
        )

