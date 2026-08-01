
def _check_names(specs, avals: FlatTree) -> None:
  fail = [a if isinstance(sp, P) and sp and len(sp) > a.ndim else no_fail
          for sp, a in zip(specs, avals)]
  if any(f is not no_fail for f in fail):
    raise _SpecError(fail, avals.tree)

