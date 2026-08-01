
def pack_array(values):
  if not values:
    raise ValueError("Empty array")
  elem_ty = values[0].type
  i64 = ir.IntegerType.get_signless(64)
  ptr_ty = ir.Type.parse("!llvm.ptr")
  arr_ptr = llvm.alloca(ptr_ty, c(len(values), i64), elem_ty)
  for i, v in enumerate(values):
    elem_ptr = getelementptr(arr_ptr, [i], elem_ty)
    llvm.store(v, elem_ptr)
  return arr_ptr

