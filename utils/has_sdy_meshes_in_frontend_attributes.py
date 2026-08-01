
def has_sdy_meshes_in_frontend_attributes(submodule: ir.Module) -> bool:
  if "mhlo.frontend_attributes" not in submodule.operation.attributes:
    return False
  frontend_attributes = ir.DictAttr(
      submodule.operation.attributes["mhlo.frontend_attributes"]
  )
  return "xla.sdy.meshes" in frontend_attributes

