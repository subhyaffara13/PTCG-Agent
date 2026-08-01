
def _run(main_wrapper: Callable[[TextIO, TextIO], None]) -> tuple[str, str, int]:
    stdout = StringIO()
    stderr = StringIO()

    try:
        main_wrapper(stdout, stderr)
        exit_status = 0
    except SystemExit as system_exit:
        assert isinstance(system_exit.code, int)
        exit_status = system_exit.code

    return stdout.getvalue(), stderr.getvalue(), exit_status


def _run(checker, text: str) -> dict:
    """Run a checker's check method, return result dict."""
    try:
        checker.check(text)
        return {"decision": "ALLOW", "score": 0.0, "matched_topic": None}
    except HTTPException as e:
        if e.status_code == 400:
            detail: Dict[str, Any] = e.detail if isinstance(e.detail, dict) else {}
            return {
                "decision": "BLOCK",
                "score": detail.get("score", 1.0),
                "matched_topic": detail.get("topic"),
                "match_type": detail.get("match_type"),
            }
        raise

