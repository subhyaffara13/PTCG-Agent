
def analyze_borrowed_arguments(
    blocks: list[BasicBlock], cfg: CFG, borrowed: set[Value]
) -> AnalysisResult[Value]:
    """Calculate arguments that can use references borrowed from the caller.

    When assigning to an argument, it no longer is borrowed.
    """
    return run_analysis(
        blocks=blocks,
        cfg=cfg,
        gen_and_kill=BorrowedArgumentsVisitor(borrowed),
        initial=borrowed,
        backward=False,
        kind=MUST_ANALYSIS,
        universe=borrowed,
    )

