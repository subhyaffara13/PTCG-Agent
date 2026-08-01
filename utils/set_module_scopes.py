
def set_module_scopes(module, args, kwargs, scopes):
  """Set all scopes on module, including those on Modules in dataclass fields.

  To properly functionalize a Module we must also "rehydrate" it with Scopes
  from `get_module_scopes`.  We need to set scopes not just on the Module but
  also on any Module living inside dataclass attributes or even pytrees in its
  dataclass attributes.  We additionally handle restoring Variables and Module
  instances from their placeholders in the method positional and keyword
  arguments.  The order of traversal through this method is the same as in
  `get_module_scopes`, guaranteeing the correct Scopes are applied to each
  Module.

  Args:
    module: a flax Module.
    args: an *args list possibly containing VariablePlaceholder or
      InstancePlaceholder members.
    kwargs: a **kwargs dict possibly containing VariablePlaceholder or
      InstancePlaceholder members.
    scopes: a list of Scopes corresponding to this Module and its arguments that
      was created by the `get_module_scopes` function.

  Returns:
    A copy of the module with it and its attributes bound to the scopes passed
    to this function, an updated args list, and an updated kwargs dict with
    updated Variable and Module instance references.
  """
  idx = 0
  refs = {}

  # Set scopes associated with Variables and Module instances passed as
  # positional and keyword arguments.
  @functools.partial(_memoize_by_id, refs=refs)
  def set_arg_scope(x):
    nonlocal idx
    if isinstance(x, VariablePlaceholder):
      new_x = Variable(
        scope=scopes[idx], collection=x.collection, name=x.name, unbox=x.unbox
      )
      idx += 1
      return new_x
    elif isinstance(x, InstancePlaceholder):
      instance_scope = scopes[idx]
      idx += 1
      instance_attrs = jax.tree_util.tree_map(set_arg_scope, x.attrs)
      return x.cls(parent=instance_scope, **instance_attrs)
    return x

  def is_placeholder(x):
    return isinstance(x, (VariablePlaceholder, InstancePlaceholder))

  new_args, new_kwargs = jax.tree_util.tree_map(
    set_arg_scope, (args, kwargs), is_leaf=is_placeholder
  )

  # set scopes in Variables and Submodules passed as Module attributes
  @functools.partial(_memoize_by_id, refs=refs)
  def set_scopes(module):
    nonlocal idx

    def set_scopes_inner(x):
      nonlocal idx
      if isinstance(x, Module) and isinstance(x.scope, Scope):
        return set_scopes(x)
      elif isinstance(x, Variable) and isinstance(x.scope, Scope):
        new_x = Variable(
          scope=scopes[idx],
          collection=x.collection,
          name=x.name,
          unbox=x.unbox,
        )
        idx += 1
        return new_x
      else:
        return x

    attrs = {
      f.name: getattr(module, f.name)
      for f in dataclasses.fields(module)
      if f.name != 'parent' and f.init
    }
    new_attrs = jax.tree_util.tree_map(set_scopes_inner, attrs)
    new_module = module.clone(parent=scopes[idx], **new_attrs)
    idx += 1
    return new_module

  new_module = set_scopes(module)
  assert len(scopes) == idx, f'scope list mismatch {len(scopes)} != {idx}'
  return new_module, new_args, new_kwargs

