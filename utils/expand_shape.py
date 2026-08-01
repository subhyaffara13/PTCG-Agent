
def expand_shape(arr_shape, axis):
    # taken from numpy 1.23.x, expand_dims function
    if type(axis) not in (list, tuple):
        axis = (axis,)
    out_ndim = len(axis) + len(arr_shape)
    axis = normalize_axis_tuple(axis, out_ndim)
    shape_it = iter(arr_shape)
    shape = [1 if ax in axis else next(shape_it) for ax in range(out_ndim)]
    return shape


def expand_shape(result: _ods_ir.Type, src: _ods_ir.Value[_ods_ir.MemRefType], reassociation: _Union[_Any, _ods_ir.ArrayAttr], output_shape: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], static_output_shape: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.MemRefType]:
  return ExpandShapeOp(result=result, src=src, reassociation=reassociation, output_shape=output_shape, static_output_shape=static_output_shape, loc=loc, ip=ip).result

