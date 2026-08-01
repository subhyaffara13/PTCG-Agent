
def _get_cpp_global_cache(contains_explicit_attributes: bool):
  if contains_explicit_attributes:
    return _cpp_pjit_cache_explicit_attributes
  else:
    return _cpp_pjit_cache_fun_only

