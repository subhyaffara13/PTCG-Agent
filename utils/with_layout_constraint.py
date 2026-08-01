
def with_layout_constraint(x, layouts):
  x_flat, tree = tree_flatten(x)
  x_avals_flat = [core.shaped_abstractify(x) for x in x_flat]
  layouts_flat = tuple(flatten_axes("with_layout_constraint layouts", tree,
                                    layouts))
  if any(not isinstance(l, Layout) for l in layouts_flat):
    raise ValueError(
        'layouts passed to `with_layout_constraint` must be of type'
        f' `Layout`. Got {[type(l) for l in layouts_flat]}')
  check_aval_layout_compatibility(
      layouts_flat, x_avals_flat, ("",) * len(layouts_flat),
      "with_layout_constraint arguments")
  outs = [layout_constraint_p.bind(xf, layout=l)
          for xf, l in zip(x_flat, layouts_flat)]
  return tree_unflatten(tree, outs)

