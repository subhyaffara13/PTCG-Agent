
def dimension_as_value(d: DimSize):
  """Turns a dimension size into a JAX array.
     This is the identity function for constant dimensions.

     Has the same abstract value as Python constants.
     """
  if isinstance(d, (int, Tracer, np.int32, np.int64)): return d
  # For shape_poly._DimPolynomial
  m = getattr(d, "dimension_as_value", None)
  if m is not None: return m()
  return operator.index(d)

