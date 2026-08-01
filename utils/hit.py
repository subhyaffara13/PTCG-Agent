
def hit(key: str, ty: str) -> defaultdict[CodeId, CodeState]:
    global _INIT_CODE_STATE
    assert isinstance(_CODE_STATE, defaultdict)
    log.info("get_code_state %s hit %s, %d entries", key, ty, len(_CODE_STATE))
    trace_structured_artifact(
        f"get_{ty}_code_state",
        "string",
        lambda: render_code_state(_CODE_STATE),  # type: ignore[arg-type]
    )
    set_feature_use("pgo", True)
    _INIT_CODE_STATE = copy.deepcopy(_CODE_STATE)
    return _CODE_STATE

