
def _apply_tensorify_python_scalars(module: torch.fx.GraphModule) -> None:
    """
    Util to apply tensorify_python_scalars.
    """
    # TODO(anijain2305) - Add tensorify_python_scalars to the HOP graph passes.
    fake_mode = detect_fake_mode()
    if fake_mode is not None and fake_mode.shape_env is not None:
        tensorify_python_scalars(module, fake_mode.shape_env, fake_mode)

