
def get_mesh_from_symbol(symtab: ir.SymbolTable) -> mesh_lib.AbstractMesh:
  if "mesh" not in symtab:
    return mesh_lib.empty_abstract_mesh
  # pyrefly: ignore[missing-attribute]
  mesh_attr = sdy.MeshAttr(symtab["mesh"].mesh)
  axes = [sdy.MeshAxisAttr(a) for a in mesh_attr.axes]
  if not axes:
    return mesh_lib.empty_abstract_mesh
  axes_sizes = tuple(a.size for a in axes)
  axes_names = tuple(a.name for a in axes)
  # TODO(necula): Shardy meshes do not have axis_types :-(
  return mesh_lib.AbstractMesh(axes_sizes, axes_names)

