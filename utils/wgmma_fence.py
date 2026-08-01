
def wgmma_fence(array: fa.FragmentedArray) -> fa.FragmentedArray:
  """Fences the array construction from WGMMA instructions.

  LLVM treats in-register computation as pure and can move it after the fence,
  which is explicitly disallowed by the PTX programming model. For that reason,
  we insert an LLVM optimization barrier before the fence.
  """
  array = fa.optimization_barrier(array)
  nvvm.wgmma_fence_aligned()
  return array

