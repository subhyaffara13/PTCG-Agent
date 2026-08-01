
def render_code_state(cs: defaultdict[CodeId, CodeState]) -> str:
    code_state_str = "\n".join(
        f"{k}:\n"
        + "\n".join(
            f"  {src}: {fs.render()}" for src, fs in v.automatic_dynamic.items()
        )
        for k, v in cs.items()
    )
    dynamic_sources: OrderedSet[str] = OrderedSet()
    for state in cs.values():
        dynamic_sources.update(_collect_dynamic_sources(state))
    if dynamic_sources:
        code_state_str += (
            "\n\nPGO detected a recompilation due to dynamic shapes. "
            "To reduce shape recompilations by compiling dynamically to start, "
            f'set environment variable TORCH_COMPILE_DYNAMIC_SOURCES="{",".join(dynamic_sources)}"'
        )
    return code_state_str

