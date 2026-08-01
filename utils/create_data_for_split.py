
def create_data_for_split(
    df: DataFrame, are_all_object_dtype_cols: bool, object_dtype_indices: list[int]
) -> Generator[list]:
    """
    Simple helper method to create data for to ``to_dict(orient="split")``
    to create the main output data
    """
    if are_all_object_dtype_cols:
        for tup in df.itertuples(index=False, name=None):
            yield list(map(maybe_box_native, tup))
    else:
        for tup in df.itertuples(index=False, name=None):
            data = list(tup)
            if object_dtype_indices:
                # If we have object_dtype_cols, apply maybe_box_naive after
                # for perf
                for i in object_dtype_indices:
                    data[i] = maybe_box_native(data[i])
            yield data

