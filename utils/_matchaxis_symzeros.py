
def _matchaxis_symzeros(axis_data, src, dst, x, sum_match=False):
  # Just like `matchaxis`, but handles symbolic zeros using ad_util.py
  # TODO(mattjj): dedup with matchaxis
  if isinstance(x, (Zero, SymbolicZero)):
    if src == dst:
      return x
    elif type(src) == type(dst) == int:
      aval = core.mapped_aval(axis_data.size, src, x.aval)
      return type(x)(core.unmapped_aval(axis_data.size, dst, aval,
                                        axis_data.explicit_mesh_axis))
    elif src is None and dst is not None:
      return type(x)(core.unmapped_aval(axis_data.size, dst, x.aval,
                                        axis_data.explicit_mesh_axis))
    elif dst is None and sum_match:
      return type(x)(core.mapped_aval(axis_data.size, src, x.aval))
    else:
      raise ValueError((axis_data.name, x, src, dst))
  else:
    return matchaxis(axis_data, src, dst, x, sum_match=sum_match)

