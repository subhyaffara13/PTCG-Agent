
def _unmatch_spec(mesh: Mesh, check_vma, context_mesh, manual_axes, in_spec,
                  x: JaxType) -> JaxType:
  with (core.eval_context(), api.disable_jit(False),
        use_abstract_mesh(context_mesh)):
    return api.jit(HashablePartial(_unmatch, mesh, check_vma, in_spec,
                                   manual_axes))(x)

