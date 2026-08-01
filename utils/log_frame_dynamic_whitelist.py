
def log_frame_dynamic_whitelist(f_code: types.CodeType) -> None:
    global _KNOWN_DYNAMIC_SOURCES
    code_id = CodeId.make(f_code, None)
    frame_state = get_code_state()[code_id]
    all_dynamic_sources = _collect_dynamic_sources(frame_state)
    frame_whitelist = ",".join(all_dynamic_sources)
    missing_whitelist = ",".join(_collect_missing_sources(all_dynamic_sources))
    if frame_whitelist:
        with dynamo_timed(name := "pgo.dynamic_whitelist", log_pt2_compile_event=True):
            CompileEventLogger.pt2_compile(
                name,
                recompile_dynamic_whitelist=frame_whitelist,
                missing_dynamic_whitelist=missing_whitelist,
            )

