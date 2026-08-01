
def naryop_dtype_rule(result_dtype, accepted_dtypes, name, *avals,
                      require_same=True, allow_extended_dtype=False, **kwargs):
  assert len(avals) == len(accepted_dtypes), (avals, accepted_dtypes)
  for i, aval in enumerate(avals):
    if allow_extended_dtype and isinstance(aval.dtype, dtypes.ExtendedDType):
      continue
    types = accepted_dtypes[i]
    if not any(dtypes.issubdtype(aval.dtype, t) for t in types):
      if aval.dtype == dtypes.float0:
        raise TypeError(
            f"Called {name} with a float0 at position {i}. "
            "float0s do not support any operations by design, because they "
            "are not compatible with non-trivial vector spaces. No implicit dtype "
            "conversion is done. You can use np.zeros_like(arr, dtype=np.float) "
            "to cast a float0 array to a regular zeros array. \n"
            "If you didn't expect to get a float0 you might have accidentally "
            "taken a gradient with respect to an integer argument.")
      else:
        msg = ('{} does not accept dtype {} at position {}. '
               'Accepted dtypes at position {} are subtypes of {}.')
        typename = dtype_to_string(aval.dtype)
        typenames = ', '.join(t.__name__ for t in types)
        raise TypeError(msg.format(name, typename, i, i, typenames))
  if require_same and kwargs.get('out_dtype') is None:
    check_same_dtypes(name, *avals)
  return result_dtype(*avals, **kwargs)

