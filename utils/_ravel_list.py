from typing import Any, Callable

def _ravel_list(lst: list[Any], /) -> tuple[Array, Callable[[Array], list[Any]]]:
  if not lst:
    return lax.full([0], 0, "float32"), lambda _: []
  from_dtypes = tuple(dtypes.dtype(l) for l in lst)
  to_dtype = dtypes.result_type(*from_dtypes)
  sizes, shapes = unzip2((np.size(x), np.shape(x)) for x in lst)

  if all(dt == to_dtype for dt in from_dtypes):
    # Skip any dtype conversion, resulting in a dtype-polymorphic `unravel`.
    # See https://github.com/jax-ml/jax/issues/7809.
    del from_dtypes, to_dtype
    ravel = lambda e: lax.reshape(e, (np.size(e),))
    raveled = lax.concatenate([ravel(e) for e in lst], dimension=0)
    return raveled, HashablePartial(_unravel_list_single_dtype, sizes, shapes)

  # When there is more than one distinct input dtype, we perform type
  # conversions and produce a dtype-specific unravel function.
  ravel = lambda e: lax.convert_element_type(e, to_dtype).ravel()
  raveled = lax.concatenate([ravel(e) for e in lst], dimension=0)
  unrav = HashablePartial(_unravel_list, sizes, shapes, from_dtypes, to_dtype)
  return raveled, unrav

