
def layout_cast(x: _ods_ir.Value[_ods_ir.VectorType], new_layout: _Union[_Any, _ods_ir.Attribute], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return LayoutCastOp(x=x, new_layout=new_layout, results=results, loc=loc, ip=ip).result


def layout_cast(x: Any, new_layout: SomeLayout):
  """Casts the layout of the given array."""
  return layout_cast_p.bind(x, new_layout=new_layout)

