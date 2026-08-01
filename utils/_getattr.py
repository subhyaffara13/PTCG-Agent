
def _getattr(objclass, name, repr_str):
    # hack to grab the reference directly
    try: #XXX: works only for __builtin__ ?
        attr = repr_str.split("'")[3]
        return eval(attr+'.__dict__["'+name+'"]')
    except Exception:
        try:
            attr = objclass.__dict__
            if type(attr) is DictProxyType:
                if sys.hexversion > 0x30f00a0 and name in ('__weakref__','__dict__'):
                    attr = _dictproxy_helper.__dict__[name]
                else:
                    attr = attr[name]
            else:
                attr = getattr(objclass,name)
        except (AttributeError, KeyError):
            attr = getattr(objclass,name)
        return attr


def _getattr(
    obj: _Dataclass,
    attribute_name: str,
) -> _Out:
  """Returns the `obj.attribute_name`."""
  _init_dataclass_state(obj)
  # Accessing the attribute before it was set (e.g. before super().__init__)
  if attribute_name not in obj._dataclass_field_values:  # pylint: disable=protected-access
    raise AttributeError(
        f"type object '{type(obj).__qualname__}' has no attribute "
        f"'{attribute_name}'"
    )
  else:
    return obj._dataclass_field_values[attribute_name]  # pylint: disable=protected-access


def _getattr(
    name: str,
    *,
    module_name: str,
    imported_symbols: dict[str, lazy_imports_utils.LazyModule | Any],
    error_msg: str | None,
) -> Any:
  """Module `__getattr__` that lazy-imports symbols."""
  if name not in imported_symbols:
    raise AttributeError(
        f'module {module_name!r} has no attribute {name!r}',
        name=name,
        obj=sys.modules.get(module_name),
    )
  symbol_or_lazy_module = imported_symbols[name]

  # symbol already loaded
  if not isinstance(symbol_or_lazy_module, lazy_imports_utils.LazyModule):
    return symbol_or_lazy_module

  # Otherwise, load the symbol
  lazy_module = symbol_or_lazy_module
  with lazy_module._maybe_adhoc():  # pylint: disable=protected-access
    try:
      symbol = _import_symbol(
          import_qualname=lazy_module.module_name,
          parent_module_name=module_name,
      )
    except ImportError as e:
      if error_msg:
        reraise_utils.reraise(
            e,
            prefix=error_msg.format(symbol_name=lazy_module.module_name),
        )
      else:
        raise

  imported_symbols[name] = symbol
  return symbol

