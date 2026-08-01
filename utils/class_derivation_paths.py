
def class_derivation_paths(typ: TypeInfo, supertype: TypeInfo) -> list[list[TypeInfo]]:
    """Return an array of non-empty paths of direct base classes from
    type to supertype.  Return [] if no such path could be found.

      InterfaceImplementationPaths(A, B) == [[B]] if A inherits B
      InterfaceImplementationPaths(A, C) == [[B, C]] if A inherits B and
                                                        B inherits C
    """
    # FIX: Currently we might only ever have a single path, so this could be
    #      simplified
    result: list[list[TypeInfo]] = []

    for base in typ.bases:
        btype = base.type
        if btype == supertype:
            result.append([btype])
        else:
            # Try constructing a longer path via the base class.
            for path in class_derivation_paths(btype, supertype):
                result.append([btype] + path)

    return result

