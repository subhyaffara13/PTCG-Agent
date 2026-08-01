
def analyze_maybe_defined_attrs_in_init(
    blocks: list[BasicBlock], self_reg: Register, attrs_with_defaults: set[str], cfg: CFG
) -> AnalysisResult[str]:
    return run_analysis(
        blocks=blocks,
        cfg=cfg,
        gen_and_kill=AttributeMaybeDefinedVisitor(self_reg),
        initial=attrs_with_defaults,
        backward=False,
        kind=MAYBE_ANALYSIS,
    )

