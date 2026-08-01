
def has_sdy_mesh(symtab: ir.SymbolTable, submodule: ir.Module) -> bool:
  for mesh_name in ("mesh", "empty_mesh", "maximal_mesh_0"):
    if mesh_name in symtab:
      return isinstance(symtab[mesh_name], sdy.MeshOp)
  return has_sdy_meshes_in_frontend_attributes(submodule)

