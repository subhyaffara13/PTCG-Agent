
def view_info(node: Module, /, *, only: filterlib.Filter = ..., graph: bool | None = None) -> str:
  """Provides information about the ``view`` arguments for a module and all
  submodules. If no docstring is provided for a module's `set_view`, this function
  puts the `set_view` signature below the function.

  Example::
    >>> from flax import nnx
    ...
    >>> class CustomModel(nnx.Module):
    ...   def __init__(self, *, rngs):
    ...       self.mha = nnx.MultiHeadAttention(4, 8, 32, rngs=rngs)
    ...       self.drop = nnx.Dropout(0.5, rngs=rngs)
    ...       self.bn = nnx.BatchNorm(32, rngs=rngs)
    ...
    >>> model = CustomModel(rngs=nnx.Rngs(0))
    >>> print(nnx.view_info(model))
    BatchNorm:
      use_running_average: bool | None = None
        if True, the stored batch statistics will be
        used instead of computing the batch statistics on the input.
    Dropout:
      deterministic: bool | None = None
        if True, disables dropout masking.
    MultiHeadAttention:
      deterministic: bool | None = None
        if True, the module is set to deterministic mode.
      decode: bool | None = None
        if True, the module is set to decode mode.
      batch_size: int | Shape | None = None
        the batch size to use for the cache.
      max_length: int | None = None
        the max length to use for the cache.

  Args:
    node: the object to display ``view`` information for.
    only: Filters to select the Modules to display information for.
    graph: If ``True`` (default), uses graph-mode which supports the full
      NNX feature set including shared references. If ``False``, uses
      tree-mode which treats Modules as regular JAX pytrees, avoiding
      the overhead of the graph protocol.
  """
  predicate = filterlib.to_predicate(only)
  classes: set[Module] = set()

  def _set_mode_info_fn(path, node):
    if hasattr(node, 'set_view') and predicate(path, node):
      classes.add(node.__class__)
    return node

  graphlib.recursive_map(_set_mode_info_fn, node, graph=graph)

  class_list = sorted(list(classes), key=lambda x: x.__qualname__)
  out_str = []
  for c in class_list:
    out_str.append(f"{c.__qualname__}:")
    sig = inspect.signature(c.set_view)
    doc = inspect.getdoc(c.set_view)

    # Parse docstring
    if isinstance(doc, str):
      start, end = doc.find("Args:\n"), doc.find("Returns:\n")
      if end == -1:
        end = len(doc)
      doc = doc[start+6:end]
      parsed_docstring = _parse_docstring_args(doc)

      # Generate output from signature and docstring
      skip_names = {"self", "args", "kwargs"}
      for name, param in sig.parameters.items():
        if name in skip_names:
          continue

        if param.default is inspect.Parameter.empty:
          out_str.append(f"  {name}: {param.annotation}")
        else:
          out_str.append(f"  {name}: {param.annotation} = {param.default}")
        out_str.append(parsed_docstring[name])
    else:
      out_str.append(f"  set_view{sig}")


  return "\n".join(out_str)

