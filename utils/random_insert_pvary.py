
def random_insert_pvary(name, key, *args):
  if not config._check_vma.value or not config.auto_pcast.value:
    return key, args
  if not args:
    return key, args
  key_vma = core.typeof(key).mat.varying
  out = []
  for a in args:
    arg_vma = (aval.mat.varying
               if isinstance(aval := core.typeof(a), core.ShapedArray)
               else frozenset())
    # If key is less varying than the args, then it's an error and user should
    # pvary at their level because it has key-reuse implications. They can
    # shard the keys passed to shard_map correctly so as to avoid key-reuse
    # getting correctly varying keys. But JAX shouldn't auto-pvary the key.
    if key_vma - arg_vma:
      a = core.pvary(a, tuple(k for k in key_vma if k not in arg_vma))
    if core.typeof(key).mat != core.typeof(a).mat:
      raise TypeError(
          f"{name} requires all arguments to have matching type. Got key type:"
          f" {core.typeof(key)} vs arg type: {core.typeof(a)}. Use"
          " jax.lax.pcast(..., to='varying') to make them match. If your key is"
          " less varying than arg, watch out for key-reuse problems.")
    out.append(a)
  return key, out

