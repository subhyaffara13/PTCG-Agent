
def approx_max_k(operand: Array,
                 k: int,
                 reduction_dimension: int = -1,
                 recall_target: float = 0.95,
                 reduction_input_size_override: int = -1,
                 aggregate_to_topk: bool = True) -> tuple[Array, Array]:
  """Returns max ``k`` values and their indices of the ``operand`` in an approximate manner.

  See https://arxiv.org/abs/2206.14286 for the algorithm details.

  Args:
    operand : Array to search for max-k. Must be a floating number type.
    k : Specifies the number of max-k.
    reduction_dimension : Integer dimension along which to search. Default: -1.
    recall_target : Recall target for the approximation.
    reduction_input_size_override : When set to a positive value, it overrides
      the size determined by ``operand[reduction_dim]`` for evaluating the
      recall. This option is useful when the given ``operand`` is only a subset
      of the overall computation in SPMD or distributed pipelines, where the
      true input size cannot be deferred by the operand shape.
    aggregate_to_topk : When true, aggregates approximate results to the top-k
      in sorted order. When false, returns the approximate results unsorted. In
      this case, the number of the approximate results is implementation defined
      and is greater or equal to the specified ``k``.

  Returns:
    Tuple of two arrays. The arrays are the max ``k`` values and the
    corresponding indices along the ``reduction_dimension`` of the input
    ``operand``. The arrays' dimensions are the same as the input ``operand``
    except for the ``reduction_dimension``: when ``aggregate_to_topk`` is true,
    the reduction dimension is ``k``; otherwise, it is greater equals to ``k``
    where the size is implementation-defined.

  We encourage users to wrap ``approx_max_k`` with jit. See the following
  example for maximal inner production search (MIPS):

  >>> import functools
  >>> import jax
  >>> import numpy as np
  >>> @jax.jit(static_argnames=["k", "recall_target"])
  ... def mips(qy, db, k=10, recall_target=0.95):
  ...   dists = jax.lax.dot(qy, db.transpose())
  ...   # returns (f32[qy_size, k], i32[qy_size, k])
  ...   return jax.lax.approx_max_k(dists, k=k, recall_target=recall_target)
  >>>
  >>> qy = jax.numpy.array(np.random.rand(50, 64))
  >>> db = jax.numpy.array(np.random.rand(1024, 64))
  >>> dot_products, neighbors = mips(qy, db, k=10)
  """
  return approx_top_k_p.bind(
      operand,
      k=k,
      reduction_dimension=reduction_dimension,
      recall_target=recall_target,
      is_max_k=True,
      reduction_input_size_override=reduction_input_size_override,
      aggregate_to_topk=aggregate_to_topk)

