
def average_incrementally_updates(
    per_elt_axis: MaybeAxis, accumulation_steps: int
) -> Aggregator | base.GradientTransformation:
  """Average and accumulate per-element updates.

  Args:
    per_elt_axis: The axis to average over, or None if no averaging is desired.
    accumulation_steps: The number of microbatches to accumulate over.

  Returns:
    An optax GradientTransformation or an Aggregator that averages and/or
    accumulates per-element updates.
  """
  if per_elt_axis is None:
    return accumulate_avg_updates(accumulation_steps)
  else:
    agg = _combining.chain(
        average_per_element_updates(per_elt_axis),
        accumulate_avg_updates(accumulation_steps),
    )
    return Aggregator(agg.init, agg.update)

