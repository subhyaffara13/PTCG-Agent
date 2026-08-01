
def analyze_maybe_defined_regs(
    blocks: list[BasicBlock], cfg: CFG, initial_defined: set[Value]
) -> AnalysisResult[Value]:
    """Calculate potentially defined registers at each CFG location.

    A register is defined if it has a value along some path from the initial location.
    """
    return run_analysis(
        blocks=blocks,
        cfg=cfg,
        gen_and_kill=DefinedVisitor(),
        initial=initial_defined,
        backward=False,
        kind=MAYBE_ANALYSIS,
    )

