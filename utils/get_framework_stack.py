
def get_framework_stack(
    num_frames: int = 25, cpp: bool = False
) -> list[dict[str, Any]]:
    """
    Returns the traceback for the user stack and the framework stack
    """
    from torch.fx.experimental.symbolic_shapes import uninteresting_files
    from torch.utils._traceback import CapturedTraceback

    tb = CapturedTraceback.extract(cpp=cpp).summary()
    tb = [
        frame
        for frame in tb
        if (
            (
                frame.filename.endswith(".py")
                and frame.filename not in uninteresting_files()
            )
            or ("at::" in frame.name or "torch::" in frame.name)
        )
    ]

    return from_traceback(tb[-1 * num_frames :])

