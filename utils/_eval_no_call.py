
def _eval_no_call(stmt, glob, loc):
    """Evaluate statement as long as it does not contain any method/function calls."""
    bytecode = compile(stmt, "", mode="eval")
    for insn in dis.get_instructions(bytecode):
        if "CALL" in insn.opname:
            raise RuntimeError(
                f"Type annotation should not contain calls, but '{stmt}' does"
            )
    return eval(bytecode, glob, loc)  # type: ignore[arg-type] # noqa: P204

