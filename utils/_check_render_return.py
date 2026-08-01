
def _check_render_return(render_mode, render_return):
    """Produces warning if `render_return` doesn't match `render_mode`."""
    if render_mode == "human":
        if render_return is not None:
            logger.warn(
                f"Human rendering should return `None`, got {type(render_return)}"
            )
    elif render_mode == "rgb_array":
        if not isinstance(render_return, np.ndarray):
            logger.warn(
                f"RGB-array rendering should return a numpy array, got {type(render_return)}"
            )
        else:
            if render_return.dtype != np.uint8:
                logger.warn(
                    f"RGB-array rendering should return a numpy array with dtype uint8, got {render_return.dtype}"
                )
            if render_return.ndim != 3:
                logger.warn(
                    f"RGB-array rendering should return a numpy array with three axes, got {render_return.ndim}"
                )
            if render_return.ndim == 3 and render_return.shape[2] != 3:
                logger.warn(
                    f"RGB-array rendering should return a numpy array in which the last axis has three dimensions, got {render_return.shape[2]}"
                )
    elif render_mode == "depth_array":
        if not isinstance(render_return, np.ndarray):
            logger.warn(
                f"Depth-array rendering should return a numpy array, got {type(render_return)}"
            )
        elif render_return.ndim != 2:
            logger.warn(
                f"Depth-array rendering should return a numpy array with two axes, got {render_return.ndim}"
            )
    elif render_mode in ["ansi", "ascii"]:
        if not isinstance(render_return, str):
            logger.warn(
                f"ANSI/ASCII rendering should produce a string, got {type(render_return)}"
            )
    elif render_mode.endswith("_list"):
        if not isinstance(render_return, list):
            logger.warn(
                f"Render mode `{render_mode}` should produce a list, got {type(render_return)}"
            )
        else:
            base_render_mode = render_mode[: -len("_list")]
            for item in render_return:
                _check_render_return(
                    base_render_mode, item
                )  # Check that each item of the list matches the base render mode

