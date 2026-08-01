
def _reduce_argmax_combine(left, right):
  value1, index1 = left
  value2, index2 = right
  gt = value1 > value2
  lt = value1 < value2
  index_min = jnp.minimum(index1, index2)
  index_ret = jnp.where(gt, index1, jnp.where(lt, index2, index_min))
  value_ret = jnp.maximum(value1, value2)
  return value_ret, index_ret

