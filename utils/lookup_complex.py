from typing import Any, Callable

def lookup_complex(
    func: OpOverload, *args: Any, **kwargs: Any
) -> Callable[..., Any] | None:
    """
    Lookup an impl from the table.

    Try the particular overload first, then the overload packet.

    If nothing is found, try the decompositions with both.
    """
    return COMPLEX_OPS_TABLE.get(
        func,
        COMPLEX_OPS_TABLE.get(
            func.overloadpacket,
            DECOMPOSITIONS.get(func, DECOMPOSITIONS.get(func.overloadpacket)),
        ),
    )

