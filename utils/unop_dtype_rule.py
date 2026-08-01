
def unop_dtype_rule(result_dtype, accepted_dtypes, name, aval,
                    supports_narrow_ints=True, **kwargs):
  if aval.dtype == dtypes.float0:
    raise TypeError(
        f"Called {name} with a float0 array. "
        "float0s do not support any operations by design, because they "
        "are not compatible with non-trivial vector spaces. No implicit dtype "
        "conversion is done. You can use np.zeros_like(arr, dtype=np.float) "
        "to cast a float0 array to a regular zeros array. \n"
        "If you didn't expect to get a float0 you might have accidentally "
        "taken a gradient with respect to an integer argument.")
  if not any(dtypes.issubdtype(aval.dtype, t) for t in accepted_dtypes):
    msg = '{} does not accept dtype {}. Accepted dtypes are subtypes of {}.'
    typename = dtype_to_string(aval.dtype)
    accepted_typenames = (t.__name__ for t in accepted_dtypes)
    raise TypeError(msg.format(name, typename, ', '.join(accepted_typenames)))
  if (not supports_narrow_ints) and aval.dtype in [dtypes.uint2, dtypes.int2, dtypes.uint4, dtypes.int4]:
    raise TypeError(f'{name} does not accept dtype {dtype_to_string(aval.dtype)}.'
                    ' Support for narrow-width integers is platform-dependent'
                    ' and limited to a few specific operations, e.g. basic'
                    ' arithmetic and type casting.')
  return result_dtype(aval.dtype, **kwargs)

