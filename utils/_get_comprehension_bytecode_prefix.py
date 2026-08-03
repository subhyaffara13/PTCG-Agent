import sys

def _get_comprehension_bytecode_prefix() -> list[str]:
    """Get the bytecode instructions that precede BUILD_LIST in a list comprehension."""

    assert sys.version_info >= (3, 12)

    def fn() -> list[int]:
        return [i for i in range(1)]  # noqa: C416

    insts = [inst.opname for inst in dis.get_instructions(fn)]

    start_idx = len(insts) - 1 - insts[::-1].index("LOAD_FAST_AND_CLEAR")
    end_idx = insts.index("BUILD_LIST")

    return insts[start_idx:end_idx]

