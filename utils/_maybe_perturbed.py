
def _maybe_perturbed(x: Any) -> bool:
  # False if x can't represent an AD-perturbed value (i.e. a value
  # with a nontrivial tangent attached), up to heuristics, and True otherwise.
  # See https://github.com/jax-ml/jax/issues/6415 for motivation.
  if not isinstance(x, core.Tracer):
    # If x is not a Tracer, it can't be perturbed.
    return False
  elif isinstance(x, ad.JVPTracer) and isinstance(x.tangent, ad.Zero):
    return _maybe_perturbed(x.primal)
  elif isinstance(x, pe.DynamicJaxprTracer):
    # If x is a DynamicJaxprTracer then we're staging out; differentiation could
    # happen later, but some types always have trivial tangents.
    vspace = x.aval.to_tangent_aval()
    return not (vspace is core.abstract_token or
                getattr(vspace, 'dtype', None) == dtypes.float0)
  elif not isinstance(x, ad.JVPTracer):
    # If x is not a JVPTracer, recursively check its contents.
    return any(_maybe_perturbed(attr) for name, attr in x._contents())
  else:
    return True  # We can't be sure!

