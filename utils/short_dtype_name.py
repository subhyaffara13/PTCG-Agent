
def short_dtype_name(dtype) -> str:
  if isinstance(dtype, ExtendedDType):
    return str(dtype)
  else:
    return (dtype.name.replace('float', 'f').replace('uint'   , 'u')
                      .replace('int'  , 'i').replace('complex', 'c'))

