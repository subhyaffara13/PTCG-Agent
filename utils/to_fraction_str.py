
def to_fraction_str(x, lrsnash_max_denom):
  return str(fractions.Fraction(x).limit_denominator(lrsnash_max_denom))

