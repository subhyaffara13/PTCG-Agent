
def handle_data_source(data: object) -> pd.DataFrame | Mapping | None:
    """Convert the data source object to a common union representation."""
    if isinstance(data, pd.DataFrame) or hasattr(data, "__dataframe__"):
        # Check for pd.DataFrame inheritance could be removed once
        # minimal pandas version supports dataframe interchange (1.5.0).
        data = convert_dataframe_to_pandas(data)
    elif data is not None and not isinstance(data, Mapping):
        err = f"Data source must be a DataFrame or Mapping, not {type(data)!r}."
        raise TypeError(err)

    return data

