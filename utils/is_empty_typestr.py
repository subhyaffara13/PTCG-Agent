
def is_empty_typestr(typestr: str) -> bool:
  return (
      typestr == RESTORE_TYPE_LIST
      or typestr == RESTORE_TYPE_NAMED_TUPLE
      or typestr == RESTORE_TYPE_TUPLE
      or typestr == RESTORE_TYPE_DICT
      or typestr == RESTORE_TYPE_NONE
  )

