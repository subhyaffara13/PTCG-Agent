from typing import Callable

def specialize_dunder(name: str, typ: RType) -> Callable[[DunderSpecializer], DunderSpecializer]:
    """Decorator to register a function as being a dunder specializer.

    Dunder specializers handle special method calls like __getitem__ that
    don't naturally map to CallExpr nodes.

    There may exist multiple specializers for one dunder. When translating
    dunder calls, the earlier appended specializer has higher priority.
    """

    def wrapper(f: DunderSpecializer) -> DunderSpecializer:
        dunder_specializers.setdefault((name, typ), []).append(f)
        return f

    return wrapper

