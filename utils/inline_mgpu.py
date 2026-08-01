
def inline_mgpu(*, arg_types=(), return_type=None):
  r"""Returns a decorator that inlines Mosaic GPU code.

  This allows using lower-level Mosaic GPU abstractions and operations, which
  are otherwise not directly exposed in Pallas.

  Example::

      layout = plgpu.Layout.WG_STRIDED(x_ref.shape, vec_size=4)

      @plgpu.inline_mgpu(
          arg_types=(plgpu.RefType(),),
          return_type=plgpu.ShapeDtypeStruct(
              (128, 128), dtype, layout=layout
          ),
      )
      def add_one(ctx, smem_ref):
        x = mgpu.FragmentedArray.load_tiled(smem_ref)
        y = mgpu.FragmentedArray.splat(
            mgpu.c(1, x.mlir_dtype), shape=x.shape, layout=x.layout
        )
        return x + y

  Args:
    arg_types: A sequence of pytrees where the leaves are
      :class:`~jax.experimental.pallas.mosaic_gpu.RefType`\s or
      :class:`~jax.experimental.pallas.mosaic_gpu.Layout`\s for reference or
      array arguments respectively.
    return_type: A pytree where the leaves are
      :class:`~jax.experimental.pallas.mosaic_gpu.ShapeDtypeStruct`\s
      representing the arrays returned by the decorated function.
  """
  flat_arg_types, treedef_ty = jax.tree.flatten(tuple(arg_types))
  flat_ret_ty, pytree_ret_ty = jax.tree.flatten(return_type)
  if return_type and not all(isinstance(r, ShapeDtypeStruct) for r in flat_ret_ty):
    raise ValueError(
        "inline_mgpu_p only supports plgpu.ShapeDtypeStruct return types."
    )
  if not all(isinstance(r, (SomeLayout, RefType)) for r in flat_arg_types):
    raise ValueError(
        "inline_mgpu_p only supports only SomeLayout and RefType arg types."
    )

  def inner(f):
    def wrapper(*args):
      flat_args, treedef = jax.tree.flatten(tuple(args))
      if treedef != treedef_ty:
        raise ValueError(f"Mismatched type shape: {treedef} != {treedef_ty}")

      # Strip the transforms from the refs since they will be recorded in
      # the types.
      ref_transforms: list[Any] = []
      raw_flat_args = []
      for a, t in zip(flat_args, flat_arg_types):
        if isinstance(a, state_types.TransformedRef) and isinstance(t, RefType):
          raw_flat_args.append(a.ref)
          ref_transforms.append(a.transforms)
        elif isinstance(aval := jax_core.typeof(a), jax_core.ShapedArray) and isinstance(t, SomeLayout):
          raw_flat_args.append(a)
          ref_transforms.append(None)
        elif isinstance(aval, state.AbstractRef) and isinstance(t, RefType):
          raw_flat_args.append(a)
          ref_transforms.append(())
        else:
          raise ValueError(f"Mismatched type: {a, t}")

      flat_ref_transforms, pytree_ref_transforms = jax.tree.flatten(ref_transforms)
      flat_ret = inline_mgpu_p.bind(
          *raw_flat_args,
          *flat_ref_transforms,
          flat_arg_types=tuple(flat_arg_types),
          flat_ret_ty=tuple(flat_ret_ty),
          pytree_ret_ty=pytree_ret_ty,
          pytree_args=treedef,
          pytree_ref_transforms=pytree_ref_transforms,
          mgpu_fn=f,
      )
      return jax.tree.unflatten(pytree_ret_ty, flat_ret)
    return wrapper

  return inner

