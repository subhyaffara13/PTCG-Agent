
def get_repr(obj: Representable) -> str:
  REPR_CONTEXT.depth += 1
  try:
    if not isinstance(obj, Representable):
      raise TypeError(f'Object {obj!r} is not representable')

    c = REPR_CONTEXT.current_color
    iterator = obj.__nnx_repr__()
    config = next(iterator)

    if not isinstance(config, Object):
      raise TypeError(f'First item must be Config, got {type(config).__name__}')

    kv_sep = f'{c.SEP}{config.kv_sep}{c.END}'

    def _repr_elem(elem: tp.Any) -> str:
      if not isinstance(elem, Attr):
        raise TypeError(f'Item must be Elem, got {type(elem).__name__}')

      value_repr = elem.value if elem.use_raw_value else colorized(elem.value)
      value_repr = value_repr.replace('\n', '\n' + config.indent)
      key = elem.key if elem.use_raw_key else f'{c.ATTRIBUTE}{elem.key}{c.END}'
      indent = '' if config.same_line else config.indent

      return f'{indent}{elem.start}{key}{kv_sep}{value_repr}{elem.end}'

    max_depth_reached = (
      flax_config.flax_max_repr_depth is not None
      and REPR_CONTEXT.depth > flax_config.flax_max_repr_depth
    )
    if max_depth_reached:
      elems = '...'
    else:
      elems = config.elem_sep.join(map(_repr_elem, iterator))

    if elems:
      if config.same_line or max_depth_reached:
        elems_repr = elems
        comment = ''
      else:
        elems_repr = '\n' + elems + '\n'
        comment = f'{c.COMMENT}{config.comment}{c.END}'
    else:
      elems_repr = config.empty_repr
      comment = ''

    type_repr = (
      config.type if isinstance(config.type, str) else config.type.__name__
    )
    type_repr = f'{c.TYPE}{type_repr}{c.END}' if type_repr else ''
    start = f'{c.PAREN}{config.start}{c.END}' if config.start else ''
    end = f'{c.PAREN}{config.end}{c.END}' if config.end else ''

    out = f'{type_repr}{start}{comment}{elems_repr}{end}'
    return out
  finally:
    REPR_CONTEXT.depth -= 1

