
def _lift_linearized(jaxpr, in_avals, out_avals, out_known, consts, *tangents):
  tangents_ft = FlatTree.flatten(tangents)
  if tangents_ft.tree != in_avals.tree:
    raise TypeError(f"expected {in_avals.tree}, got {tangents_ft.tree}")

  tangent_avals = tangents_ft.map(core.typeof)
  for primal_aval, tangent_aval in zip(in_avals, tangent_avals):
    expected_tangent_aval  = primal_aval.to_tangent_aval()
    if not core.typecompat(expected_tangent_aval, tangent_aval):
      extra_msg = ''
      if (isinstance(primal_aval, core.ShapedArray) and
          isinstance(tangent_aval, core.ShapedArray) and
          primal_aval.mat != tangent_aval.mat):
        # TODO(yashkatariya): Tweak error.
        pvary_applications = []
        if left := tangent_aval.mat.varying - primal_aval.mat.varying:
          pvary_applications.append(
              f"applying `jax.lax.pcast(..., {tuple(left)}, to='varying')` to"
              " the primal value passed to `jax.linearize`")
        if left := primal_aval.mat.varying - tangent_aval.mat.varying:
          pvary_applications.append(
              f"applying `jax.lax.pcast(..., {tuple(left)}, to='varying')` to"
              " the tangent value passed to the callable `f_jvp` returned by"
              " `jax.linearize`")
        extra_msg = " \nThis might be fixed by:\n" + "\n".join(
            f"  * {d};" for d in pvary_applications)
      raise ValueError(
          "linearized function called on tangent values inconsistent with "
          "the original primal values:\n"
          f"Got tangent aval {tangent_aval} for primal aval {primal_aval} "
          f"but expected {expected_tangent_aval}.{extra_msg}")
  tangents_out = eval_jaxpr(jaxpr, consts, *tangents_ft)
  tangents_out_ = iter(tangents_out)
  full_out = [a2tz(aval).instantiate() if known else next(tangents_out_)
              for aval, known in zip(out_avals, out_known)]
  assert next(tangents_out_, None) is None
  return out_avals.update(full_out).unflatten()

