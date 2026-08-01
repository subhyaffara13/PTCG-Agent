
def _reshard_transpose_fancy(ct, x, *, dst_sharding, concrete_mesh):
  assert isinstance(x, ad.GradAccum)
  if type(ct) is ad.Zero or isinstance(x, ad.NullAccum):
    return
  out_sharding = x.aval.sharding  # pyrefly: ignore[missing-attribute]
  with mesh_lib.use_abstract_mesh(out_sharding.mesh):
    x_bar = reshard_p.bind(ct, dst_sharding=out_sharding,
                           concrete_mesh=concrete_mesh)
    x.accum(x_bar)

