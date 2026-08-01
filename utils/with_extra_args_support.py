
def with_extra_args_support(
    tx: GradientTransformation,
) -> GradientTransformationExtraArgs:
  """Wraps a gradient transformation, so that it ignores extra args."""

  if isinstance(tx, GradientTransformationExtraArgs):
    return tx

  def update(updates, state, params=None, **extra_args):
    del extra_args
    return tx.update(updates, state, params)

  return GradientTransformationExtraArgs(tx.init, update)

