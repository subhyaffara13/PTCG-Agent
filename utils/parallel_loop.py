
def parallel_loop(
    lower: jax.typing.ArrayLike,
    upper: jax.typing.ArrayLike,
    step: jax.typing.ArrayLike = ...,
    *,
    unroll: int = ...,
    carry: None = None,
) -> Callable[[Callable[[jax.Array], None]], None]:
  ...


def parallel_loop(
    lower: jax.typing.ArrayLike,
    upper: jax.typing.ArrayLike,
    step: jax.typing.ArrayLike = ...,
    *,
    unroll: int = ...,
    carry: _T,
) -> Callable[[Callable[[jax.Array, _T], _T]], _T]:
  ...


def parallel_loop(lower, upper, step=1, *, unroll=1, carry=None):
  """A parallel loop decorator.

  The decorated function forms the loop body. It is called with the current
  loop index as the argument and optionally, a single additional carry argument.

  The loop iterations must be independent, meaning that operations in one
  iteration cannot depend on the side effects, especially Ref writes, of any
  other iteration. This allows the compiler to execute instructions from
  different iterations concurrently, potentially reordering them for better
  performance.

  Cross-iteration dependencies traceable via carried values are allowed. Refs
  may not be carried.

  Safe usage of carried value::

    @parallel_loop(0, 64, step=8, carry=jnp.int32(1))
    def body(i, j):
      # Writes are independent across iterations.
      x_ref[pl.ds(i, 8)] = j + jnp.arange(8)
      return j + 1

  Any pytree can be carried. The final value is returned by the decorator::

    def body(i, my_tree: MyTree):
      # Writes are independent across iterations.
      x_ref[pl.ds(i, 8)] = my_tree.transform(jnp.arange(8))
      return my_tree.step(i)
    final_value = parallel_loop(0, 64, step=8, carry=MyTree())(body)

  Undefined result::

    @parallel_loop(0, 64, step=4, carry=jnp.int32(1))
    def body(i, j):
      # Because the step size is 4, the array written is of size 8, and loop
      # iterations may be reordered, the values in indices 4-59 of x_ref are
      # unspecified after the loop. (The values in 0-3 and 60-63 are only
      # written by the first and last iterations, so are well-defined.)
      x_ref[pl.ds(i, 8)] = j + jnp.arange(8)
      return j + 1

  Unsafe read of "previous" iteration's write (don't do this)::

    @parallel_loop(0, 64, 8, carry=jnp.int32(1))
    def body(i, j):
      # Unsafe because it depends on the side-effect of "previous" iterations,
      # which may be executed in parallel or reordered.
      mask = x_ref[pl.ds(0, 8)] < j
      x_ref[pl.ds(0, 8)] += jnp.where(mask, j + jnp.arange(8), 0)
      return j + 1

  Args:
    lower: The starting value of the loop index.
    upper: The exclusive upper bound of the loop index.
    step: The increment of the loop index. Default to 1.
    unroll: The unroll factor of the loop.
    carry: Optional carried state of the loop.

  Returns:
    A decorator that executes the given function in a parallel loop.
  """

  def decorator(body):
    flat_carries, carry_tree = jax.tree.flatten(carry)
    def wrapped(idx, *carries):
      if carry is None:
        body(idx)
        return []
      result = body(idx, carry_tree.unflatten(carries))
      result, result_tree = jax.tree.flatten(result)
      if result_tree != carry_tree:
        raise ValueError(
            "parallel_loop: body result should have same structure as carry:"
            f" {result_tree} != {carry_tree}"
        )
      return result

    flat_avals = [
        pallas_core.index_map_grid_aval,
        *(c.aval for c in flat_carries),
    ]
    debug_info = api_util.debug_info("parallel_loop", body, flat_avals, {})
    check_no_transformed_refs_args(lambda: debug_info, flat_carries)
    jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(
        lu.wrap_init(wrapped, debug_info=debug_info), flat_avals
    )
    carry_tree.unflatten(jaxpr.outvars)  # Verify same structure.
    disallowed_effects = effects.control_flow_allowed_effects.filter_not_in(
        jaxpr.effects
    )
    if disallowed_effects:
      raise NotImplementedError(
          f"Effects not supported in parallel_loop: {disallowed_effects}"
      )
    flat_args, tree = jax.tree.flatten(
        (lower, upper, step, consts, flat_carries)
    )
    flat_result = parallel_loop_p.bind(
        *flat_args, tree=tree, unroll=unroll, jaxpr=jaxpr
    )
    if carry is None:
      return None
    return carry_tree.unflatten(flat_result)

  return decorator

