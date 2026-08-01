
def register_type_whose_dtype_should_not_be_canonicalized(typ: type):
  global _types_whose_dtype_should_not_be_canonicalized
  _types_whose_dtype_should_not_be_canonicalized += (typ,)

