
def _atomic_op_type_to_int(atomic_type: AtomicOpType) -> int:
  match atomic_type:
    case AtomicOpType.ADD:
      return 0
    case AtomicOpType.MIN:
      return 1
    case AtomicOpType.MAX:
      return 2
    case AtomicOpType.AND:
      return 3
    case AtomicOpType.OR:
      return 4
    case AtomicOpType.XOR:
      return 5
    case _:
      assert_never(atomic_type)

