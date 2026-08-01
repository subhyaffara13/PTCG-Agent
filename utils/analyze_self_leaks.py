
def analyze_self_leaks(
    blocks: list[BasicBlock], self_reg: Register, cfg: CFG
) -> AnalysisResult[None]:
    return run_analysis(
        blocks=blocks,
        cfg=cfg,
        gen_and_kill=SelfLeakedVisitor(self_reg),
        initial=set(),
        backward=False,
        kind=MAYBE_ANALYSIS,
    )

