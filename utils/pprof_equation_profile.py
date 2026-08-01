
def pprof_equation_profile(jaxpr: core.Jaxpr, *,
                           workspace_root: str | None = None) -> bytes:
  """Generates a pprof profile that maps jaxpr equations to Python stack traces.

  By visualizing the profile using pprof, one can identify Python code that is
  responsible for yielding large numbers of jaxpr equations.

  Args:
    jaxpr: a Jaxpr.
    workspace_root: the root of the workspace. If specified, function names
      will be fully qualified, with respect to the workspace root.

  Returns:
    A gzip-compressed pprof Profile protocol buffer, suitable for passing to
    pprof tool for visualization.
  """
  d = Counter(
      (tb, eqn.primitive)
      for tb, eqn in _all_eqns_with_traceback(jaxpr, None, set())
  )
  comment = jaxpr.debug_info.func_name
  if func_filename := jaxpr.debug_info.func_filename:
    if workspace_root is not None:
      func_filename = _strip_workspace_root(func_filename, workspace_root)
    comment += f" at {func_filename}"
  if func_lineno := jaxpr.debug_info.func_lineno:
    comment += f":{func_lineno}"
  return _pprof_profile(
      d,
      workspace_root,
      sample_type="equations",
      sample_unit="count",
      comment=comment,
  )

