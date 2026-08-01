
def _overwrite_methods(env):
  "Overwrite methods with functions from an environment"
  for (obj_type, name), f in env.items():
    setattr(obj_type, name, f)

