import itertools
from typing import Any

def pallas_call_hlo_interpret(
    *args,
    jaxpr: jax_core.Jaxpr,
    debug: bool,
    input_output_aliases: tuple[tuple[int, int], ...],
    grid_mapping: GridMapping,
    mesh: pallas_core.Mesh | None,
    compiler_params: Any,
    cost_estimate: CostEstimate,
    out_avals: tuple[jax_core.AbstractValue, ...],
    metadata: frozen_dict.FrozenDict[str, str] | None,
    name: str | None,
):
  del mesh, compiler_params, cost_estimate, out_avals, metadata, name
  debug_info = jaxpr.debug_info
  # If we're in interpret mode, we *scan* over the grid and eval the
  # discharged jaxpr.
  dynamic_grid_args, args = split_list(
      args, [grid_mapping.num_dynamic_grid_bounds]
  )
  dynamic_grid_args_iter = iter(dynamic_grid_args)
  grid = tuple(
      a if not isinstance(a, pallas_core.DynamicGridDim)
      else next(dynamic_grid_args_iter)
      for a in grid_mapping.grid
  )
  assert next(dynamic_grid_args_iter, None) is None
  discharged_jaxpr, discharged_consts, scratch_avals = kernel_to_hlo_jaxpr(
      jaxpr, (), grid_mapping)
  if debug:
    print(f"\nJaxpr of the kernel in pallas_call {debug_info.func_src_info}:")
    print(discharged_jaxpr)
  out = _initialize_output_vals(grid_mapping.block_mappings_output,
                                args, input_output_aliases)
  # TODO(b/370563936): Fix correctness issue w/ io aliasing
  scalars = args[grid_mapping.slice_index_ops]
  block_args = args[len(scalars):]
  # invars: [*scalar_prefetch, *consts, *inputs, *outputs, *scratch]
  # block_args now contains: *consts, *inputs, *outputs
  scratch_values = tuple(
      primitives.uninitialized_value(a.shape, a.dtype) for a in scratch_avals
  )

  carry = []
  for x, bm in zip(itertools.chain(block_args, out), grid_mapping.block_mappings):
    padding = [bd.padding if isinstance(bd, pallas_core.Element) else (0, 0)
               for bd in bm.block_shape]
    if padding is not None and any(p != (0, 0) for p in padding):
      if input_output_aliases:
        raise NotImplementedError("Padding with aliasing not supported.")
      pad_value = primitives.uninitialized_value(shape=(), dtype=x.dtype)
      x = lax.pad(x, pad_value, [(*p, 0) for p in padding])
    carry.append(x)

  block_shapes = [pallas_core._get_block_shape(bm.block_shape)
                  for bm in grid_mapping.block_mappings]
  is_squeeze_dim = [
      tuple(isinstance(bd, pallas_core.Squeezed) for bd in bm.block_shape)
      for bm in grid_mapping.block_mappings
  ]

  # Pad values to evenly divide into block dimensions. This matches the
  # behavior of the non-interpret mode. We pad with NaN, to make it easier
  # to catch OOB accesses.

  carry = map(_pad_to_block_dimension, carry, block_shapes)
  carry.extend(scratch_values)

  num_inout_blocks = len(block_args) + len(out)
  grid_start_indices = (jnp.int32(0),) * len(grid)
  if grid:
    num_iterations = reduce(jnp.multiply, grid)
  else:
    # Base case is always one iteration when grid is ()
    num_iterations = 1

  # The scan carry: (i, loop_idx, *consts, *ins, *outs, *scratch)
  # i:int32 is the iteration index
  # loop_idx: tuple[int32] are the program ids for each grid axis
  def cond(carry):
    i, *_ = carry
    return i < num_iterations
  def body(carry):
    i, loop_idx, *carry_blocks = carry

    if grid_mapping.local_grid_env is not None:
      local_grid_env = grid_mapping.local_grid_env(loop_idx, grid)
    else:
      local_grid_env = tuple(
          pallas_core.GridAxis(idx, b)
          for dim, (idx, b) in enumerate(zip(loop_idx, grid))
          if dim not in grid_mapping.vmapped_dims
      )

    carry_consts_ins, scratch = split_list(carry_blocks, [num_inout_blocks])
    with pallas_core.grid_env(local_grid_env):
      for s in scalars:
        if isinstance(s.dtype, jax_core.bint):
          aval = jax_core.typeof(s)
          s.aval = aval.update(dtype=jnp.int32)
      start_indices = [
          bm.compute_start_indices_interpret(loop_idx, *scalars)
          for bm in grid_mapping.block_mappings
      ]
    blocks = map(_dynamic_slice, start_indices, block_shapes,
                 carry_consts_ins, is_squeeze_dim)
    with pallas_core.grid_env(local_grid_env):
      assert len(discharged_jaxpr.invars) == len(scalars) + len(blocks) + len(
          scratch_values
      ), (
          len(discharged_jaxpr.invars),
          len(scalars),
          len(blocks),
          len(scratch_values),
      )

      blocks = jax_core.eval_jaxpr(
          discharged_jaxpr, discharged_consts, *scalars, *blocks, *scratch
      )

    _, out_inout, out_scratch = split_list(
        blocks, [grid_mapping.num_index_operands, num_inout_blocks])
    out_carry = map(_dynamic_update_slice, start_indices, block_shapes,
                    carry_consts_ins, out_inout, is_squeeze_dim)
    return (i + 1, _get_next_indices(grid, loop_idx),
            *out_carry, *out_scratch)

  (_, _, *carry) = loops.while_loop(
      cond, body, (jnp.int32(0), grid_start_indices, *carry)
  )

  out_out = carry[len(block_args):len(block_args) + len(out)]
  out_nopad = []
  for o, bm in zip(out_out, grid_mapping.block_mappings_output):
    padding = [bd.padding if isinstance(bd, pallas_core.Element) else (0, 0)
               for bd in bm.block_shape]
    if padding is not None and any(p != (0, 0) for p in padding):
      if input_output_aliases:
        raise NotImplementedError("Padding with aliasing not supported.")
      pad_low, pad_high = zip(*padding)
      limit_indices = [s - p for s, p in zip(o.shape, pad_high)]
      o = slicing.slice(o, pad_low, limit_indices)
    if o.shape != bm.array_aval.shape:
      o = slicing.slice(o, (0,) * o.ndim, bm.array_aval.shape)
    out_nopad.append(o)
  return out_nopad

