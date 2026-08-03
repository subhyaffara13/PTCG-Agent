from typing import Optional

def scale_by_learning_rate(
    learning_rate: Optional[base.ScalarOrSchedule] = None,
    *,
    flip_sign: bool = True,
) -> base.GradientTransformation:
  """Scale by the (negative) learning rate (either as scalar or as schedule).

  Args:
    learning_rate: Can either be a scalar or a schedule (i.e. a callable that
      maps an (int) step to a float). None means no scaling.
    flip_sign: When set to True (the default) this corresponds to scaling by the
      negative learning rate.

  Returns:
    An optax.GradientTransformation that corresponds to multiplying the gradient
    with `-learning_rate` (if flip_sign is True) or with `learning_rate` (if
    flip_sign is False).
  """
  if learning_rate is None:
    return base.identity()
  m = -1 if flip_sign else 1
  if callable(learning_rate):
    return scale_by_schedule(lambda count: m * learning_rate(count))
  return scale(m * learning_rate)

