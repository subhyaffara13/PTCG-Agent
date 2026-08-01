
def _bubble_up_transforms_for_lowering(
    ctx: LoweringRuleContext,
    aval: jax_core.AbstractValue,
    transforms: Sequence[state_types.Transform],
    transform_avals: Sequence[state_types.Transform],
    *,
    handle_transposes: bool = True,
    handle_reshapes: bool = True,
) -> tuple[
    list[state_types.Transform],
    list[state_types.Transform],
    list[state_types.Transform],
    list[state_types.Transform],
]:
  """Bubbles up eligible `transforms` to the head of the sequence.

  The transforms to lower are commuted to the head of the sequence of
  transforms, such that the (unmaterialized) new order of transform
  application is:

    (*transforms_to_lower, *remaining_transforms)

  Returns a tuple where:
    * first element is a list of bubbled up transforms (i.e.,
    `transforms_to_lower`)
    * second element is a list of avals corresponding to bubbled up transforms
    * third element is a list of remaining transforms (i.e.,
    `remaining_transforms`)
    * fourth element is a list of avals corresponding to remaining transforms
  """
  bubbled_up_transforms = []
  bubbled_up_transform_avals = []
  remaining_transforms = []
  remaining_transform_avals = []

  for t_aval, t in zip(transform_avals, transforms):
    match t:
      case TransposeTransform():
        should_bubble_up = handle_transposes
      case ReshapeTransform():
        should_bubble_up = handle_reshapes
      case (
          indexing.NDIndexer()
          | gpu_core.PeerMemRef()
          | gpu_core.MulticastRef()
          | gpu_core.ClusterRefTransform()
      ):
        should_bubble_up = True
      case _:
        should_bubble_up = False

    if should_bubble_up:
      (
          t,
          t_aval,
          remaining_transforms,
          remaining_transform_avals,
      ) = _bubble_up_transform(
          ctx,
          aval,
          remaining_transforms,
          remaining_transform_avals,
          t,
          t_aval,
      )
      bubbled_up_transforms.append(t)
      bubbled_up_transform_avals.append(t_aval)
      aval = t_aval.transform_type(aval)
    else:
      remaining_transforms.append(t)
      remaining_transform_avals.append(t_aval)

  assert len(bubbled_up_transforms) == len(bubbled_up_transform_avals)
  assert len(remaining_transforms) == len(remaining_transform_avals)
  return (
      bubbled_up_transforms,
      bubbled_up_transform_avals,
      remaining_transforms,
      remaining_transform_avals,
  )

