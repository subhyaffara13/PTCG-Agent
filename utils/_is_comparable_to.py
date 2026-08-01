
def _is_comparable_to(self, other):
    """
    Check whether `other` is comparable to `self`.
    """
    return all(func(self, other) for func in self._requirements)

