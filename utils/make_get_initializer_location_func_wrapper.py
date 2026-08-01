
def make_get_initializer_location_func_wrapper(
    get_initializer_location_func: GetInitializerLocationFunc,
) -> GetInitializerLocationWrapperFunc:
    """
    Wraps a user's "get initializer location" function. The returned wrapper function adheres to the
    signature expected by ORT.

    Need this wrapper to:
      - Convert the `initializer_value` parameter from `C.OrtValue` to `onnxruntime.OrtValue`, which is more
        convenient for the user's function to use.
      - Allow the user's function to return the original `external_info` parameter (this wrapper makes a copy)
    """

    def get_initializer_location_func_wrapper(
        initializer_name: str,
        initializer_value: C.OrtValue,
        external_info: C.OrtExternalInitializerInfo | None,
    ) -> C.OrtExternalInitializerInfo | None:
        ret_val: C.OrtExternalInitializerInfo | None = get_initializer_location_func(
            initializer_name, OrtValue(initializer_value), external_info
        )
        if ret_val is not None and ret_val == external_info:
            # User returned `external_info` (const and owned by ORT). ORT expects the returned value to be
            # a new instance (that it deletes), so make a copy.
            ret_val = C.OrtExternalInitializerInfo(ret_val.filepath, ret_val.file_offset, ret_val.byte_size)
        return ret_val

    return get_initializer_location_func_wrapper

