from typing import Any, Optional, Tuple

def get_type(obj):
    '''Determine the type of the object if among some of the built-in ones.'''
    otype = type(obj)
    if any(otype is t for t in set([int, float, str, bool])):
        return {'type': otype}
    return {}


def get_type(type):
    """Convert the given type to a torchScript acceptable format."""
    if isinstance(type, str):
        return type
    elif inspect.getmodule(type) == typing:
        # If the type is a type imported from typing
        # like Tuple, List, Dict then replace `typing.`
        # with a null string. This needs to be done since
        # typing.List is not accepted by TorchScript.
        type_to_string = str(type)
        return type_to_string.replace(type.__module__ + ".", "")
    elif is_torch_native_class(type):
        # If the type is a subtype of torch module, then TorchScript expects a fully qualified name
        # for the type which is obtained by combining the module name and type name.
        return type.__module__ + "." + type.__name__
    else:
        # For all other types use the name for the type.
        return type.__name__


def get_type(
    tokens: list[tokenize.TokenInfo], start_index: int
) -> tuple[int, int, Literal["code", "docstring", "comment", "empty"]]:
    """Return the line type : docstring, comment, code, empty."""
    i = start_index
    start = tokens[i][2]
    pos = start
    line_type = None
    while i < len(tokens) and tokens[i][2][0] == start[0]:
        tok_type = tokens[i][0]
        pos = tokens[i][3]
        if line_type is None:
            if tok_type == tokenize.STRING:
                line_type = "docstring"
            elif tok_type == tokenize.COMMENT:
                line_type = "comment"
            elif tok_type in JUNK:
                pass
            else:
                line_type = "code"
        i += 1
    if line_type is None:
        line_type = "empty"
    elif i < len(tokens) and tokens[i][0] == tokenize.NEWLINE:
        i += 1
    # Mypy fails to infer the literal of line_type
    return i, pos[0] - start[0] + 1, line_type  # type: ignore[return-value]


def get_type(agent: Tuple[str, int]):
    return agent[0]


def get_type(agent):
    return agent[: agent.rfind("_")]


def get_type(agent: Tuple[str, int]):
    return agent[0]


def get_type(agent):
    return agent[: agent.rfind("_")]


def get_type(
    config_path: str,
    config: Any,
    normalize=True,
    default_type: Optional[Type[Any]] = None,
):
  """Gets type of field in config described by a config_path.

  Example usage:
    >>> config = {'a': {'b', {'c', 10}}}
    >>> assert config_path.get_type('a.b.c', config) is int

  Args:
    config_path: Any string that `split` can process.
    config: A nested datastructure
    normalize: whether to normalize the type (in particular strip Optional
      annotations on dataclass fields)
    default_type: If the `config_path` is not found and `default_type` is set,
      the `default_type` is returned.

  Returns:
    The type of last object when walking config with config_path.

  Raises:
    IndexError: Integer field not found in nested structure.
    KeyError: Non-integer field not found in nested structure.
    ValueError: Empty/invalid config_path after parsing.
    TypeError: Ambiguous type annotation on dataclass field.
  """
  holder, field = _get_holder_field(config_path, config)
  # Check if config is a DM collection and hence has attribute get_type()
  if isinstance(holder,
                (config_dict.ConfigDict, config_dict.FieldReference)):
    if default_type is not None and field not in holder:
      return default_type
    return holder.get_type(field)
  # For dataclasses we can just use the type annotation.
  elif dc.is_dataclass(holder):
    matches = [f.type for f in dc.fields(holder) if f.name == field]
    if not matches:
      raise KeyError(f'Field {field} not found on dataclass {type(holder)}')
    return normalize_type(matches[0]) if normalize else matches[0]
  else:
    return type(_get_item_or_attribute(holder, field, config_path))

