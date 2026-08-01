
def convert_object_array(
    content: list[npt.NDArray[np.object_]],
    dtype: DtypeObj | None,
    dtype_backend: str = "numpy",
    coerce_float: bool = False,
) -> list[ArrayLike]:
    """
    Internal function to convert object array.

    Parameters
    ----------
    content: List[np.ndarray]
    dtype: np.dtype or ExtensionDtype
    dtype_backend: Controls if nullable/pyarrow dtypes are returned.
    coerce_float: Cast floats that are integers to int.

    Returns
    -------
    List[ArrayLike]
    """
    # provide soft conversion of object dtypes

    def convert(arr):
        if dtype != np.dtype("O"):
            # e.g. if dtype is UInt32 then we want to cast Nones to NA instead of
            #  NaN in maybe_convert_objects.
            to_nullable = dtype_backend != "numpy" or isinstance(dtype, BaseMaskedDtype)
            arr = lib.maybe_convert_objects(
                arr,
                try_float=coerce_float,
                convert_to_nullable_dtype=to_nullable,
            )
            # Notes on cases that get here 2023-02-15
            # 1) we DO get here when arr is all Timestamps and dtype=None
            # 2) disabling this doesn't break the world, so this must be
            #    getting caught at a higher level
            # 3) passing convert_non_numeric to maybe_convert_objects get this right
            # 4) convert_non_numeric?

            if dtype is None:
                if arr.dtype == np.dtype("O"):
                    # i.e. maybe_convert_objects didn't convert
                    convert_to_nullable_dtype = dtype_backend != "numpy"
                    arr = lib.maybe_convert_objects(
                        arr,
                        # Here we do not convert numeric dtypes, as if we wanted that,
                        #  numpy would have done it for us.
                        convert_numeric=False,
                        convert_non_numeric=True,
                        convert_to_nullable_dtype=convert_to_nullable_dtype,
                        dtype_if_all_nat=np.dtype("M8[s]"),
                    )
                    if convert_to_nullable_dtype and arr.dtype == np.dtype("O"):
                        new_dtype = StringDtype()
                        arr_cls = new_dtype.construct_array_type()
                        arr = arr_cls._from_sequence(arr, dtype=new_dtype)
                elif dtype_backend != "numpy" and isinstance(arr, np.ndarray):
                    if arr.dtype.kind in "iufb":
                        arr = pd_array(arr, copy=False)

            elif isinstance(dtype, ExtensionDtype):
                # TODO: test(s) that get here
                # TODO: try to de-duplicate this convert function with
                #  core.construction functions
                cls = dtype.construct_array_type()
                arr = cls._from_sequence(arr, dtype=dtype, copy=False)
            elif dtype.kind in "mM":
                # This restriction is harmless bc these are the only cases
                #  where maybe_cast_to_datetime is not a no-op.
                # Here we know:
                #  1) dtype.kind in "mM" and
                #  2) arr is either object or numeric dtype
                arr = maybe_cast_to_datetime(arr, dtype)

        return arr

    arrays = [convert(arr) for arr in content]

    return arrays

