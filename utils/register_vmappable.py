
def register_vmappable(data_type: type, spec_type: type, axis_size_type: type,
                       to_elt: Callable, from_elt: Callable,
                       make_iota: Callable | None):
  vmappables[data_type] = (spec_type, axis_size_type)
  spec_types.add(spec_type)
  to_elt_handlers[data_type] = to_elt
  from_elt_handlers[data_type] = from_elt
  if make_iota: make_iota_handlers[axis_size_type] = make_iota

