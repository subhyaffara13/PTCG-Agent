
def _round_lower(ctx, x, *, rounding_method):
  if rounding_method is RoundingMethod.AWAY_FROM_ZERO:
    return [hlo.round_nearest_afz(x)]
  else:
    assert rounding_method is RoundingMethod.TO_NEAREST_EVEN
    return [hlo.round_nearest_even(x)]

