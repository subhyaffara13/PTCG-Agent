import itertools

def _inline_mgpu_abstract_eval(
    *flat_args_and_transforms,
    flat_arg_types,
    flat_ret_ty,
    pytree_args,
    pytree_ref_transforms,
    pytree_ret_ty,
    mgpu_fn,
):
  del flat_arg_types, pytree_ret_ty, pytree_ref_transforms, mgpu_fn  # Unused.
  aval_return = tuple(
      jax_core.ShapedArray(x.shape, x.dtype) for x in flat_ret_ty
  )
  # TODO(cperivol): Let the user set the effects.
  flat_args = flat_args_and_transforms[:pytree_args.num_leaves]
  return aval_return, {
      gpu_core._wgmma_pipeline_effect,
      gpu_core._memory_effect,
      *itertools.chain.from_iterable(
          (state.ReadEffect(i), state.WriteEffect(i))
          for i, r in enumerate(flat_args)
          if isinstance(r, state.AbstractRef)
      ),
  }

