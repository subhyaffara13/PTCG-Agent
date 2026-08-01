
def step_unsupported(msg: str = "") -> None:
    """Force a step unsupported graph break, which results in compiling
    the traced FX graph so far, then skipping the rest of the frame.
    In order to get expected behavior, there should be at least 2 ops
    and a part of the code not contained in any try/with blocks."""

