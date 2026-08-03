import itertools

def assign_layouts(solution: dict[ValueSite, cs.Constant]) -> None:
  """Assigns the layouts in `solution` to the MLIR ops they belong to.

  This function requires that, for each MLIR op that appears in `solution`,
  `solution` contains a layout assignment for all of its `vector`, TMEM, and
  SMEM operands and results. Block arguments are ignored.
  """
  solution_sorted_by_op = sorted(
      solution.items(), key=lambda kv: id(kv[0].operation)
  )
  solution_per_op = itertools.groupby(
      solution_sorted_by_op, key=lambda kv: kv[0].operation
  )

  for op, assignments in solution_per_op:
    assignments_sorted_by_type = sorted(assignments, key=lambda kv: kv[0].type)
    assignments_by_type = {
        ty: list(group)
        for ty, group in itertools.groupby(
            assignments_sorted_by_type, key=lambda kv: kv[0].type
        )
    }

    in_assignments = assignments_by_type.get(VariableType.OPERAND, [])
    out_assignments = assignments_by_type.get(VariableType.RESULT, [])

    index = lambda kv: kv[0].index
    in_tls = [
        _TypeAndLayout(v.value.type, ce)
        for v, ce in sorted(in_assignments, key=index)
    ]
    out_tls = [
        _TypeAndLayout(v.value.type, ce)
        for v, ce in sorted(out_assignments, key=index)
    ]

    in_layouts = [
        tl.layout.value
        for tl in in_tls
        if isinstance(tl.layout, cs.RegisterLayout)
    ]
    out_layouts = [
        tl.layout.value
        for tl in out_tls
        if isinstance(tl.layout, cs.RegisterLayout)
    ]
    in_tmem_layouts = [
        tl.layout.value for tl in in_tls if isinstance(tl.layout, cs.TMEMLayout)
    ]
    out_tmem_layouts = [
        tl.layout.value
        for tl in out_tls
        if isinstance(tl.layout, cs.TMEMLayout)
    ]
    in_transforms = [
        tl for tl in in_tls if isinstance(tl.layout, cs.SMEMTransforms)
    ]
    out_transforms = [
        tl for tl in out_tls if isinstance(tl.layout, cs.SMEMTransforms)
    ]

    if inference_utils.should_have_in_layout(op):
      attrs = [layouts_lib.to_layout_attr(l) for l in in_layouts]
      op.attributes["in_layouts"] = ir.ArrayAttr.get(attrs)
    if inference_utils.should_have_out_layout(op):
      attrs = [layouts_lib.to_layout_attr(l) for l in out_layouts]
      op.attributes["out_layouts"] = ir.ArrayAttr.get(attrs)
    if inference_utils.should_have_in_tmem_layout(op):
      attrs = [layouts_lib.to_layout_attr(l) for l in in_tmem_layouts]
      op.attributes["in_tmem_layouts"] = ir.ArrayAttr.get(attrs)
    if inference_utils.should_have_out_tmem_layout(op):
      attrs = [layouts_lib.to_layout_attr(l) for l in out_tmem_layouts]
      op.attributes["out_tmem_layouts"] = ir.ArrayAttr.get(attrs)

    def _to_transform_attrs(
        transforms: list[_TypeAndLayout],
    ) -> list[ir.ArrayAttr]:
      all_attrs: list[ir.ArrayAttr] = []
      for tl in transforms:
        assert isinstance(tl.layout, cs.SMEMTransforms)
        attrs = []
        if tl.layout.tiling is not None:
          attrs.append(layouts_lib.to_transform_attr(tl.layout.tiling))
          swizzle = _compute_swizzle(tl.type, tl.layout.tiling)
          attrs.append(layouts_lib.to_transform_attr(swizzle))
        all_attrs.append(ir.ArrayAttr.get(attrs))
      return all_attrs

    if inference_utils.should_have_in_transforms(op):
      attrs = _to_transform_attrs(in_transforms)
      op.attributes["in_transforms"] = ir.ArrayAttr.get(attrs)
    if inference_utils.should_have_out_transforms(op):
      attrs = _to_transform_attrs(out_transforms)
      op.attributes["out_transforms"] = ir.ArrayAttr.get(attrs)

    _ensure_all_layouts_are_set(op)

