import functools

def get_module_scopes(module, args=None, kwargs=None):
  """Get all scopes on module, including constructor Module arguments.

  To properly functionalize a Module that has other bound Modules passed in
  "from the outside" as dataclass attributes, we need to traverse all dataclass
  fields to find the Scopes associated with the Module.  Additionally, because
  we allow Modules to be passed inside pytrees on the dataclass attributes, we
  must traverse all dataclass attributes as pytrees to find all Modules.  We
  additionally handle lifting Variables (which are just references to data in
  particular scopes) and Module instances that are passed as arguments to
  methods.

  Args:
    module: a bound flax Module.
    args: an *args list possibly containing Variables or Module instances
      referencing a scope.
    kwargs: a **kwargs dict possibly containing Variables or Module instances
      referencing a scope.

  Returns:
    A list of all functional-core Scopes bound on self and inside dataclass
    fields as well as any Scopes passed via argument Variables, an updated args
    list, and an updated kwargs dict that have both had Variables replaced with
    VariablePlaceholders and Module instances replaced with InstancePlaceholders
    that are compatible with jax functions.
  """
  scopes: list[Scope] = []
  refs = {}

  # Gather scopes associated with Variables and Module instances passed as
  # positional and keyword arguments.
  @functools.partial(_memoize_by_id, refs=refs)
  def get_arg_scope(x):
    nonlocal scopes
    if isinstance(x, Variable) and isinstance(x.scope, Scope):
      scopes.append(x.scope)
      return VariablePlaceholder(x.collection, x.name, x.unbox, x._id)
    elif isinstance(x, Module) and isinstance(x.scope, Scope):
      x._try_setup(shallow=True)
      scopes.append(x.scope)
      attrs = {
        f.name: getattr(x, f.name)
        for f in dataclasses.fields(x)
        if f.name != 'parent' and f.init
      }
      attrs = jax.tree_util.tree_map(get_arg_scope, attrs)
      return InstancePlaceholder(x.__class__, attrs, x._id)
    return x

  new_args, new_kwargs = jax.tree_util.tree_map(get_arg_scope, (args, kwargs))

  # Gather scopes in Variables and Submodules passed as Module attributes.
  @functools.partial(_memoize_by_id, refs=refs)
  def get_scopes(module):
    nonlocal scopes
    module._try_setup(shallow=True)

    def get_scopes_inner(x):
      nonlocal scopes
      if isinstance(x, Module) and isinstance(x.scope, Scope):
        get_scopes(x)
      elif isinstance(x, Variable) and isinstance(x.scope, Scope):
        scopes.append(x.scope)

    attrs = {
      f.name: getattr(module, f.name)
      for f in dataclasses.fields(module)
      if f.name != 'parent' and f.init
    }
    for leaf in jax.tree_util.tree_leaves(attrs):
      get_scopes_inner(leaf)
    scopes.append(module.scope)

  get_scopes(module)
  return scopes, new_args, new_kwargs

