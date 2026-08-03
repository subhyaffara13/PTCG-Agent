import itertools
from typing import Any, Tuple

def convert_interleaved_input(operands: Sequence[Any]) -> Tuple[str, Tuple[Any, ...]]:
    """Convert 'interleaved' input to standard einsum input."""
    tmp_operands = list(operands)
    operand_list = []
    subscript_list = []
    for _ in range(len(operands) // 2):
        operand_list.append(tmp_operands.pop(0))
        subscript_list.append(tmp_operands.pop(0))

    output_list = tmp_operands[-1] if len(tmp_operands) else None

    # build a map from user symbols to single-character symbols based on `get_symbol`
    # The map retains the intrinsic order of user symbols
    try:
        # collect all user symbols
        symbol_set = set(itertools.chain.from_iterable(subscript_list))

        # remove Ellipsis because it can not be compared with other objects
        symbol_set.discard(Ellipsis)

        # build the map based on sorted user symbols, retaining the order we lost in the `set`
        symbol_map = {symbol: get_symbol(idx) for idx, symbol in enumerate(sorted(symbol_set))}

    except TypeError:  # unhashable or uncomparable object
        raise TypeError(
            "For this input type lists must contain either Ellipsis "
            "or hashable and comparable object (e.g. int, str)."
        )

    subscripts = ",".join(convert_subscripts(sub, symbol_map) for sub in subscript_list)
    if output_list is not None:
        subscripts += "->"
        subscripts += convert_subscripts(output_list, symbol_map)

    return subscripts, tuple(operand_list)

