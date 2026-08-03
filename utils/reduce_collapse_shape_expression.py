import math


def reduce_collapse_shape_expression(
    expr: CollapseShape, assignments: dict[Variable, Constant]
) -> Expression | Unsatisfiable:
  reduced_expr = reduce_expression(expr.expression, assignments)
  match reduced_expr:
    case Unsatisfiable():
      return Unsatisfiable()
    case SMEMTransforms(tiling=tile_transform):
      if tile_transform is None:
        return SMEMTransforms(None)
      tiling = tile_transform.tiling
      rev_tiling_to_process = list(tiling)[::-1]
      rev_shape_to_process = expr.source_shape[-len(tiling):][::-1]
      # Ensure that the provided tiling applies to the shape. Otherwise, the
      # expression is unsatisfiable.
      for s, t in zip(rev_shape_to_process, rev_tiling_to_process):
        if s % t != 0:
          return Unsatisfiable()
      rev_new_tiling: list[int] = []
      for ndim in expr.reassociation[::-1]:
        # Collapsing tiled dimensions into untiled dimensions is not
        # supported. While there is a reasonable way of handling this case in
        # particular situations, we forbid it in the semantics of
        # `CollapseShape`.
        if len(rev_tiling_to_process) < ndim:
          return Unsatisfiable()

        rev_tiling_slice = rev_tiling_to_process[:ndim]
        rev_shape_slice = rev_shape_to_process[:ndim]
        new_tiling_dim = math.prod(rev_tiling_slice)
        num_elems = math.prod(rev_shape_slice)
        assert num_elems % new_tiling_dim == 0
        # We can collapse dimensions when the tiling is of the form
        # (1*, partial_dim?, full_dim*)---i.e. when it contains any number of
        # leading unit dimensions, followed by at most one arbitrary non-unit
        # dimension, and any number of trailing "full" dimensions (where the
        # tiling size equals the dimension size).
        #
        # Here, the tiling and shape are reversed, so we look for the pattern
        # (full_dim*, partial_dim?, 1*).
        suffix_length = 0
        for t, s in zip(rev_tiling_slice, rev_shape_slice):
          if t != s:
            break
          suffix_length += 1
        if (rev_unsuffixed_tiling := rev_tiling_slice[suffix_length:]):
          # Ignore the partial dimension, since it can be anything.
          _, *rev_prefix_tiling = rev_unsuffixed_tiling
          if any(t != 1 for t in rev_prefix_tiling):
            return Unsatisfiable()
        rev_new_tiling.append(new_tiling_dim)
        rev_tiling_to_process = rev_tiling_to_process[ndim:]
        rev_shape_to_process = rev_shape_to_process[ndim:]
        if not rev_tiling_to_process:
          break
      assert not rev_tiling_to_process
      assert not rev_shape_to_process
      new_tiling = tuple(rev_new_tiling[::-1])
      return SMEMTransforms(lc.TileTransform(tuple(new_tiling)))
    case Constant():
      raise NotImplementedError(
          "CollapseShape is only implemented for variables in SMEM")
    case _:
      return dataclasses.replace(expr, expression=reduced_expr)

