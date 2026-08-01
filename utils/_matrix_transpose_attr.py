
def _matrix_transpose_attr(transpose: bool, conjugate: bool):
  return _char_attr(("C" if conjugate else "T") if transpose else "N")

