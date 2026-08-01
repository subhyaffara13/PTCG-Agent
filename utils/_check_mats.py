
def _check_mats(mesh, specs, avals):
  fail = [a.mat if isinstance(sp, P) and not _valid_repeats(mesh, a.mat, sp)
          else no_fail for sp, a in zip(specs, avals)]
  if any(f is not no_fail for f in fail):
    raise _RepError(fail, avals.tree)

