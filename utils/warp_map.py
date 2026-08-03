from typing import Callable

def warp_map(operands, *, loc=None, ip=None) -> WarpMapOp:
  return WarpMapOp(operands, loc=loc, ip=ip)


def warp_map(operands_: _Sequence[_ods_ir.Value], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> WarpMapOp:
  return WarpMapOp(operands_=operands_, loc=loc, ip=ip)


def warp_map(f: Callable[[jax.Array], _T], /) -> _T:
  """Runs a function with single warp semantics, passing it the warp ID."""
  mesh = gpu_core.WarpMesh(axis_name=object())
  return pallas_core.core_map(mesh)(lambda: f(lax.axis_index(mesh.axis_name)))

