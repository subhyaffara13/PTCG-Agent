
def _mulhi_impl(x: Array, y: Array) -> Array:
  """Temporary mulhi impl until XLA supports it natively."""
  dtype = x.dtype
  info = dtypes.iinfo(dtype)
  bits = info.bits
  is_signed = dtypes.issubdtype(dtype, np.signedinteger)

  if bits < 64:
    # For sub-64-bit types, widen to double-width, multiply, shift right.
    widen_dtype = np.dtype(f'{"i" if is_signed else "u"}{bits * 2 // 8}')
    x_wide = convert_element_type(x, widen_dtype)
    y_wide = convert_element_type(y, widen_dtype)
    prod = mul(x_wide, y_wide)
    result = shift_right_arithmetic(prod, _const(prod, bits)) if is_signed \
        else shift_right_logical(prod, _const(prod, bits))
    return convert_element_type(result, dtype)
  else:
    # For 64-bit types, use half-width split multiply in uint64.
    u64 = np.dtype('uint64')
    x_u64 = convert_element_type(x, u64)
    y_u64 = convert_element_type(y, u64)
    lomask_val = np.uint64(0xFFFFFFFF)

    x_lo = bitwise_and(x_u64, _const(x_u64, lomask_val))
    x_hi = shift_right_logical(x_u64, _const(x_u64, 32))
    y_lo = bitwise_and(y_u64, _const(y_u64, lomask_val))
    y_hi = shift_right_logical(y_u64, _const(y_u64, 32))

    # Four partial products.
    lo_lo = mul(x_lo, y_lo)
    lo_hi = mul(x_lo, y_hi)
    hi_lo = mul(x_hi, y_lo)
    hi_hi = mul(x_hi, y_hi)

    # Accumulate cross terms and carry.
    cross_lo = add(bitwise_and(lo_hi, _const(lo_hi, lomask_val)),
                   bitwise_and(hi_lo, _const(hi_lo, lomask_val)))
    cross_lo = add(cross_lo, shift_right_logical(lo_lo, _const(lo_lo, 32)))

    # High 64 bits of the unsigned product.
    hi64 = add(hi_hi,
               add(shift_right_logical(lo_hi, _const(lo_hi, 32)),
                   add(shift_right_logical(hi_lo, _const(hi_lo, 32)),
                       shift_right_logical(cross_lo, _const(cross_lo, 32)))))
    hi64 = convert_element_type(hi64, dtype)

    if is_signed:
      # Signed correction: signed_mulhi = unsigned_mulhi - (x<0 ? y : 0) - (y<0 ? x : 0)
      x_sign = shift_right_arithmetic(x, _const(x, 63))
      y_sign = shift_right_arithmetic(y, _const(y, 63))
      hi64 = add(hi64, add(mul(x_sign, y), mul(y_sign, x)))
    return hi64

