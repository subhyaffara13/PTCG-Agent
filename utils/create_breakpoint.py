
def create_breakpoint() -> list[Instruction]:
    """
    Create instructions that trigger the bytecode debugger to stop.

    Usage:
        codegen.extend_output(create_breakpoint())

    When the bytecode debugger is active, execution will pause at this point.
    At runtime, these instructions have no effect on program state.
    """
    from .bytecode_debugger import BREAKPOINT_MARKER

    return [
        create_instruction("LOAD_CONST", argval=BREAKPOINT_MARKER),
        create_instruction("POP_TOP"),
    ]

