
def path_to_str(path: list[tuple[object, object]]) -> str:
    result = "<root>"
    for attr, obj in path:
        t = type(obj).__name__
        if t in ("dict", "tuple", "SymbolTable", "list"):
            result += f"[{repr(attr)}]"
        else:
            if isinstance(obj, Var):
                result += f".{attr}({t}:{obj.name})"
            elif t in ("BuildManager", "FineGrainedBuildManager"):
                # Omit class name for some classes that aren't part of a class
                # hierarchy since there isn't much ambiguity.
                result += f".{attr}"
            else:
                result += f".{attr}({t})"
    return result

