
def decide_worker_start_method() -> str:
    if "TORCHINDUCTOR_WORKER_START" in os.environ:
        start_method = os.environ["TORCHINDUCTOR_WORKER_START"]
    else:
        start_method = "subprocess"
    assert start_method in (
        "subprocess",
        "fork",
        "spawn",
    ), f"Invalid start method: {start_method}"
    return start_method

