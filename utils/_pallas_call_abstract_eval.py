from typing import Set

def _pallas_call_abstract_eval(
    *avals,
    out_avals: tuple[jax_core.AbstractValue, ...],
    interpret,
    compiler_params: CompilerParams | None,
    input_output_aliases,
    grid_mapping,
    **params,
):
  del params  # Unused.

  effs: Set[jax_core.Effect] = {*pallas_core.get_interpret_effects(interpret)}

  # closed-over refs and dynamic grid bounds aren't reflected in
  # input_output_aliases, though they are present in `avals`, so split them off
  num_refs = sum(isinstance(a, state.AbstractRef) for a in avals)
  _, _, avals = split_list(avals, [num_refs, grid_mapping.num_dynamic_grid_bounds])

  inout_aliases = dict(input_output_aliases)
  lin_avals = {i for i, a in enumerate(avals)
               if isinstance(a, state_types.AbstractLinVal)}
  if (missing := lin_avals - set(inout_aliases)):
    raise ValueError(f"input pinned buffers without input_output_aliases:"
                     f"{missing}")
  outin_aliases = {out_idx: in_idx for in_idx, out_idx in inout_aliases.items()}
  out_avals = tuple(
      avals[outin_aliases[out_idx]] if out_idx in outin_aliases else a
      for out_idx, a in enumerate(out_avals)
  )
  # Make sure we don't return ShapedArray with pallas memory space to the
  # outside world.
  out_avals = tuple(a.update(memory_space=jax_core.MemorySpace.Device)
                    if isinstance(a, jax_core.ShapedArray) else a
                    for a in out_avals)

  # TODO(mattjj,yashkatariya): if we hide vmapped away mesh axes, use this:
  # if not (all(a.sharding.mesh.are_all_axes_manual for a in avals) and
  #         all(a.sharding.mesh.are_all_axes_manual for a in out_avals) and
  #         get_abstract_mesh().are_all_axes_manual):
  #   raise ValueError("pallas_call requires all mesh axes to be Manual, "
  #                    f"got {get_abstract_mesh().axis_types}")

  # NOTE(mattjj,yashkatariya): this doesn't catch auto-mode non-manual axes
  if not (all(p is None for a in avals if isinstance(a, jax_core.ShapedArray)
              for p in a.sharding.spec) and
          all(p is None for a in out_avals if isinstance(a, jax_core.ShapedArray)
              for p in a.sharding.spec)):
    raise ValueError("pallas_call requires all mesh axes to be Manual, "
                     f"got {get_abstract_mesh().axis_types}")
  return out_avals, effs

