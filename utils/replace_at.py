
def replaceAt(string: str, index: int, ch: str) -> str:
    # When the index is negative, the behavior is different from the js version.
    # But basically, the index will not be negative.
    assert index >= 0
    return string[:index] + ch + string[index + 1 :]


def replace_at(t: tuple, index: int, value: tp.Any) -> tuple:
  return tuple(
    value if i == index else x
    for i, x in enumerate(t)
  )

