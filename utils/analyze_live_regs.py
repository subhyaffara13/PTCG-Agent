
def analyze_live_regs(blocks: list[BasicBlock], cfg: CFG) -> AnalysisResult[Value]:
    """Calculate live registers at each CFG location.

    A register is live at a location if it can be read along some CFG path starting
    from the location.
    """
    return run_analysis(
        blocks=blocks,
        cfg=cfg,
        gen_and_kill=LivenessVisitor(),
        initial=set(),
        backward=True,
        kind=MAYBE_ANALYSIS,
    )

