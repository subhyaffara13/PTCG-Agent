
def _jaxpr_call(
    jaxpr: jax_core.Jaxpr,
    *refs: state_types.AbstractRef | state_types.TransformedRef,
    program_ids: Sequence[jax_typing.Array | None],
) -> Sequence[jax_typing.Array]:
  """Internal primitive for calling a kernel jaxpr inside ``emit_pipeline``.

  This is *not* a general purpose primitive. In particular, it assumes that
  the transformed references have been indexed.

  Args:
    jaxpr: The jaxpr to call.
    *refs: The references to pass into the jaxpr.
    program_ids: The loop-bound program IDs to pass into the jaxpr, or None if
      the program ID corresponds to a parallel dimension.

  Returns:
    The outputs of the jaxpr.
  """
  assert not jaxpr.outvars
  flat_refs = []
  ref_treedefs = []
  ref: Any
  for ref in refs:
    if isinstance(ref, state_types.TransformedRef):
      if not isinstance(ref.transforms[-1], indexing.NDIndexer):
        raise ValueError(
            "TransformedRef must have been indexed before passing into"
            f" jaxpr_call. Got {ref}."
        )
      ref = (ref.ref, ref.transforms)
    flat_ref, treedef = tree_util.tree_flatten(ref)
    flat_refs.extend(flat_ref)
    ref_treedefs.append(treedef)
  flat_program_ids, program_ids_treedef = tree_util.tree_flatten(program_ids)
  return jaxpr_call_p.bind(
      *flat_refs,
      *flat_program_ids,
      jaxpr=jaxpr,
      ref_treedefs=tuple(ref_treedefs),
      program_ids_treedef=program_ids_treedef,
  )

