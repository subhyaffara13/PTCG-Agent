
def _primal_tangent_shapes_match(primal, tangent):
  if type(tangent) is not Zero:
    primal_aval = typeof(primal).strip_weak_type()
    tangent_aval = typeof(tangent).strip_weak_type()
    if not isinstance(primal_aval, core.ShapedArray):
      return  # TODO(mattjj,dougalm)
    assert core.definitely_equal_shape(primal_aval.shape, tangent_aval.shape), (
        primal_aval.shape, tangent_aval.shape)
    expected_tangent_dtype = core.primal_dtype_to_tangent_dtype(primal_aval.dtype)
    assert expected_tangent_dtype == tangent_aval.dtype, (
        expected_tangent_dtype, tangent_aval.dtype)
    if (not primal_aval.sharding.mesh.empty and
        not tangent_aval.sharding.mesh.empty and
        (primal_aval.sharding.mesh._any_axis_explicit or
         tangent_aval.sharding.mesh._any_axis_explicit)):
      assert primal_aval.sharding == tangent_aval.sharding, (
          primal_aval.sharding, tangent_aval.sharding)

