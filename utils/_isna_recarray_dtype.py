
def _isna_recarray_dtype(values: np.rec.recarray) -> npt.NDArray[np.bool_]:
    result = np.zeros(values.shape, dtype=bool)
    for i, record in enumerate(values):
        record_as_array = np.array(record.tolist())
        does_record_contain_nan = isna_all(record_as_array)
        result[i] = np.any(does_record_contain_nan)

    return result

