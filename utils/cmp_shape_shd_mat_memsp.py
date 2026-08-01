
def cmp_shape_shd_mat_memsp(t1, t2):
  # TODO(yashkatariya): Expand this to Manual and Auto mode.
  # See https://github.com/jax-ml/jax/issues/26474
  t1_mesh, t2_mesh = t1.sharding.mesh, t2.sharding.mesh
  if not t1_mesh.empty and not t2_mesh.empty:
    if t1_mesh._any_axis_explicit or t2_mesh._any_axis_explicit:
      shd_eq = t1.sharding == t2.sharding
    else:
      shd_eq = True
  else:
    shd_eq = True
  return (shd_eq and definitely_equal_shape(t1.shape, t2.shape) and
          t1.mat == t2.mat and t1.memory_space == t2.memory_space)

