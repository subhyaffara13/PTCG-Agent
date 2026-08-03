import sys
from typing import Any, Callable

def _get_comprehension_result_patterns() -> dict[str, dict[str, Any]]:
    """Discover bytecode patterns for comprehension result handling.

    Analyzes sample functions to extract the opcode sequences that appear
    after END_FOR for each result disposition (stored, discarded, returned, consumed).

    Returns patterns with:
        - pre_store_ops: opcodes between END_FOR and first STORE_FAST
        - post_store_op: first opcode after all STORE_FASTs (for disambiguation)
    """
    assert sys.version_info >= (3, 12)

    def fn_stored() -> list[int]:
        result = [i for i in range(1)]  # noqa: C416
        return result

    def fn_discarded() -> int:
        [i for i in range(1)]  # noqa: C416
        return 1

    def fn_returned() -> list[int]:
        return [i for i in range(1)]  # noqa: C416

    def fn_consumed() -> int:
        return sum([i for i in range(1)])  # noqa: C416

    def extract_pattern(fn: Callable[..., Any]) -> tuple[list[str], str | None]:
        """Extract (pre_store_ops, post_store_op) from comprehension bytecode."""
        target_line = list(dis.findlinestarts(fn.__code__))[1][1]
        insts: list[str] = []
        started = False
        for instr in dis.get_instructions(fn):
            if started and instr.starts_line:
                break
            pos = instr.positions
            if pos and pos.lineno == target_line:
                started = started or bool(instr.starts_line)
                insts.append(instr.opname)

        ops = insts[insts.index("END_FOR") + 1 :]
        idx = 0

        pre_store_ops = []
        while idx < len(ops) and ops[idx] != "STORE_FAST":
            pre_store_ops.append(ops[idx])
            idx += 1

        while idx < len(ops) and ops[idx] == "STORE_FAST":
            idx += 1

        return pre_store_ops, ops[idx] if idx < len(ops) else None

    stored = extract_pattern(fn_stored)
    discarded = extract_pattern(fn_discarded)
    returned = extract_pattern(fn_returned)
    consumed = extract_pattern(fn_consumed)

    return {
        "stored": {"pre_store_ops": stored[0], "post_store_op": stored[1]},
        "discarded": {"pre_store_ops": discarded[0], "post_store_op": discarded[1]},
        "returned": {"pre_store_ops": returned[0], "post_store_op": returned[1]},
        "consumed": {"pre_store_ops": consumed[0], "post_store_op": []},
    }

