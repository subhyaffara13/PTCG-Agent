
def is_dynamic_dtype_set(op):
    # Detect if the OpInfo entry acquired dtypes dynamically
    # using `get_supported_dtypes`.
    return op.dynamic_dtypes

