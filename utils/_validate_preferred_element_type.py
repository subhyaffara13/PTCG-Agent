
def _validate_preferred_element_type(input_dtype, preferred_element_type):
  if (dtypes.issubdtype(input_dtype, np.integer) and
      dtypes.issubdtype(preferred_element_type, np.floating)):
    # Special-case integer->float multiply. This is allowed, and also allows
    # different signedness between input and output.
    pass
  else:
    allowed_types = (np.integer, np.floating, np.complexfloating)
    if any(dtypes.issubdtype(input_dtype, t) and not
           dtypes.issubdtype(preferred_element_type, t) for t in allowed_types):
      raise TypeError("Input type is incompatible with "
                      "`preferred_element_type`. The compatible combinations "
                      "of (input_type, preferred_element_type) are "
                      "(integral, integral), (integral, floating), "
                      "(floating, floating), (complex, complex.")
    if (dtypes.issubdtype(input_dtype, np.signedinteger) and
        not dtypes.issubdtype(preferred_element_type, np.signedinteger)):
      raise TypeError("`preferred_element_type` must have the same signedness "
                      "as the original type.")
  input_bitwidth = np.dtype(input_dtype).itemsize
  preferred_bitwidth = np.dtype(preferred_element_type).itemsize
  if preferred_bitwidth < input_bitwidth:
    raise TypeError("`preferred_element_type` must not be narrower than the "
                    "original type.")

