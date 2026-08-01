
def analyze_must_defined_regs(
    blocks: list[BasicBlock],
    cfg: CFG,
    initial_defined: set[Value],
    regs: Iterable[Value],
    strict_errors: bool = False,
) -> AnalysisResult[Value]:
    """Calculate always defined registers at each CFG location.

    This analysis can work before exception insertion, since it is a
    sound assumption that registers defined in a block might not be
    initialized in its error handler.

    A register is defined if it has a value along all paths from the
    initial location.
    """
    return run_analysis(
        blocks=blocks,
        cfg=cfg,
        gen_and_kill=DefinedVisitor(strict_errors=strict_errors),
        initial=initial_defined,
        backward=False,
        kind=MUST_ANALYSIS,
        universe=set(regs),
    )

