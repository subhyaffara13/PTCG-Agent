
def primal_tangent_dtype(primal_dtype, tangent_dtype,
                         name: str | None = None) -> ExtendedDType:
  primal_dtype, tangent_dtype = map(dtype, (primal_dtype, tangent_dtype))
  name_ = name or (f'PrimalTangentDType{{{short_dtype_name(primal_dtype)}'
                   f'/{short_dtype_name(tangent_dtype)}}}')
  return PrimalTangentDType(primal_dtype, tangent_dtype, name_)

