
def is_directory(specobj: spec.ModuleSpec) -> bool:
    return specobj.type == spec.ModuleType.PKG_DIRECTORY

