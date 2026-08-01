
def _hash_string(hash_obj, str_var):
  hash_obj.update(str_var.encode("utf-8").strip())

