
def _pp_transforms(
    context: core.JaxprPpContext,
    transforms: tuple[Transform, ...],
):
  if not transforms:
    return pp.text("[...]")
  return pp.concat(
      [transform.pretty_print(context) for transform in transforms]
  )

