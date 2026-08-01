
def _check_metadata(testing_metadata: dict[str, Any]):
    """Check the metadata of an environment."""
    if not isinstance(testing_metadata, dict):
        raise error.InvalidMetadata(
            f"Expect the environment metadata to be dict, actual type: {type(metadata)}"
        )

    render_modes = testing_metadata.get("render_modes")
    if render_modes is None:
        logger.warn(
            f"The environment creator metadata doesn't include `render_modes`, contains: {list(testing_metadata.keys())}"
        )
    elif not isinstance(render_modes, Iterable):
        logger.warn(
            f"Expects the environment metadata render_modes to be a Iterable, actual type: {type(render_modes)}"
        )

