
def register_hitype(val_cls, typeof_fn) -> None:
  core.pytype_aval_mappings[val_cls] = typeof_fn
  dtypes.register_canonicalize_value_handler(val_cls, None)

