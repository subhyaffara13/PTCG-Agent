
def _as_index(v: object) -> ir.Value:
  match v:
    case int():
      return arith_dialect.constant(ir.IndexType.get(), v)
    case ir.Value() if isinstance(v.type, ir.IndexType):
      return v
    case ir.Value() if isinstance(v.type, ir.IntegerType):
      return arith_dialect.index_cast(ir.IndexType.get(), v)
    case mgpu.FragmentedArray(layout=mgpu.WGSplatFragLayout()):
      return _as_index(v.registers.item())
    case jax_literals.TypedNdArray() if (
        np.issubdtype(v.dtype, np.integer) and v.ndim == 0
    ):
      return arith_dialect.constant(ir.IndexType.get(), int(v))
    case _:
      raise ValueError(f"Unsupported index: {v} of type {type(v)}")

