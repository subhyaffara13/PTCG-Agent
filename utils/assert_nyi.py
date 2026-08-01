
def assert_nyi(cond: bool, msg: str) -> None:
    if not cond:
        raise NotImplementedError(f"inductor does not support {msg}")

