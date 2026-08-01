
def _is_tma_reduction_op_supported(
    reduction_op: TMAReductionOp | None, dtype: ir.Type,
) -> bool:
  """Returns whether the given TMA reduction op supports the given dtype.

  This function essentially implements the table at:
  https://docs.nvidia.com/cuda/parallel-thread-execution/#data-movement-and-conversion-instructions-cp-reduce-async-bulk-tensor
  with the following differences:
  - For `add` reductions, we also support int64, treating it as uint64.
  - For `and`, `or`, and `xor` reductions, we support signed integer types.
  - For `inc` and `dec` reductions, we support both signed and unsigned i32
    treating both as unsigned.
  """
  i32 = ir.IntegerType.get_signless(32)
  i64 = ir.IntegerType.get_signless(64)
  f16 = ir.F16Type.get()
  f32 = ir.F32Type.get()
  bf16 = ir.BF16Type.get()

  match reduction_op:
    case None:
      return True
    case "add":
      return dtype in (f16, f32, bf16, i32, i64)
    case "max" | "min":
      return dtype in (f16, bf16)
    case "umax" | "umin" | "smax" | "smin":
      return dtype in (i32, i64)
    case "inc" | "dec":
      return dtype == i32
    case "and" | "or" | "xor":
      return dtype in (i32, i64)

