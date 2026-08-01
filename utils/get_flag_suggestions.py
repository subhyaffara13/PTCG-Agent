
def get_flag_suggestions(
    attempt: str, longopt_list: Sequence[str]
) -> list[str]:
  """Returns helpful similar matches for an invalid flag."""
  # Don't suggest on very short strings, or if no longopts are specified.
  if len(attempt) <= 2 or not longopt_list:
    return []

  option_names = [v.split('=')[0] for v in longopt_list]

  # Find close approximations in flag prefixes.
  # This also handles the case where the flag is spelled right but ambiguous.
  distances = [(_damerau_levenshtein(attempt, option[0:len(attempt)]), option)
               for option in option_names]
  # t[0] is distance, and sorting by t[1] allows us to have stable output.
  distances.sort()

  least_errors, _ = distances[0]
  # Don't suggest excessively bad matches.
  if least_errors >= _SUGGESTION_ERROR_RATE_THRESHOLD * len(attempt):
    return []

  suggestions = []
  for errors, name in distances:
    if errors == least_errors:
      suggestions.append(name)
    else:
      break
  return suggestions

