
def _select_to_ifop(f, prev_refs, rest_refs, idx, options):
  # TODO(b/502722198): Use IndexSwitchOp instead of nested IfOp if it's fixed.
  assert len(options) >= 2
  pred = arith.cmpi(arith.CmpIPredicate.eq, idx, ir_constant(0, idx.type))
  if_op = scf.IfOp(pred, [], has_else=True)
  with ir.InsertionPoint(if_op.then_block):
    out = _lower_transformed_refs(f, prev_refs, [options[0]] + rest_refs)
    scf.yield_(out)
  assert if_op.else_block is not None
  with ir.InsertionPoint(if_op.else_block):
    if len(options) > 2:
      idx = arith.subi(idx, ir_constant(1, idx.type))
      out = _select_to_ifop(f, prev_refs, rest_refs, idx, options[1:])
    else:
      out = _lower_transformed_refs(f, prev_refs, [options[1]] + rest_refs)
    scf.yield_(out)
  return if_op.results

