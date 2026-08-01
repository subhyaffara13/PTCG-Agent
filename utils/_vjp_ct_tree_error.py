
def _vjp_ct_tree_error(jaxpr, out_tree, ct_tree):
  msg = f"""unexpected tree structure.

The argument to a VJP function returned by `jax.vjp` must match the pytree
structure of the differentiated function {jaxpr.debug_info.func_src_info}.

But the tree structures differ:
"""
  msg += '\n'.join(f"  * out{keystr(path)} was a {thing1} in the original "
                   f"output, but a {thing2} here, so {explanation}."
                   for path, thing1, thing2, explanation
                   in equality_errors_pytreedef(out_tree, ct_tree))
  raise ValueError(msg)

