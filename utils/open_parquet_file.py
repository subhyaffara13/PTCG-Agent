
def open_parquet_file(*args, **kwargs):
    """Create files tailed to reading specific parts of parquet files

    Please see ``open_parquet_files`` for details of the arguments. The
    difference is, this function always returns a single ``AlreadyBufferedFile``,
    whereas `open_parquet_files`` always returns a list of files, even if
    there are one or zero matching parquet files.
    """
    return open_parquet_files(*args, **kwargs)[0]

