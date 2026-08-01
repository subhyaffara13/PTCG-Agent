
def _autotune_num_choices_displayed_default() -> int | None:
    env_val = os.environ.get("TORCHINDUCTOR_AUTOTUNE_NUM_CHOICES_DISPLAYED")
    if env_val is None:
        return 10
    if env_val.lower() in ("none", "all"):
        return None
    return int(env_val)

