
def _flatten_sharding(tree, shardings, shapes):
  return [
      _to_hlo_sharding(sharding, len(shape.dimensions()))
      for sharding, shape in zip(
          tree.flatten_up_to(shardings), shapes
      )
  ]

