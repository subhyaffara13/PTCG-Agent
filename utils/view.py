from typing import Any, Callable

def view(path: str, handler: type[AbstractView], **kwargs: Any) -> RouteDef:
    return route(hdrs.METH_ANY, path, handler, **kwargs)


def view(view_: Type[ViewType]) -> Callable[[_F], _F]:
    """Decorator"""

    def decorate(f: _F) -> _F:
        _logger.debug('Registering %s.%s with View: %s', f.__module__, f.__qualname__, view_)
        ObjectMetadataLibrary.register_property_view(
            qual_name=f'{f.__module__}.{f.__qualname__}', view_=view_
        )
        return f

    return decorate


def view(self: list[int], sizes: list[int]):
    return infer_size_impl(sizes, numel(self))


def view(x: TensorBox, sizes: Sequence[sympy.Expr]) -> TensorBox:
    return TensorBox(View.create(x.data, sizes))


def view(a: TensorLikeType, *shape: ShapeType | tuple[ShapeType]) -> TensorLikeType:
    from torch._subclasses.fake_impls import (
        _view_has_unbacked_input,
        _view_unbacked_meta,
    )

    # Cast to satisfy the type checker since the varargs annotation creates
    # tuple[ShapeType | tuple[ShapeType], ...] but the function expects
    # Union[ShapeType, tuple[ShapeType]].
    shape_tuple = utils.extract_shape_from_varargs(
        cast(ShapeType | tuple[ShapeType], shape), validate=False
    )
    if torch.fx.experimental._config.backed_size_oblivious or _view_has_unbacked_input(
        a,
        shape_tuple,
    ):
        return _view_unbacked_meta(a, shape_tuple)
    return _reshape_view_helper(a, *shape, allow_copy=False)


def view(g: jit_utils.GraphContext, self, size):
    return reshape(g, self, size)


def view(result: _ods_ir.Type, source: _ods_ir.Value[_ods_ir.MemRefType], byte_shift: _ods_ir.Value[_ods_ir.IndexType], sizes: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.MemRefType]:
  return ViewOp(result=result, source=source, byte_shift=byte_shift, sizes=sizes, loc=loc, ip=ip).result


def view(node: A, /, *, only: filterlib.Filter = ..., raise_if_not_found: bool = True, graph: bool | None = None, **kwargs) -> A:
  """Creates a new node with static attributes updated according to ``**kwargs``.

  The new node contains references to jax arrays in the original node. If a
  kwarg is not found in any module, this method raises a ValueError. Uses the
  ``set_view`` class method in nnx.Modules. ``set_view`` class methods should
  return any unused kwargs.

  Example::
    >>> from flax import nnx
    ...
    >>> class Block(nnx.Module):
    ...   def __init__(self, din, dout, *, rngs: nnx.Rngs):
    ...     self.linear = nnx.Linear(din, dout, rngs=rngs)
    ...     self.dropout = nnx.Dropout(0.5)
    ...     self.batch_norm = nnx.BatchNorm(10, rngs=rngs)
    ...
    >>> block = Block(2, 5, rngs=nnx.Rngs(0))
    >>> block.dropout.deterministic, block.batch_norm.use_running_average
    (False, False)
    >>> new_block = nnx.view(block, deterministic=True, use_running_average=True)
    >>> new_block.dropout.deterministic, new_block.batch_norm.use_running_average
    (True, True)

  ``Filter``'s can be used to set the attributes of specific Modules::
    >>> block = Block(2, 5, rngs=nnx.Rngs(0))
    >>> new_block = nnx.view(block, only=nnx.Dropout, deterministic=True)
    >>> # Only the dropout will be modified
    >>> new_block.dropout.deterministic, new_block.batch_norm.use_running_average
    (True, False)

  Args:
    node: the object to create a copy of.
    only: Filters to select the Modules to set the attributes of.
    graph: If ``True`` (default), uses graph-mode which supports the full
      NNX feature set including shared references. If ``False``, uses
      tree-mode which treats Modules as regular JAX pytrees, avoiding
      the overhead of the graph protocol.
    **kwargs: The attributes to set.
  """
  predicate = filterlib.to_predicate(only)

  remaining = set(kwargs)

  def _set_mode_fn(path, node):
    if hasattr(node, 'set_view') and predicate(path, node):
      sig = inspect.signature(node.set_view)
      has_var_keyword = any(
        p.kind == inspect.Parameter.VAR_KEYWORD
        for p in sig.parameters.values()
      )
      if has_var_keyword:
        node.set_view(**kwargs)
        remaining.clear()
      else:
        named_params = {
          name
          for name, p in sig.parameters.items()
          if p.kind
          in (
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.KEYWORD_ONLY,
          )
        }
        filtered_kwargs = {
          k: v for k, v in kwargs.items() if k in named_params
        }
        node.set_view(**filtered_kwargs)
        remaining.difference_update(named_params)
    return node

  out = graphlib.recursive_map(_set_mode_fn, node, graph=graph)

  if raise_if_not_found and remaining:
    raise ValueError(f"Unused keys found in nnx.view: {sorted(remaining)}")

  return out

