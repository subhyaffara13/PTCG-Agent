from typing import Optional

def subview(
    source: Value,
    offsets: MixedValues,
    sizes: MixedValues,
    strides: MixedValues,
    *,
    result_type: Optional[MemRefType] = None,
    loc=None,
    ip=None,
):
    if offsets is None:
        offsets = []
    if sizes is None:
        sizes = []
    if strides is None:
        strides = []
    source_strides, source_offset = source.type.get_strides_and_offset()
    if result_type is None and all(
        all(_is_static_int_like(i) for i in s) for s in [sizes, strides, source_strides]
    ):
        # If any are arith.constant results then this will canonicalize to python int
        # (which can then be used to fully specify the subview).
        (
            offsets,
            sizes,
            strides,
            result_type,
        ) = _infer_memref_subview_result_type(source.type, offsets, sizes, strides)
    elif result_type is None:
        raise ValueError(
            "mixed static/dynamic offset/sizes/strides requires explicit result type."
        )

    offsets, _packed_offsets, static_offsets = _dispatch_mixed_values(offsets)
    sizes, _packed_sizes, static_sizes = _dispatch_mixed_values(sizes)
    strides, _packed_strides, static_strides = _dispatch_mixed_values(strides)

    return _generated_subview(
        result_type,
        source,
        offsets,
        sizes,
        strides,
        static_offsets,
        static_sizes,
        static_strides,
        loc=loc,
        ip=ip,
    )


def subview(result: _ods_ir.Type, source: _ods_ir.Value[_ods_ir.MemRefType], offsets: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], sizes: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], strides: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], static_offsets: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], static_sizes: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], static_strides: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.MemRefType]:
  return SubViewOp(result=result, source=source, offsets=offsets, sizes=sizes, strides=strides, static_offsets=static_offsets, static_sizes=static_sizes, static_strides=static_strides, loc=loc, ip=ip).result

