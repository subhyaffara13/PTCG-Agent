
def dtypes_to_str(dtype_list: Sequence[DType], empty_means_all=False) -> str:
  """User-friendly description of a set of dtypes"""
  if not dtype_list and empty_means_all:
    return "all"

  names: set[str] = {np.dtype(dt).name for dt in dtype_list}
  signed = {"int8", "int16", "int32", "int64"}
  if signed <= names:
    names = (names - signed) | {"signed"}
  integers = {"uint8", "uint16", "uint32", "uint64"}
  if integers <= names:
    names = (names - integers) | {"unsigned"}
  integer = {"signed", "unsigned"}
  if integer <= names:
    names = (names - integer) | {"integer"}

  floating = {"bfloat16", "float16", "float32", "float64"}
  if floating <= names:
    names = (names - floating) | {"floating"}

  complex = {"complex64", "complex128"}
  if complex <= names:
    names = (names - complex) | {"complex"}

  inexact = {"floating", "complex"}
  if inexact <= names:
    names = (names - inexact) | {"inexact"}

  all_types = {"integer", "inexact", "bool"}
  if all_types <= names:
    names = (names - all_types) | {"all"}

  return ", ".join(sorted(names))

