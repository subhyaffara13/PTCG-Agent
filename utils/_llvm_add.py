
def _llvm_add(x, y):
  return llvm.add(x, y, overflow_flags=llvm.IntegerOverflowFlags.none)

