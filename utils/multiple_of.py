
def multipleOf(validator, dB, instance, schema):
    if not validator.is_type(instance, "number"):
        return

    if isinstance(dB, float):
        quotient = instance / dB
        try:
            failed = int(quotient) != quotient
        except OverflowError:
            # When `instance` is large and `dB` is less than one,
            # quotient can overflow to infinity; and then casting to int
            # raises an error.
            #
            # In this case we fall back to Fraction logic, which is
            # exact and cannot overflow.  The performance is also
            # acceptable: we try the fast all-float option first, and
            # we know that fraction(dB) can have at most a few hundred
            # digits in each part.  The worst-case slowdown is therefore
            # for already-slow enormous integers or Decimals.
            failed = (Fraction(instance) / Fraction(dB)).denominator != 1
    else:
        failed = instance % dB

    if failed:
        yield ValidationError(f"{instance!r} is not a multiple of {dB}")


def multiple_of(x: jax_typing.Array, values: Sequence[int] | int) -> jax_typing.Array:
  """A compiler hint that asserts a value is a static multiple of another.

  Note that misusing this function, such as asserting ``x`` is a multiple of
  ``N`` when it is not, can result in undefined behavior.

  Args:
    x: The input array.
    values: A set of static divisors that ``x`` is a multiple of.

  Returns:
    A copy of ``x``.
  """
  values = (values,) if isinstance(values, int) else tuple(values)
  return multiple_of_p.bind(x, values=values)

