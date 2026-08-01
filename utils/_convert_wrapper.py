
def _convert_wrapper(f, conv_dtype):
    def wrapper(
        arr: np.ndarray, indexer: np.ndarray, out: np.ndarray, fill_value=np.nan
    ) -> None:
        if conv_dtype == object:
            # GH#39755 avoid casting dt64/td64 to integers
            arr = ensure_wrapped_if_datetimelike(arr)
        arr = arr.astype(conv_dtype)
        f(arr, indexer, out, fill_value=fill_value)

    return wrapper

