
def parquetfastparquet_responder(df):
    # the fastparquet engine doesn't like to write to a buffer
    # it can do it via the open_with function being set appropriately
    # however it automatically calls the close method and wipes the buffer
    # so just overwrite that attribute on this instance to not do that

    # protected by an importorskip in the respective test
    import fsspec

    df.to_parquet(
        "memory://fastparquet_user_agent.parquet",
        index=False,
        engine="fastparquet",
        compression=None,
    )
    with fsspec.open("memory://fastparquet_user_agent.parquet", "rb") as f:
        return f.read()

