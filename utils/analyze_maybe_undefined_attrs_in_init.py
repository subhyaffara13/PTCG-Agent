
def analyze_maybe_undefined_attrs_in_init(
    blocks: list[BasicBlock], self_reg: Register, initial_undefined: set[str], cfg: CFG
) -> AnalysisResult[str]:
    return run_analysis(
        blocks=blocks,
        cfg=cfg,
        gen_and_kill=AttributeMaybeUndefinedVisitor(self_reg),
        initial=initial_undefined,
        backward=False,
        kind=MAYBE_ANALYSIS,
    )

