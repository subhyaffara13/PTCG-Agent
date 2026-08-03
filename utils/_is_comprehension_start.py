import sys

def _is_comprehension_start(tx: InstructionTranslatorBase) -> bool:
    """Detect if we're at the start of a list/dict comprehension in 3.12+.

    In Python 3.12+, comprehensions are inlined with a bytecode pattern that
    precedes BUILD_LIST/BUILD_MAP.
    """
    assert sys.version_info >= (3, 12)

    assert tx.instruction_pointer is not None
    ip = tx.instruction_pointer - 1

    pattern = _get_comprehension_bytecode_prefix()
    prefix = [inst.opname for inst in tx.instructions[ip - len(pattern) : ip]]

    return prefix == pattern

