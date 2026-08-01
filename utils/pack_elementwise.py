
def pack_elementwise(output: _ods_ir.Type, sources: _Sequence[_ods_ir.Value[_ods_ir.VectorType]], target_type: _Union[_ods_ir.Type, _ods_ir.TypeAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return PackElementwiseOp(output=output, sources=sources, target_type=target_type, loc=loc, ip=ip).result


def pack_elementwise(xs, *, packed_dtype):
  """Packs multiple arrays elementwise into a single array of a narrower dtype.

  The number of `xs` must equal the packing factor, which is the ratio of
  the element bitwidth of the `xs` to the element bitwidth of the
  `packed_dtype`. Elements from the `xs` are interleaved and packed into
  the `output`, ordered from lowest to highest bits, corresponding to their
  order in the `xs`.  The `output` is then bitcasted to the signless
  integer type of the same bitwidth as the `xs`.

  Note that for integer packing, the bits in `xs` that exceed the
  bitwidth of the `packed_type` are just truncated.
  For example, given the `xs` are int8 xxxx'1001 and yyyy'0011,
  `packed_type` is int4, the output will be 0011'1001.

  Args:
    xs: A list of arrays to pack.
    packed_dtype: The dtype of the packed array.

  Returns:
    The packed array.
  """
  return pack_elementwise_p.bind(*xs, packed_dtype=packed_dtype)

