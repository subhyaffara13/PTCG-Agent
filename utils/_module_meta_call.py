
def _module_meta_call(cls: type[M], *args, **kwargs) -> M:
  # compact behavior
  parent_ctx = MODULE_CONTEXT.module_stack[-1]
  parent = None
  module: M

  name = None
  if parent_ctx is not None:
    if 'parent' in kwargs:
      parent = kwargs.pop('parent')
      if parent_ctx.in_compact and parent is not None:
        raise ValueError(
          f"'parent' can only be set to None, got {type(parent).__name__}"
        )
    else:
      parent = parent_ctx.module

    if 'name' in kwargs:
      name = kwargs['name']
      if not 'name' in inspect.get_annotations(cls):
         kwargs.pop('name')
      if not isinstance(name, str):
        raise ValueError(f"'name' must be a 'str', got {type(name).__name__}")
    elif parent_ctx.in_compact:
      name = _auto_submodule_name(parent_ctx, cls)

  module = nnx_module.ModuleMeta.__call__(cls, *args, **kwargs)
  module.scope = None
  module.attr_priorities = {}

  if parent is not None:
    assert parent.scope is not None
    # compact, or setup if `name` exists
    if name is not None:
      setattr(parent, name, module)
      parent.set_attr_priority(name, AttrPriority.INIT_PARENT)

  return module  # type: ignore

