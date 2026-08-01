
def _custom_primitive_in_specs(
    ctx: lowering.LoweringRuleContext,
    flat_arg_types,
    flat_transformed_args,
    pytree_args,
) -> tuple[Sequence[ir.Type], Sequence[ir.Attribute], Sequence[ir.ArrayAttr]]:
  """Returns a tuple containing the list of MLIR input types, layouts, and
  transforms for the given JAX array and ref arguments."""
  in_types : list[ir.Type] = []
  in_layouts : list[ir.Attribute] = []
  in_transforms : list[ir.ArrayAttr] = []
  flat_arg_avals = ctx.avals_in[:pytree_args.num_leaves]
  for aval, transformed, t in zip(
      flat_arg_avals, flat_transformed_args, flat_arg_types
  ):
    match aval:
      case state.AbstractRef():
        initial_ty = ir.MemRefType(transformed.type)
        in_types.append(initial_ty)
        if mgpu_utils.is_smem_ref(initial_ty):
          in_transforms.append(_ref_type_to_transforms(t))
      case jax_core.ShapedArray() if isinstance(t, SomeLayout):
        el_type = mgpu_utils.dtype_to_ir_type(aval.dtype)
        if len(aval.shape) == 0:
          in_types.append(el_type)
        else:
          vector_type = ir.VectorType.get(aval.shape, el_type)
          in_types.append(vector_type)
          in_layouts.append(mgpu_layouts.to_layout_attr(t.to_mgpu()))
      case _:
        raise NotImplementedError(
            f"Unsupported aval type: {aval}, {type(aval)}, {t}"
        )
  return in_types, in_layouts, in_transforms

