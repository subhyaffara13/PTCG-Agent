
def _format_chance_outcomes(chance_outcomes):
  return "[" + ", ".join(["({},{})".format(outcome, _format_float(prob))
                          for (outcome, prob) in chance_outcomes]) + "]"

