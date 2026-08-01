
def _assert_no_intersection(static_argnames, donate_argnames):
  out = set(static_argnames).intersection(set(donate_argnames))
  if out:
    raise ValueError(
        "static_argnames and donate_argnames cannot intersect. Argument names "
        f"{out} appear in both static_argnames and donate_argnames")

