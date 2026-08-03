from typing import Callable, Optional

def parametrize_xnp(
    *,
    with_none: bool = False,
    restrict: Optional[Iterable[str]] = None,
    skip: Optional[Iterable[str]] = None,
) -> Callable[[_FnT], _FnT]:
  """Parametrize over the numpy modules.

  Args:
    with_none: If `True`, also yield `None` among the values (to test `list`)
    restrict: If given, only test the given module (e.g. `restrict=['jnp']`)
    skip: If given, skip the given module from test (e.g. `skip=['torch']`)

  Returns:
    The fixture to apply to the `def test_xyz()` function
  """
  name_to_modules = {
      'np': lambda: np,
      'jnp': lambda: lazy.jnp,
      'tnp': lambda: lazy.tnp,
      'torch': lambda: lazy.torch,
  }

  keep = _normalize_set(
      restrict, default=name_to_modules, valid=name_to_modules
  )
  skip = _normalize_set(skip, default=[], valid=name_to_modules)

  # Only resolve the `lambda:` for the modules actually tested
  name_to_modules = {
      k: v() for k, v in name_to_modules.items() if k not in skip and k in keep
  }

  if with_none:
    # Allow to test without numpy module: `x = [1, 2]` vs `x = np.array([1, 2]`
    name_to_modules['no_np'] = None

  return pytest.mark.parametrize(
      'xnp',
      list(name_to_modules.values()),
      ids=list(name_to_modules.keys()),
  )

