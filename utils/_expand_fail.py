
def _expand_fail(in_tree: PyTreeDef, dyn_argnums: Sequence[int],
                 fail: Sequence[core.ShapedArray | NoFail]
                 ) -> list[core.ShapedArray | NoFail]:
  fail_: list[core.ShapedArray | NoFail] = [no_fail] * in_tree.num_leaves
  for i, f in zip(dyn_argnums, fail):
    fail_[i] = f
  return fail_

