
def _create_timm_model_with_error_handling(config: "TimmWrapperConfig", **model_kwargs):
    """
    Creates a timm model and provides a clear error message if the model is not found,
    suggesting a library update.
    """
    try:
        model = timm.create_model(
            config.architecture,
            pretrained=False,
            **model_kwargs,
        )
        return model
    except RuntimeError as e:
        if "Unknown model" in str(e):
            # A good general check for unknown models.
            raise ImportError(
                f"The model architecture '{config.architecture}' is not supported in your version of timm ({timm.__version__}). "
                "Please upgrade timm to a more recent version with `pip install -U timm`."
            ) from e
        raise e

