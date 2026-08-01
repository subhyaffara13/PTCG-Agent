
def natural_sort(file_list: Iterable[str], signed: bool = True) -> list[str]:
  """Natural sort for filenames with numerical substrings.

  Args:
    file_list: list of paths to sort containing numerical substrings.
    signed: bool: if leading '-' (or '+') signs should be included in numerical
      substrings as a sign or treated as a separator.

  Returns:
    List of filenames sorted 'naturally', not lexicographically: any
    integer substrings are used to subsort numerically. e.g.
    file_1, file_10, file_2  -->  file_1, file_2, file_10
    file_0.1, file_-0.2, file_2.0  -->  file_-0.2, file_0.1, file_2.0
  """
  float_re = SIGNED_FLOAT_RE if signed else UNSIGNED_FLOAT_RE

  def maybe_num(s):
    if float_re.match(s):
      return float(s)
    else:
      return s

  def split_keys(s):
    return [maybe_num(c) for c in float_re.split(s)]

  return sorted(file_list, key=split_keys)

