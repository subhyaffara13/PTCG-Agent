
def with_mesh_from_kwargs(f):
  return lambda *args, **kwargs: with_mesh(kwargs['mesh'])(f)(*args, **kwargs)

