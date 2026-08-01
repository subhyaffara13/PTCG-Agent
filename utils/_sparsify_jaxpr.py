
def _sparsify_jaxpr(spenv: SparsifyEnv,
                    jaxpr: core.ClosedJaxpr, *spvalues):
  # TODO(jakevdp): currently this approach discards all information about
  #   shared data & indices when generating the sparsified jaxpr. The
  #   current approach produces valid sparsified while loops, but they
  #   don't work in corner cases (see associated TODO in sparsify_test.py)
  out_tree: pytree.PyTreeDef | None = None

  def wrapped(*args_flat):
    # TODO(frostig,jakevdp): This closes over `spenv`, which can bring
    # in buffers from the "outer scope" as constants. Is this a
    # problem for primitives like cond and while_loop, which always
    # convert constvars to invars when staging out their subjaxprs?
    nonlocal out_tree
    args = tree_unflatten(in_tree, args_flat)
    spvalues = arrays_to_spvalues(spenv, args)
    result = eval_sparse(jaxpr.jaxpr, jaxpr.consts, spvalues, spenv)
    out = spvalues_to_arrays(spenv, result)
    out_flat, out_tree = tree_flatten(out)
    return out_flat

  args = spvalues_to_arrays(spenv, spvalues)
  args_flat, in_tree = tree_flatten(args)
  avals_flat = [core.typeof(arg) for arg in args_flat]
  sp_jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(
      lu.wrap_init(wrapped, debug_info=jaxpr.jaxpr.debug_info.with_unknown_names()), avals_flat)
  sp_jaxpr = pe.ClosedJaxpr(sp_jaxpr, consts)
  assert out_tree is not None
  return sp_jaxpr, out_tree

