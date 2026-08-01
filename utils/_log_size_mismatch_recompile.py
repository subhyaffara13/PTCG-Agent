
def _log_size_mismatch_recompile() -> None:
    global _LOGGED_DYNAMIC_ALLOWLIST
    if not _LOGGED_DYNAMIC_ALLOWLIST:
        torch._utils_internal.add_mlhub_insight(
            category="dynamic_shapes_analysis",
            insight="Dynamic shape recompilation detected",
            insight_description="PGO detected a recompilation due to dynamic shapes. \
            Please follow the instruction from the action link to reduce \
            recompilation overhead.",
        )
        # add mlhub insight only once per rank
        _LOGGED_DYNAMIC_ALLOWLIST = True

