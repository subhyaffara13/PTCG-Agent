from typing import Any, Tuple

def _is_prefix(candidate, target):
    """Check whether `candidate` is a prefix of `target`."""
    return len(candidate) < len(target) and target[: len(candidate)] == candidate


def _is_prefix(t1: Tuple[Any, ...], t2: Tuple[Any, ...]) -> bool:
  """Checks if tuple t1 is a prefix of tuple t2."""
  return len(t1) < len(t2) and t2[: len(t1)] == t1


def _is_prefix(t1: tuple[str, ...], t2: tuple[str, ...]) -> bool:
  return len(t1) < len(t2) and t2[: len(t1)] == t1

