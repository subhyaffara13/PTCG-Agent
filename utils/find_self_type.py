from typing import Callable

def find_self_type(typ: Type, lookup: Callable[[str], SymbolTableNode | None]) -> bool:
    return typ.accept(HasSelfType(lookup))

