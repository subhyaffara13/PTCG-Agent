
def is_known_divisible(value: ir.Value, divisor: int, max_depth=10) -> bool:
  """Returns True if the value is statically known to be divisible by the divisor."""
  if divisor == 1:
    return True
  if max_depth < 0:
    return False

  new_depth = max_depth - 1
  def_op = value.owner

  match def_op:
    case ir.Block() as block:
      op = block.owner
      if isinstance(op, dialect.WarpMapOp):
        arg_index = list(block.arguments).index(value)  # pyrefly: ignore[bad-argument-type]
        operand = op.operands[arg_index]
        return is_known_divisible(operand, divisor, new_depth)
      return False
    # TODO(bchetioui): Clean up match once minimum supported jaxlib is 0.10.2
    case op2 if hasattr(dialect, "AssumeMultipleOp") and isinstance(op2, dialect.AssumeMultipleOp):  # pyrefly: ignore[missing-attribute]
      return ir.IntegerAttr(
          op2.multiple  # pyrefly: ignore[missing-attribute]
      ).value % divisor == 0 or is_known_divisible(op2.value, divisor, new_depth)  # pyrefly: ignore[missing-attribute]
    case arith.IndexCastOp():
      return is_known_divisible(def_op.in_, divisor, max_depth - 1)
    case arith.ConstantOp():
      return def_op.literal_value % divisor == 0
    case arith.MulIOp():
      # Only cover the case where one operand is divisible. It's still possible
      # that the final product is divisible, but we don't check that here.
      return is_known_divisible(
          def_op.lhs, divisor, new_depth
      ) or is_known_divisible(def_op.rhs, divisor, new_depth)
    case arith.SelectOp():
      return is_known_divisible(
          def_op.true_value, divisor, new_depth
      ) and is_known_divisible(def_op.false_value, divisor, new_depth)
    case arith.MaxSIOp() | arith.MinSIOp() | arith.MaxUIOp() | arith.MinUIOp():
      return is_known_divisible(
          def_op.lhs, divisor, new_depth
      ) and is_known_divisible(def_op.rhs, divisor, new_depth)
    case arith.AddIOp() | arith.SubIOp():
      # Only cover the common case where both operads are divisible.
      return is_known_divisible(
          def_op.lhs, divisor, new_depth
      ) and is_known_divisible(def_op.rhs, divisor, new_depth)
    case arith.AndIOp():
      # Only cover the specific case where the divisor is a power of two.
      return divisor.bit_count() == 1 and (
          is_known_divisible(def_op.lhs, divisor, new_depth)
          or is_known_divisible(def_op.rhs, divisor, new_depth)
      )
    case arith.TruncIOp():
      # Only cover the specific case where the divisor is a power of two.
      # trunci(a, bitwidth) = a % 2**bitwidth = a - k * 2**bitwidth for some k.
      # When the divisor is a power of 2, there are two cases:
      #   1. the divisor is smaller than 2**bitwidth. In this case, the divisor
      #      divides 2**bitwidth; if it divides a, it must thus also divide
      #      the truncated value a - k*2**bitwidth for any k;
      #   2. the divisor is larger than 2**bitwidth. In this case, if the
      #      divisor divides a, then we can conclude that a % 2**bitwidth == 0,
      #      and thus that the divisor also divides the truncated value.
      return (divisor.bit_count() == 1 and
              is_known_divisible(def_op.in_, divisor, new_depth))

  logger.debug("Unsupported defining operation %s when "
               "checking divisibility of %s", def_op, value)

  return False

