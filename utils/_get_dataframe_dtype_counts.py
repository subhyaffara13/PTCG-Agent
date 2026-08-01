
def _get_dataframe_dtype_counts(df: DataFrame) -> Mapping[str, int]:
    """
    Create mapping between datatypes and their number of occurrences.
    """
    # groupby dtype.name to collect e.g. Categorical columns
    return df.dtypes.value_counts().groupby(lambda x: x.name).sum()

