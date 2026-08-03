from typing import Any, Callable

def createResolutionCallbackFromEnv(lookup_base: HasGetattr) -> Callable[[str], Any]:
    """
    Creates a resolution callback that will look up qualified names in an
    environment, starting with `lookup_base` for the base of any qualified
    names, then proceeding down the lookup chain with the resolved object.

    You should not use this directly, it should only be used from the other
    createResolutionCallbackFrom* functions.
    """

    def lookupInModule(qualified_name: str, module: Any) -> Any:
        if "." in qualified_name:
            base, remaining_pieces = qualified_name.split(".", maxsplit=1)
            module_value = getattr(module, base)
            return lookupInModule(remaining_pieces, module_value)
        else:
            return getattr(module, qualified_name)

    def parseNestedExpr(expr: str, module: Any) -> tuple[Any, int]:
        i = 0
        while i < len(expr) and expr[i] not in (",", "[", "]"):
            i += 1

        # Special case logic for the empty Tuple as a subscript (used
        # in the type annotation `Tuple[()]`)
        if expr[:i] == "()":
            return (), i

        base = lookupInModule(expr[:i].strip(), module)
        if base is None:
            raise AssertionError(f"Unresolvable type {expr[:i]}")
        if i == len(expr) or expr[i] != "[":
            return base, i

        if expr[i] != "[":
            raise AssertionError(f"expected '[' at position {i}, got {expr[i]!r}")
        parts = []
        while expr[i] != "]":
            part_len = 0
            i += 1
            part, part_len = parseNestedExpr(expr[i:], module)
            parts.append(part)
            i += part_len
        if len(parts) > 1:
            return base[tuple(parts)], i + 1
        else:
            return base[parts[0]], i + 1

    def parseExpr(expr: str, module: Any) -> Any:
        try:
            value, len_parsed = parseNestedExpr(expr, module)
            if len_parsed != len(expr):
                raise AssertionError(
                    "whole expression was not parsed, falling back to c++ parser"
                )
            return value
        except Exception:
            """
            The python resolver fails in several cases in known unit tests, and is intended
            to fall back gracefully to the c++ resolver in general.  For example, python 2 style
            annotations which are frequent in our unit tests often fail with types e.g. int not
            resolvable from the calling frame.
            """
            return None

    return lambda expr: parseExpr(expr, lookup_base)

