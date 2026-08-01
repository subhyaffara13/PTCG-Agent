
def fori(bound, carrys):
  unwrap = False
  if not isinstance(carrys, (list, tuple)):
    carrys = [carrys]
    unwrap = True
  flat_carrys, carry_treedef = jax.tree.flatten(carrys)

  def wrapper(f):
    c0 = arith.constant(bound.type, 0)
    c1 = arith.constant(bound.type, 1)
    for_op = scf.ForOp(c0, bound, c1, flat_carrys)
    with ir.InsertionPoint(for_op.body):
      i = for_op.induction_variable
      inner_carrys = jax.tree.unflatten(carry_treedef, for_op.inner_iter_args)
      if unwrap:
        [inner_carrys] = inner_carrys
      new_carrys = f(i, inner_carrys)
      if unwrap:
        new_carrys = [new_carrys]
      new_flat_carrys, new_carry_treedef = jax.tree.flatten(new_carrys)
      if new_carry_treedef != carry_treedef:
        raise ValueError(new_carry_treedef, carry_treedef)
      scf.YieldOp(new_flat_carrys)
    final_flat_carrys = for_op.results
    return ForResult(
        for_op, jax.tree.unflatten(carry_treedef, final_flat_carrys)
    )

  return wrapper

