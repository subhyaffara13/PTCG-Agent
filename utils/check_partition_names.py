
def check_partition_names(path, expected):
    """Check partitions of a parquet file are as expected.

    Parameters
    ----------
    path: str
        Path of the dataset.
    expected: iterable of str
        Expected partition names.
    """
    import pyarrow.dataset as ds

    dataset = ds.dataset(path, partitioning="hive")
    assert dataset.partitioning.schema.names == expected

