
def _clean_keystr_arg_names(k: KeyPath) -> str:
  res = keystr(k)
  return _re_clean_keystr_arg_names.sub(r"\1", res)

