
def _unmatch_spec2(mesh, prev_manual, spec, x) -> JaxType:
  with (core.eval_context(), api.disable_jit(False),
        use_abstract_mesh(mesh.abstract_mesh)):
    return api.jit(HashablePartial(_unmatch2, mesh, prev_manual, spec))(x)

